import numpy as np

import pandas as pd


# =====================================
# Bearish Mean Reversion Engine
# =====================================

def generate_bearish_mean_reversion_signals(

    df,

    confidence_threshold=0.55

):

    signals = []

    confidence_scores = []

    for i in range(len(df)):

        row = df.iloc[i]

        rsi = row['rsi']

        zscore = row['zscore']

        ema_20_1h = row['ema_20_1h']

        ema_50_4h = row['ema_50_4h']

        trend_strength_4h = row['trend_strength_4h']

        volatility_regime = row['volatility_regime']

        relative_volume = (

            row['relative_volume']

            if 'relative_volume' in df.columns

            else 1

        )

        # =====================================
        # Confidence Score
        # =====================================

        confidence = 0

        if rsi > 70:

            confidence += 0.20

        if zscore > 1:

            confidence += 0.20

        if ema_20_1h < ema_50_4h:

            confidence += 0.20

        if trend_strength_4h < 0:

            confidence += 0.20

        if volatility_regime >= 0:

            confidence += 0.10

        if relative_volume > 1:

            confidence += 0.10

        # =====================================
        # Short Entry
        # =====================================

        if (

            rsi > 70

            and

            zscore > 1

            and

            ema_20_1h < ema_50_4h

            and

            trend_strength_4h < 0

            and

            volatility_regime >= 0

            and

            confidence >= confidence_threshold

        ):

            signals.append(-1)

        else:

            signals.append(0)

        confidence_scores.append(

            confidence

        )

    print(

        "\n===== BEARISH MEAN REVERSION SIGNALS ====="

    )

    print({

        'Short': signals.count(-1),

        'Flat': signals.count(0)

    })

    print(

        "\n===== CONFIDENCE STATS ====="

    )

    print(

        "Mean Confidence:",

        np.mean(confidence_scores)

    )

    print(

        "Max Confidence:",

        np.max(confidence_scores)

    )

    print(

        "Min Confidence:",

        np.min(confidence_scores)

    )

    return (

        signals,

        confidence_scores

    )


# =====================================
# Bearish Backtest
# =====================================

def backtest_bearish_mean_reversion(

    df,

    signals,

    initial_capital=100000

):

    capital = initial_capital

    capital_history = []

    position = 0

    entry_price = 0

    take_profit = 0

    stop_loss = 0

    bars_held = 0

    max_holding_bars = 10

    trades = []

    for i in range(len(df)):

        price = df['close'].iloc[i]

        atr = df['atr'].iloc[i]

        signal = signals[i]

        # =====================================
        # Short Entry
        # =====================================

        if (

            position == 0

            and

            signal == -1

        ):

            position = -1

            entry_price = price

            bars_held = 0

            take_profit = (

                entry_price -

                (1.5 * atr)

            )

            stop_loss = (

                entry_price +

                (1.0 * atr)

            )

        # =====================================
        # Manage Short
        # =====================================

        elif position == -1:

            bars_held += 1

            pnl = (

                entry_price -

                price

            )

            # Take Profit

            if price <= take_profit:

                capital += pnl

                trades.append(pnl)

                position = 0

            # Stop Loss

            elif price >= stop_loss:

                capital += pnl

                trades.append(pnl)

                position = 0

            # Time Exit

            elif bars_held >= max_holding_bars:

                capital += pnl

                trades.append(pnl)

                position = 0

        capital_history.append(

            capital

        )

    print(

        "\n===== BEARISH ENGINE RESULTS ====="

    )

    print(

        "Final Capital:",

        round(capital, 2)

    )

    print(

        "Total Trades:",

        len(trades)

    )

    if len(trades) > 0:

        print(

            "Average Trade:",

            round(np.mean(trades), 2)

        )

    return (

        capital,

        capital_history,

        trades

    )