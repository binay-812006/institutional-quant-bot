from sklearn.ensemble import (
    RandomForestClassifier
)

from sklearn.metrics import (
    accuracy_score
)


def walkforward_validation(
    X,
    y,
    train_size=20000,
    test_size=2000,
    step_size=2000
):

    results = []

    start = 0

    while (
        start + train_size + test_size
        <= len(X)
    ):

        X_train = X.iloc[
            start :
            start + train_size
        ]

        y_train = y.iloc[
            start :
            start + train_size
        ]

        X_test = X.iloc[
            start + train_size :
            start + train_size + test_size
        ]

        y_test = y.iloc[
            start + train_size :
            start + train_size + test_size
        ]

        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=5,
            random_state=42
        )

        model.fit(
            X_train,
            y_train
        )

        predictions = model.predict(
            X_test
        )

        accuracy = accuracy_score(
            y_test,
            predictions
        )

        results.append(accuracy)

        print(
            f"Window Accuracy: "
            f"{accuracy:.4f}"
        )

        start += step_size

    return results