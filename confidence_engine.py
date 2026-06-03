import numpy as np

from bullish_regime_filter import (

    bullish_regime_check

)


def generate_confidence_signals(

    rf_model,

    lr_model,

    gb_model,

    X_test,

    test_df

):

    # =========================
    # Predict Probabilities
    # =========================

    rf_probs = (
        rf_model
        .predict_proba(X_test)
    )

    lr_probs = (
        lr_model
        .predict_proba(X_test)
    )

    gb_probs = (
        gb_model
        .predict_proba(X_test)
    )

    # =========================
    # Debug Classes
    # =========================

    print(

        "\n===== MODEL CLASSES ====="

    )

    print(

        rf_model.classes_

    )

    # =========================
    # Directional Thresholds
    # =========================

    bullish_threshold = 0.020

    bearish_threshold = -0.0025

    # =========================
    # Base Confidence Threshold
    # =========================

    base_confidence = 0.01

    # =========================
    # Long / Short Probabilities
    # =========================

    long_probs = (

        rf_probs[:, 2] +

        lr_probs[:, 2] +

        gb_probs[:, 2]

    ) / 3

    short_probs = (

        rf_probs[:, 0] +

        lr_probs[:, 0] +

        gb_probs[:, 0]

    ) / 3

    # =========================
    # Probability Statistics
    # =========================

    print(

        "\n===== LONG PROBABILITY STATS ====="

    )

    print(

        "Min:", long_probs.min(),

        "Max:", long_probs.max(),

        "Mean:", long_probs.mean()

    )

    print(

        "\n===== SHORT PROBABILITY STATS ====="

    )

    print(

        "Min:", short_probs.min(),

        "Max:", short_probs.max(),

        "Mean:", short_probs.mean()

    )

    # =========================
    # Signal Engine
    # =========================

    signals = []

    confidence_scores = []

    spreads = []

    filtered_signals = 0

    for i, (long_p, short_p) in enumerate(

        zip(

            long_probs,

            short_probs

        )

    ):

        # =========================
        # Relative Probability Spread
        # =========================

        raw_spread = (

            long_p -

            short_p

        )

        confidence_strength = max(

            long_p,

            short_p

        )

        spread = (

            raw_spread *

            confidence_strength

        )

        spreads.append(spread)

        # =========================
        # Signal Quality Score
        # =========================

        signal_quality = (

            abs(spread)

            *

            confidence_strength

        )

        # =========================
        # Market Regime
        # =========================

        market_regime = (

            test_df[
                'market_regime'
            ].iloc[i]

        )

        # =========================
        # Volatility Regime
        # =========================

        volatility_regime = (

            test_df[
                'volatility_regime'
            ].iloc[i]

        )

        # =========================
        # Adaptive Confidence Threshold
        # =========================

        minimum_confidence = (

            base_confidence

            +

            (0.005 * volatility_regime)

        )

        # =========================
        # Long Signal
        # =========================

        if (

            bullish_regime_check(

                test_df.iloc[i],

                spread,

                long_p

            )

            and

            signal_quality > minimum_confidence

        ):

            signals.append(1)

        # =========================
        # Short Signal
        # =========================

        elif (

            spread < bearish_threshold

            and

            short_p > long_p

            and

            market_regime <= 0

            and

            signal_quality > minimum_confidence

        ):

            signals.append(-1)

        # =========================
        # Flat
        # =========================

        else:

            signals.append(0)

            filtered_signals += 1

        # =========================
        # Confidence Score
        # =========================

        confidence_scores.append(

            signal_quality

        )

    # =========================
    # Spread Diagnostics
    # =========================

    print(

        "\n===== SPREAD STATS ====="

    )

    print(

        "Min Spread:",

        np.min(spreads)

    )

    print(

        "Max Spread:",

        np.max(spreads)

    )

    print(

        "Mean Spread:",

        np.mean(spreads)

    )

    # =========================
    # Signal Distribution
    # =========================

    print(

        "\n===== SIGNAL DISTRIBUTION ====="

    )

    print({

        'Long': signals.count(1),

        'Short': signals.count(-1),

        'Flat': signals.count(0)

    })

    # =========================
    # Confidence Diagnostics
    # =========================

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

    # =========================
    # Filter Diagnostics
    # =========================

    print(

        "\n===== FILTERED SIGNAL DISTRIBUTION ====="

    )

    print({

        'Filtered': filtered_signals,

        'Tradable': len(signals) - filtered_signals

    })

    # =========================
    # Return Results
    # =========================

    return (

        signals,

        confidence_scores

    )