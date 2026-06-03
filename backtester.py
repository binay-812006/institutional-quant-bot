from risk_engine import (

    calculate_position_size,

    adjust_risk_for_drawdown

)

def run_backtest(

    test_df,

    initial_capital=100000,

    total_cost_pct=0.0008

):

    # =========================
    # Initial Setup
    # =========================

    capital = initial_capital

    peak_capital = capital

    position = 0

    entry_price = 0

    position_size = 1

    stop_loss = 0

    take_profit = 0

    consecutive_long = 0
    
    consecutive_short = 0

    bars_held = 0

    breakeven_moved = False

    trade_log = []

    equity_curve = []

    # =========================
    # Main Loop
    # =========================

    for i in range(len(test_df)):

        row = test_df.iloc[i]

        signal = row['signal']

        price = row['close']

        atr = row['atr']

        confidence = row['confidence']

        timestamp = row.name

        # =========================
        # Safety Check
        # =========================

        if atr <= 0:

            equity_curve.append(capital)

            continue

        # =========================
        # Dynamic Risk Adjustment
        # =========================

        risk_per_trade = adjust_risk_for_drawdown(

            capital,

            peak_capital,

            base_risk=0.005

        )

        # =========================
        # Volatility Adjusted
        # Position Sizing
        # =========================

        position_size = calculate_position_size(

            capital=capital,

            atr=atr,

            confidence=confidence,

            risk_per_trade=risk_per_trade,

            max_position_size=2

        )

        # =========================
        # LONG ENTRY
        # =========================

        if signal == 1 and position == 0:

            breakeven_moved = False

             # Exposure Control

            if consecutive_long >= 3:

                equity_curve.append(capital)

                continue

            position = 1

            bars_held = 0

            entry_price = price

            stop_loss = (

                entry_price -

                (1.5 * atr)

            )

            take_profit = (

                entry_price +

                (3 * atr)

            )

            trade_log.append(

                f"{timestamp} BUY at {price:.2f} | Size: {position_size:.2f}"

            )

            consecutive_long += 1

            consecutive_short = 0

        # =========================
        # SHORT ENTRY
        # =========================

        elif signal == -1 and position == 0:

            breakeven_moved = False

            # Exposure Control

            if consecutive_short >= 3:

                equity_curve.append(capital)

                continue
            position = -1

            bars_held = 0

            entry_price = price

            stop_loss = (

                entry_price +

                (1.5 * atr)

            )

            tp_multiplier = (

                3+(confidence * 10)

            )

            take_profit = (

                entry_price-(tp_multiplier * atr)

            )

            trade_log.append(

                f"{timestamp} SHORT at {price:.2f} | Size: {position_size:.2f}"

            )
    
            consecutive_short += 1

            consecutive_long = 0

        # =========================
        # LONG POSITION MANAGEMENT
        # =========================

        elif position == 1:

            bars_held += 1

            # Optional Trailing Stop

            stop_loss = max(

                stop_loss,

                price - (1.2 * atr)

            )

            # =========================
            # Breakeven Protection
            # =========================

            if (

                not breakeven_moved

                and

                price >= (

                    entry_price

                    +

                    (1.5 * atr)

                )

            ):

                stop_loss = entry_price

                breakeven_moved = True
                
            # Exit Logic

            if (

                price >= take_profit

                or

                price <= stop_loss

                or

                bars_held >= 20

            ):

                pnl = (

                    (price - entry_price)

                    * position_size

                )

                cost = (

                    price *

                    total_cost_pct *

                    position_size

                )

                net_pnl = pnl - cost

                capital += net_pnl

                peak_capital = max(

                    peak_capital,

                    capital

                )

                trade_log.append(

                    f"{timestamp} EXIT LONG at {price:.2f} | NetPnL: {net_pnl:.2f}"

                )

                position = 0

                consecutive_long = 0

                bars_held = 0

        # =========================
        # SHORT POSITION MANAGEMENT
        # =========================

        elif position == -1:

            bars_held += 1

            # Optional Trailing Stop

            stop_loss = min(

                stop_loss,

                price + (1.2 * atr)

            )

            # =========================
            # Breakeven Protection
            # =========================

            if (

                not breakeven_moved

                and

                price <= (

                    entry_price

                    -

                    (1.5 * atr)

                )

            ):

                stop_loss = entry_price

                breakeven_moved = True
            # Exit Logic

            if (

                price <= take_profit

                or

                price >= stop_loss

                or

                bars_held >= 20

            ):

                pnl = (

                    (entry_price - price)

                    * position_size

                )

                cost = (

                    price *

                    total_cost_pct *

                    position_size

                )

                net_pnl = pnl - cost

                capital += net_pnl

                peak_capital = max(
                    peak_capital,
                    capital
                )

                trade_log.append(

                    f"{timestamp} EXIT SHORT at {price:.2f} | NetPnL: {net_pnl:.2f}"

                )

                position = 0

                consecutive_short = 0

                bars_held = 0

        # =========================
        # Equity Curve
        # =========================

        equity_curve.append(

            capital

        )

    # =========================
    # Save Equity Curve
    # =========================

    test_df['equity_curve'] = equity_curve

    # =========================
    # Return Results
    # =========================

    return (

        test_df,

        capital,

        trade_log

    )