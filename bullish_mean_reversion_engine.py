import numpy as np

import pandas as pd


# =====================================
# Bullish Mean Reversion Engine
# =====================================

def generate_bullish_mean_reversion_signals(

    df,

    confidence_threshold=0.55

):

    # =====================================
    # Initialize
    # =====================================

    signals = []

    confidence_scores = []

    # =====================================
    # Main Loop
    # =====================================

    for i in range(len(df)):

        # =====================================
        # Current Row
        # =====================================

        row = df.iloc[i]

        # =====================================
        # Features
        # =====================================

        rsi = row['rsi']

        zscore = row['zscore']

        volatility = row['volatility']

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

        # RSI Contribution

        if rsi < 35:

            confidence += 0.20

        # Z-Score Contribution

        if zscore < -1:

            confidence += 0.20

        # EMA Structure

        if ema_20_1h > ema_50_4h:

            confidence += 0.20

        # Trend Strength

        if trend_strength_4h > 0:

            confidence += 0.20

        # Calm Volatility Regime

        if volatility_regime <= 0:

            confidence += 0.10

        # Relative Volume

        if relative_volume > 1:

            confidence += 0.10

        # =====================================
        # Long Entry Logic
        # =====================================

        if (

            rsi < 35

            and

            zscore < -1

            and

            ema_20_1h > ema_50_4h

            and

            trend_strength_4h > 0

            and

            volatility_regime <= 0

            and

            confidence >= confidence_threshold

        ):

            signals.append(1)

        # =====================================
        # Flat
        # =====================================

        else:

            signals.append(0)

        # =====================================
        # Save Confidence
        # =====================================

        confidence_scores.append(

            confidence

        )

    # =====================================
    # Diagnostics
    # =====================================

    print(

        "\n===== BULLISH MEAN REVERSION SIGNALS ====="

    )

    print({

        'Long': signals.count(1),

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

    # =====================================
    # Return
    # =====================================

    return (

        signals,

        confidence_scores

    )


# =====================================
# Bullish Mean Reversion Backtest
# =====================================

def backtest_bullish_mean_reversion(

    df,

    signals,

    initial_capital=100000

):

    # =====================================
    # Initialize
    # =====================================

    capital = initial_capital

    capital_history = []

    position = 0

    entry_price = 0

    take_profit = 0

    stop_loss = 0

    bars_held = 0

    max_holding_bars = 10

    trades = []

    # =====================================
    # Main Loop
    # =====================================

    for i in range(len(df)):

        price = df['close'].iloc[i]

        atr = df['atr'].iloc[i]

        signal = signals[i]

        # =====================================
        # Entry
        # =====================================

        if (

            position == 0

            and

            signal == 1

        ):

            position = 1

            entry_price = price

            bars_held = 0

            take_profit = (

                entry_price +

                (1.5 * atr)

            )

            stop_loss = (

                entry_price -

                (1.0 * atr)

            )

        # =====================================
        # Manage Long
        # =====================================

        elif position == 1:

            bars_held += 1

            pnl = (

                price -

                entry_price

            )

            # =====================================
            # Take Profit
            # =====================================

            if price >= take_profit:

                capital += pnl

                trades.append(pnl)

                position = 0

            # =====================================
            # Stop Loss
            # =====================================

            elif price <= stop_loss:

                capital += pnl

                trades.append(pnl)

                position = 0

            # =====================================
            # Time Exit
            # =====================================

            elif bars_held >= max_holding_bars:

                capital += pnl

                trades.append(pnl)

                position = 0

        # =====================================
        # Save Capital
        # =====================================

        capital_history.append(

            capital

        )

    # =====================================
    # Diagnostics
    # =====================================

    print(

        "\n===== BULLISH ENGINE RESULTS ====="

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

    # =====================================
    # Return
    # =====================================

    return (

        capital,

        capital_history,

        trades

    )