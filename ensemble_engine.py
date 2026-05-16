from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier
)

from sklearn.linear_model import (
    LogisticRegression
)


def train_ensemble(
    X_train,
    y_train
):

    # RF

    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=5,
        random_state=42
    )

    rf_model.fit(
        X_train,
        y_train
    )

    # Logistic

    lr_model = LogisticRegression(
        max_iter=1000
    )

    lr_model.fit(
        X_train,
        y_train
    )

    # Gradient Boosting

    gb_model = GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.05,
        max_depth=3,
        random_state=42
    )

    gb_model.fit(
        X_train,
        y_train
    )

    return (
        rf_model,
        lr_model,
        gb_model
    )


def generate_ensemble_signals(
    rf_model,
    lr_model,
    gb_model,
    X_test
):

    rf_probs = (
        rf_model
        .predict_proba(X_test)[:,1]
    )

    lr_probs = (
        lr_model
        .predict_proba(X_test)[:,1]
    )

    gb_probs = (
        gb_model
        .predict_proba(X_test)[:,1]
    )

    ensemble_probs = (
        rf_probs +
        lr_probs +
        gb_probs
    ) / 3

    signals = []

    for prob in ensemble_probs:

        if prob > 0.55:

            signals.append(1)

        elif prob < 0.45:

            signals.append(-1)

        else:

            signals.append(0)

    return signals