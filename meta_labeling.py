import numpy as np

import pandas as pd


# =====================================
# Triple Barrier Meta Labeling
# =====================================

def create_meta_labels(

    df,

    horizon=10,

    tp_atr_multiplier=2.0,

    sl_atr_multiplier=1.5

):

    # =====================================
    # Initialize Labels
    # =====================================

    labels = []

    future_returns_list = []

    # =====================================
    # First Pass:
    # Calculate Future Returns
    # =====================================

    for i in range(len(df)):

        # =====================================
        # Prevent Overflow
        # =====================================

        if i + horizon >= len(df):

            future_returns_list.append(0)

            continue

        # =====================================
        # Current Price
        # =====================================

        current_close = (

            df['close'].iloc[i]

        )

        # =====================================
        # Future Window
        # =====================================

        future_window = (

            df['close'].iloc[
                i + 1:
                i + horizon + 1
            ]

        )

        # =====================================
        # Future Return
        # =====================================

        future_return = (

            (
                future_window.iloc[-1]
                -
                current_close
            )
            /
            current_close
        )

        future_returns_list.append(

            future_return

        )

    # =====================================
    # Save Future Returns
    # =====================================

    df['future_returns'] = future_returns_list

    # =====================================
    # Future Strength
    # =====================================

    df['future_strength'] = (

        abs(df['future_returns'])

    )

    # =====================================
    # Dynamic Strength Threshold
    # =====================================

    df['strength_threshold'] = (

        df['future_strength']
        .rolling(100)
        .quantile(0.60)

    )

    # =====================================
    # Main Triple Barrier Loop
    # =====================================

    for i in range(len(df)):

        # =====================================
        # Prevent Overflow
        # =====================================

        if i + horizon >= len(df):

            labels.append(0)

            continue

        # =====================================
        # Current Values
        # =====================================

        current_close = (

            df['close'].iloc[i]

        )

        atr = (

            df['atr'].iloc[i]

        )

        future_return = (

            df['future_returns'].iloc[i]

        )

        future_strength = (

            df['future_strength'].iloc[i]

        )

        strength_threshold = (

            df['strength_threshold'].iloc[i]

        )

        # =====================================
        # Handle NaN Threshold
        # =====================================

        if np.isnan(strength_threshold):

            labels.append(0)

            continue

        # =====================================
        # Triple Barrier Levels
        # =====================================

        take_profit = (

            current_close +

            (tp_atr_multiplier * atr)

        )

        stop_loss = (

            current_close -

            (sl_atr_multiplier * atr)

        )

        # =====================================
        # Future Window
        # =====================================

        future_data = (

            df.iloc[

                i + 1:

                i + horizon + 1

            ]

        )

        # =====================================
        # Initialize Label
        # =====================================

        label = 0

        # =====================================
        # Triple Barrier Checks
        # =====================================

        for _, row in future_data.iterrows():

            future_high = row['high']

            future_low = row['low']

            # =====================================
            # Strong Bullish Label
            # =====================================

            if (

                future_high >= take_profit

                and

                future_return > 0

                and

                future_strength > strength_threshold

            ):

                label = 1

                break

            # =====================================
            # Strong Bearish Label
            # =====================================

            elif (

                future_low <= stop_loss

                and

                future_return < 0

                and

                future_strength > strength_threshold

            ):

                label = -1

                break

        # =====================================
        # Save Label
        # =====================================

        labels.append(label)

    # =====================================
    # Save Labels
    # =====================================

    df['meta_target'] = labels

    # =====================================
    # Diagnostics
    # =====================================

    print(

        "\n===== META LABEL DISTRIBUTION ====="

    )

    print(

        df['meta_target']
        .value_counts()

    )

    # =====================================
    # Cleanup
    # =====================================

    df.drop(

        columns=[
            'future_returns',
            'future_strength',
            'strength_threshold'
        ],

        inplace=True

    )

    return df