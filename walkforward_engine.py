import pandas as pd

from sklearn.metrics import (
    accuracy_score
)

from ensemble_engine import (
    train_ensemble
)

from preprocessing import (
    scale_features
)

from confidence_engine import (
    generate_confidence_signals
)

from backtester import (
    run_backtest
)


def run_walkforward(

    df,

    X,

    y,

    train_size=3000,

    test_size=300,

    step_size=300

):

    # =====================================
    # Storage
    # =====================================

    walkforward_results = []

    all_predictions = []

    all_actuals = []

    capital_history = []

    rolling_capital = 100000

    start = 0

    # =====================================
    # Walk-Forward Loop
    # =====================================

    while (

        start + train_size + test_size

        <= len(X)

    ):

        # =====================================
        # Train Split
        # =====================================

        X_train = X.iloc[
            start:
            start + train_size
        ]

        y_train = y.iloc[
            start:
            start + train_size
        ]

        # =====================================
        # Test Split
        # =====================================

        X_test = X.iloc[
            start + train_size:
            start + train_size + test_size
        ]

        y_test = y.iloc[
            start + train_size:
            start + train_size + test_size
        ]

        # =====================================
        # Scaling
        # =====================================

        X_train_scaled, X_test_scaled, scaler = (

            scale_features(

                X_train,

                X_test

            )

        )

        # =====================================
        # Train Ensemble
        # =====================================

        rf_model, lr_model, gb_model = (

            train_ensemble(

                X_train_scaled,

                y_train

            )

        )

        # =====================================
        # Preserve Original Features
        # =====================================

        test_df = X_test.copy()

        # Real Market Data

        test_df['close'] = (

            df.loc[
                test_df.index,
                'close'
            ]

        )

        test_df['atr'] = (

            df.loc[
                test_df.index,
                'atr'
            ]

        )

        test_df['market_regime'] = (

            df.loc[
                test_df.index,
                'market_regime'
            ]

        )

        # =====================================
        # Generate Signals
        # =====================================

        signals, confidence_scores = (

            generate_confidence_signals(

                rf_model,

                lr_model,

                gb_model,

                X_test_scaled,

                test_df

            )

        )

        # =====================================
        # Regime Filtering
        # =====================================

        filtered_signals = []

        for signal, regime in zip(

            signals,

            test_df['market_regime']

        ):

            # Bullish Regime

            if regime == 1:

                if signal == 1:

                    filtered_signals.append(1)

                else:

                    filtered_signals.append(0)

            # Bearish Regime

            elif regime == -1:

                if signal == -1:

                    filtered_signals.append(-1)

                else:

                    filtered_signals.append(0)

            # Neutral Regime

            else:

                filtered_signals.append(0)

        # =====================================
        # Final Signals
        # =====================================

        test_df['signal'] = (

            filtered_signals

        )

        test_df['confidence'] = (

            confidence_scores

        )

        # =====================================
        # Signal Distribution
        # =====================================

        print(

            "\n===== FILTERED SIGNAL DISTRIBUTION ====="

        )

        print({

            "Long": filtered_signals.count(1),

            "Short": filtered_signals.count(-1),

            "Flat": filtered_signals.count(0)

        })

        # =====================================
        # Accuracy
        # =====================================

        accuracy = accuracy_score(

            y_test,

            filtered_signals

        )

        walkforward_results.append(

            accuracy

        )

        # =====================================
        # Store Results
        # =====================================

        all_predictions.extend(

            filtered_signals

        )

        all_actuals.extend(

            y_test

        )

        # =====================================
        # Backtest
        # =====================================

        test_df, rolling_capital, trades = (

            run_backtest(

                test_df,

                initial_capital=rolling_capital

            )

        )

        capital_history.append(

            rolling_capital

        )

        # =====================================
        # Progress
        # =====================================

        print(

            f"Rolling Capital: {rolling_capital:.2f}"

        )

        print(

            f"WalkForward Accuracy: {accuracy:.4f}"

        )

        # =====================================
        # Move Forward
        # =====================================

        start += step_size

    # =====================================
    # Return Results
    # =====================================

    return (

        walkforward_results,

        all_predictions,

        all_actuals,

        capital_history

    )