import numpy as np
import pandas as pd


def create_features(df):

    # Returns

    df['returns'] = df['close'].pct_change()

    # Log returns

    df['log_returns'] = np.log(
        df['close'] / df['close'].shift(1)
    )

    # Volatility

    df['volatility'] = (
        df['returns']
        .rolling(20)
        .std()
    )

    # Momentum

    df['momentum'] = (
        df['close'] -
        df['close'].shift(10)
    )

    # Rolling mean

    rolling_mean = (
        df['close']
        .rolling(20)
        .mean()
    )

    # Rolling std

    rolling_std = (
        df['close']
        .rolling(20)
        .std()
    )

    # Z-score

    df['zscore'] = (
        (
            df['close'] -
            rolling_mean
        )
        /
        rolling_std
    )

    # ATR

    high_low = (
        df['high'] -
        df['low']
    )

    high_close = np.abs(
        df['high'] -
        df['close'].shift()
    )

    low_close = np.abs(
        df['low'] -
        df['close'].shift()
    )

    true_range = pd.concat(
        [
            high_low,
            high_close,
            low_close
        ],
        axis=1
    ).max(axis=1)

    df['atr'] = (
        true_range
        .rolling(14)
        .mean()
    )

    # RSI

    delta = df['close'].diff()

    gain = delta.clip(lower=0)

    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()

    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss

    df['rsi'] = (
        100 -
        (
            100 /
            (1 + rs)
        )
    )

    # Hour

    df['hour'] = df.index.hour

    # Session

    df['session'] = np.where(
        df['hour'] < 12,
        0,
        1
    )

    return df