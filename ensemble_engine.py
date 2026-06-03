from sklearn.ensemble import (

    RandomForestClassifier,

    GradientBoostingClassifier

)

from sklearn.linear_model import (

    LogisticRegression

)

from sklearn.calibration import (

    CalibratedClassifierCV

)

from sklearn.utils.class_weight import (

    compute_sample_weight

)

import numpy as np


# =====================================
# Train Ensemble Models
# =====================================

def train_ensemble(

    X_train,

    y_train

):

    # =====================================
    # Balanced Sample Weights
    # =====================================

    sample_weights = compute_sample_weight(

        class_weight='balanced',

        y=y_train

    )

    # =====================================
    # Random Forest
    # =====================================

    rf_base = RandomForestClassifier(

        n_estimators=120,

        max_depth=5,

        min_samples_split=20,

        min_samples_leaf=10,

        class_weight='balanced',

        n_jobs=-1,

        random_state=42

    )

    # =====================================
    # Logistic Regression
    # =====================================

    lr_base = LogisticRegression(

        max_iter=2000,

        class_weight='balanced',

        random_state=42

    )

    # =====================================
    # Gradient Boosting
    # =====================================

    gb_base = GradientBoostingClassifier(

        n_estimators=80,

        learning_rate=0.05,

        max_depth=3,

        subsample=0.8,

        random_state=42

    )

    # =====================================
    # Probability Calibration
    # =====================================

    rf_model = CalibratedClassifierCV(

        rf_base,

        method='sigmoid',

        cv=2

    )

    lr_model = CalibratedClassifierCV(

        lr_base,

        method='sigmoid',

        cv=2

    )

    gb_model = CalibratedClassifierCV(

        gb_base,

        method='sigmoid',

        cv=2

    )

    # =====================================
    # Train Models
    # =====================================

    rf_model.fit(

        X_train,

        y_train,

        sample_weight=sample_weights

    )

    lr_model.fit(

        X_train,

        y_train,

        sample_weight=sample_weights

    )

    gb_model.fit(

        X_train,

        y_train,

        sample_weight=sample_weights

    )

    # =====================================
    # Return Models
    # =====================================

    return (

        rf_model,

        lr_model,

        gb_model

    )


# =====================================
# Generate Ensemble Signals
# =====================================

def generate_ensemble_signals(

    rf_model,

    lr_model,

    gb_model,

    X_test,

    long_threshold=0.36,

    short_threshold=0.34

):

    # =====================================
    # Predict Probabilities
    # =====================================

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

    # =====================================
    # Ensemble Long Probabilities
    # =====================================

    long_probs = (

        rf_probs[:, 2] +

        lr_probs[:, 2] +

        gb_probs[:, 2]

    ) / 3

    # =====================================
    # Ensemble Short Probabilities
    # =====================================

    short_probs = (

        rf_probs[:, 0] +

        lr_probs[:, 0] +

        gb_probs[:, 0]

    ) / 3

    # =====================================
    # Generate Signals
    # =====================================

    signals = []

    confidence_scores = []

    spreads = []

    for long_p, short_p in zip(

        long_probs,

        short_probs

    ):

        # =====================================
        # Confidence Weighted Spread
        # =====================================

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

        spreads.append(

            spread

        )

        # =====================================
        # Signal Logic
        # =====================================

        if spread > 0.008:

            signals.append(1)

        elif spread < -0.008:

            signals.append(-1)

        else:

            signals.append(0)
            
        # =====================================
        # Confidence Scores
        # =====================================

        confidence_scores.append(

            confidence_strength

        )

    # =====================================
    # Diagnostics
    # =====================================

    print(

        "\n===== ENSEMBLE SIGNAL DISTRIBUTION ====="

    )

    print({

        'Long': signals.count(1),

        'Short': signals.count(-1),

        'Flat': signals.count(0)

    })

    print(

        "\n===== SPREAD STATS ====="

    )

    print(

        "Min:",

        np.min(spreads)

    )

    print(

        "Max:",

        np.max(spreads)

    )

    print(

        "Mean:",

        np.mean(spreads)

    )

    print(

        "\n===== CONFIDENCE STATS ====="

    )

    print(

        "Mean:",

        np.mean(confidence_scores)

    )

    print(

        "Max:",

        np.max(confidence_scores)

    )

    print(

        "Min:",

        np.min(confidence_scores)

    )

    # =====================================
    # Return Results
    # =====================================

    return (

        signals,

        confidence_scores

    )