def get_adaptive_thresholds(

    volatility_regime,

    trend_strength,

    trend_exhaustion

):

    # =========================
    # Base Thresholds
    # =========================

    long_threshold = 0.42

    short_threshold = 0.38

    # =========================
    # High Volatility
    # =========================

    if volatility_regime == 1:

        long_threshold += 0.05

        short_threshold += 0.05

    # =========================
    # Strong Trend
    # =========================

    if abs(trend_strength) > 150:

        long_threshold -= 0.03

        short_threshold -= 0.03

    # =========================
    # Trend Exhaustion
    # =========================

    if trend_exhaustion > 6:

        long_threshold += 0.04

        short_threshold += 0.04

    # =========================
    # Safety Limits
    # =========================

    long_threshold = min(

        max(long_threshold, 0.45),

        0.65

    )

    short_threshold = min(

        max(short_threshold, 0.45),

        0.65

    )

    return (

        long_threshold,

        short_threshold

    )