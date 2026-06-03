# =====================================
# Bullish Regime Validation Engine
# =====================================

def bullish_regime_check(

    row,

    spread,

    long_probability

):

    # =====================================
    # Extract Features
    # =====================================

    trend_strength = (

        row['trend_strength_4h']

    )

    volatility_regime = (

        row['volatility_regime']

    )

    momentum = (

        row['momentum']

    )

    rsi = (

        row['rsi']

    )

    trend_exhaustion = (

        row['trend_exhaustion']

    )

    # =====================================
    # Strong Bullish Spread
    # =====================================

    spread_condition = (

        spread > 0.015

    )

    # =====================================
    # Trend Confirmation
    # =====================================

    trend_condition = (

        trend_strength > 0

    )

    # =====================================
    # Momentum Confirmation
    # =====================================

    momentum_condition = (

        momentum > 0

    )

    # =====================================
    # RSI Filter
    # Avoid Overbought Entries
    # =====================================

    rsi_condition = (

        rsi < 68

    )

    # =====================================
    # Volatility Filter
    # Avoid Chaotic Bull Regimes
    # =====================================

    volatility_condition = (

        volatility_regime < 1.5

    )

    # =====================================
    # Exhaustion Filter
    # =====================================

    exhaustion_condition = (

        trend_exhaustion < 0.8

    )

    # =====================================
    # Probability Confirmation
    # =====================================

    probability_condition = (

        long_probability > 0.34

    )

    # =====================================
    # Final Bullish Validation
    # =====================================

    bullish_valid = all([

        spread_condition,

        trend_condition,

        momentum_condition,

        rsi_condition,

        volatility_condition,

        exhaustion_condition,

        probability_condition

    ])

    return bullish_valid