from data_loader import load_data

from feature_engineering import (
    create_features
)

from target_engine import (
    create_triple_barrier_labels
)

from model_engine import (
    build_dataset,
    split_data
)

from ensemble_engine import (
    train_ensemble,
    generate_ensemble_signals
)

from backtester import (
    run_backtest
)

from metrics import (
    calculate_metrics
)

from utils.logger import (
    save_results
)

# Load

df = load_data(
    "data/raw/INDIA VIX_15minute.csv"
)

# Features

df = create_features(df)

# Targets

df = create_triple_barrier_labels(df)

# Features list

features = [
    'returns',
    'log_returns',
    'volatility',
    'momentum',
    'zscore',
    'atr',
    'rsi',
    'hour',
    'session'
]

# Dataset

X, y = build_dataset(
    df,
    features
)

# Split

X_train, X_test, y_train, y_test = (
    split_data(X, y)
)

# Train

rf_model, lr_model, gb_model = (
    train_ensemble(
        X_train,
        y_train
    )
)

# Signals

signals = generate_ensemble_signals(
    rf_model,
    lr_model,
    gb_model,
    X_test
)

# Test DF

test_df = X_test.copy()

test_df['signal'] = signals

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

# Backtest

test_df, capital, trades = (
    run_backtest(test_df)
)

# Metrics

metrics = calculate_metrics(
    test_df
)

print(
    f"Final Capital: {capital:.2f}"
)

print(metrics)

save_results(
    metrics,
    capital
)