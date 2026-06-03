from data_loader import load_data

from bullish_mean_reversion_engine import (
    generate_bullish_mean_reversion_signals,
    backtest_bullish_mean_reversion
)

from bearish_mean_reversion_engine import (
    generate_bearish_mean_reversion_signals,
    backtest_bearish_mean_reversion
)

from portfolio_manager import (
    combine_portfolio_signals
)

from portfolio_allocator import (
    allocate_portfolio
)

from portfolio_backtester import (
    run_portfolio_backtest
)

from feature_engineering import (
    create_features
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

from multi_timeframe_engine import (
    create_multi_timeframe_features
)

from preprocessing import (
    scale_features
)

from feature_analysis import (
    analyze_feature_importance
)

from confidence_engine import (
    generate_confidence_signals
)

from walkforward_engine import (
    run_walkforward
)

from meta_labeling import (
    create_meta_labels
)

# Load

df = load_data(filepath="D:/institutional_quant_bot/data/raw/nifty50.csv")

# Features

df = create_features(df)

# Multiple Timeframes
df = create_multi_timeframe_features(df)

# Targets

df = create_meta_labels(df)
print(

    "\n===== META LABEL DISTRIBUTION ====="

)

print(

    df['meta_target']
    .value_counts()

)

# =====================================
# Bullish Mean Reversion Signals
# =====================================

bullish_signals, bullish_confidence = (

    generate_bullish_mean_reversion_signals(df)

)

# Features list

features = [

    'returns',

    'log_returns',

    'volatility',

    'momentum',

    'zscore',

    'atr',

    'rsi',

    'ema_20_1h',

    'ema_50_4h',

    'trend_strength_4h',

    'body_strength',

    'upper_wick',

    'lower_wick',

    'volatility_regime',

    'rsi_exhaustion',

    'candle_expansion',

    'trend_persistence',

    'trend_exhaustion',

    'volatility_expansion',
    
    'trend_acceleration',
   
    'downside_pressure',
   
    'range_expansion',
   
    'momentum_exhaustion'

    ]

# Dataset

print(df[features].isna().sum())

print(df[features].shape)

print(df[features].dropna().shape)

print("\n===== FEATURE NaNs =====")

print(

    df[features]
    .isna()
    .sum()

)

print("\n===== FEATURE SHAPE =====")

print(

    df[features]
    .shape

)

print("\n===== AFTER DROPNA =====")

print(

    df[features]
    .dropna()
    .shape

)

# =====================================
# Bullish Mean Reversion Backtest
# =====================================

bullish_capital, bullish_history, bullish_trades = (

    backtest_bullish_mean_reversion(

        df,

        bullish_signals

    )

)

# =====================================
# Combined Portfolio Signals
# =====================================

portfolio_signals, allocations = (

    combine_portfolio_signals(

        df,

        bearish_signals=[0] * len(df),

        bullish_signals=bullish_signals,

        bullish_weight=0.7,

        bearish_weight=0.3

    )

)

portfolio_capital, portfolio_history, portfolio_trades = (

    run_portfolio_backtest(

        df,

        portfolio_signals,

        allocations

    )

)

print(

    "\n===== PORTFOLIO CAPITAL ====="

)

print(

    portfolio_capital

)

print(

    "\n===== BULLISH ENGINE CAPITAL ====="

)

print(

    bullish_capital

)

print(

    "\n===== BULLISH ENGINE TRADES ====="

)

print(

    len(bullish_trades)

)

X, y = build_dataset(
    df,
    features
)

# =========================
# Walk-Forward Training
# =========================

walkforward_results, predictions, actuals, capital_history = (

run_walkforward(

    df,

    X,

    y

)

)

print(

    "\n===== WALKFORWARD RESULTS ====="

)

print(

    walkforward_results

)

print(

    "\nAverage Accuracy:",

    sum(walkforward_results)

    /

    len(walkforward_results)

)
print(

    "\n===== CAPITAL HISTORY ====="

)

print(

    capital_history

)

bearish_capital = capital_history[-1]

portfolio_capital = (

    allocate_portfolio(

        bullish_capital,

        bearish_capital,

        bullish_weight=1.0,

        bearish_weight=0.0

    )

)

"""
# Split

X_train, X_test, y_train, y_test = (
    split_data(X, y)
)

# Scale Features

X_train_scaled, X_test_scaled, scaler = (
    scale_features(
        X_train,
        X_test
    )
)

# Train

rf_model, lr_model, gb_model = (
    train_ensemble(
        X_train_scaled,
        y_train
    )
)

importance_df = analyze_feature_importance(

    rf_model,

    features

)

print(

    "\n===== FEATURE IMPORTANCE ====="

)

print(

    importance_df

)
# Signals

signals, confidence_scores = (

    generate_confidence_signals(
        rf_model,
        lr_model,
        gb_model,
        X_test_scaled,
        test_df
    )

)

print(

    "\n===== SIGNAL DISTRIBUTION ====="

)

print(

    {
        "Long": signals.count(1),

        "Short": signals.count(-1),

        "Flat": signals.count(0)
    }

)

# Test DF

test_df = X_test.copy()

test_df['signal'] = signals

test_df['confidence'] = (

    confidence_scores

)

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
print(df.tail())

print(df.columns)
print(

    df[
        [
            'ema_20_1h',
            'ema_50_4h'
        ]
    ].tail()

)
print(signals[-20:])
"""