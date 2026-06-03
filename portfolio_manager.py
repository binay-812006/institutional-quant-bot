import numpy as np


# =====================================
# Portfolio Manager
# =====================================

def combine_portfolio_signals(

    df,

    bearish_signals,

    bullish_signals,

    bullish_weight=0.7,

    bearish_weight=0.3

):

    # =====================================
    # Combined Signals
    # =====================================

    combined_signals = []

    allocations = []

    # =====================================
    # Main Loop
    # =====================================

    for i in range(len(df)):

        market_regime = (

            df[
                'market_regime'
            ].iloc[i]

        )

        bearish_signal = (

            bearish_signals[i]

        )

        bullish_signal = (

            bullish_signals[i]

        )

        # =====================================
        # Bearish Regime
        # =====================================

        if (

            market_regime < 0

            and

            bearish_signal == -1

        ):

            combined_signals.append(-1)

            allocations.append(

                bearish_weight

            )

        # =====================================
        # Bullish Regime
        # =====================================

        elif (

            market_regime > 0

            and

            bullish_signal == 1

        ):

            combined_signals.append(1)

            allocations.append(

                bullish_weight

            )

        # =====================================
        # Neutral
        # =====================================

        else:

            combined_signals.append(0)

            allocations.append(0)

    # =====================================
    # Diagnostics
    # =====================================

    print(

        "\n===== PORTFOLIO SIGNAL DISTRIBUTION ====="

    )

    print({

        'Long': combined_signals.count(1),

        'Short': combined_signals.count(-1),

        'Flat': combined_signals.count(0)

    })

    print(

        "\n===== PORTFOLIO ALLOCATION ====="

    )

    print({

        'Bullish Weight': bullish_weight,

        'Bearish Weight': bearish_weight

    })

    active_allocations = [

        a for a in allocations

        if a > 0

    ]

    if len(active_allocations) > 0:

        print(

            "Average Active Allocation:",

            np.mean(active_allocations)

        )

    # =====================================
    # Return
    # =====================================

    return (

        combined_signals,

        allocations

    )