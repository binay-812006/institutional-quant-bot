import numpy as np


# =====================================
# Dynamic Risk Position Sizing
# =====================================

def calculate_position_size(

    capital,

    atr,

    confidence,

    risk_per_trade=0.01,

    max_position_size=2,

    signal_direction=None,

    spread_strength=0

):

    # =====================================
    # Safety Checks
    # =====================================

    if atr <= 0:

        return 1

    if confidence <= 0:

        return 1

    # =====================================
    # Volatility Adjusted Risk
    # =====================================

    dollar_risk = (

        capital *

        risk_per_trade

    )

    # =====================================
    # Confidence Multiplier
    # =====================================

    confidence_multiplier = (

        1 +

        (confidence * 2)

    )

    # =====================================
    # Raw Position Size
    # =====================================

    raw_position_size = (

        dollar_risk /

        atr

    )

    # =====================================
    # Final Position Size
    # =====================================

    position_size = (

        raw_position_size *

        confidence_multiplier

    )

    # =====================================
    # Bearish Alpha Boost
    # =====================================

    if (

        signal_direction == -1

        and

        spread_strength < -0.04

    ):

        position_size *= 1.15

    # =====================================
    # Normalize
    # =====================================

    position_size = max(

        1,

        min(

            position_size,

            max_position_size

        )

    )

    return round(

        position_size,

        2

    )


# =====================================
# Drawdown-Based Risk Reduction
# =====================================

def adjust_risk_for_drawdown(

    capital,

    peak_capital,

    base_risk=0.005

):

    # =====================================
    # Drawdown
    # =====================================

    drawdown = (

        (peak_capital - capital)

        /

        peak_capital

    )

    # =====================================
    # Dynamic Risk Scaling
    # =====================================

    if drawdown > 0.20:

        return base_risk * 0.4

    elif drawdown > 0.10:

        return base_risk * 0.6

    elif drawdown > 0.05:

        return base_risk * 0.8

    else:

        return base_risk