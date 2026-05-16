def run_backtest(
    test_df,
    total_cost_pct=0.0008
):

    capital = 100000

    position = 0

    entry_price = 0

    trade_log = []

    equity_curve = []

    for i in range(len(test_df)):

        row = test_df.iloc[i]

        signal = row['signal']

        price = row['close']

        atr = row['atr']

        timestamp = row.name

        # LONG ENTRY

        if signal == 1 and position == 0:

            position = 1

            entry_price = price

            stop_loss = (
                entry_price -
                (1.5 * atr)
            )

            take_profit = (
                entry_price +
                (2 * atr)
            )

            trade_log.append(
                f"{timestamp} BUY at {price}"
            )

        # SHORT ENTRY

        elif signal == -1 and position == 0:

            position = -1

            entry_price = price

            stop_loss = (
                entry_price +
                (1.5 * atr)
            )

            take_profit = (
                entry_price -
                (2 * atr)
            )

            trade_log.append(
                f"{timestamp} SHORT at {price}"
            )

        # LONG EXIT

        elif position == 1:

            if (
                price >= take_profit
                or
                price <= stop_loss
            ):

                pnl = (
                    price -
                    entry_price
                )

                cost = (
                    price *
                    total_cost_pct
                )

                net_pnl = pnl - cost

                capital += net_pnl

                trade_log.append(
                    f"{timestamp} EXIT LONG at {price} | NetPnL: {net_pnl:.2f}"
                )

                position = 0

        # SHORT EXIT

        elif position == -1:

            if (
                price <= take_profit
                or
                price >= stop_loss
            ):

                pnl = (
                    entry_price -
                    price
                )

                cost = (
                    price *
                    total_cost_pct
                )

                net_pnl = pnl - cost

                capital += net_pnl

                trade_log.append(
                    f"{timestamp} EXIT SHORT at {price} | NetPnL: {net_pnl:.2f}"
                )

                position = 0

        equity_curve.append(capital)

    test_df['equity_curve'] = (
        equity_curve
    )

    return (
        test_df,
        capital,
        trade_log
    )