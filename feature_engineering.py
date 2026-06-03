import numpy as np
import pandas as pd


def create_features(df):

    # =====================================
    # Returns
    # =====================================

    df['returns'] = df['close'].pct_change()

    # =====================================
    # Log Returns
    # =====================================

    df['log_returns'] = np.log(
        df['close'] / df['close'].shift(1)
    )

    # =====================================
    # Volatility
    # =====================================

    df['volatility'] = (
        df['returns']
        .rolling(20)
        .std()
    )

    # =====================================
    # Momentum
    # =====================================

    df['momentum'] = (
        df['close']
        -
        df['close'].shift(10)
    )

    # =====================================
    # Rolling Statistics
    # =====================================

    rolling_mean = (
        df['close']
        .rolling(20)
        .mean()
    )

    rolling_std = (
        df['close']
        .rolling(20)
        .std()
    )

    # =====================================
    # Z-Score
    # =====================================

    df['zscore'] = (
        (
            df['close']
            -
            rolling_mean
        )
        /
        rolling_std
    )

    # =====================================
    # ATR
    # =====================================

    high_low = (
        df['high']
        -
        df['low']
    )

    high_close = np.abs(
        df['high']
        -
        df['close'].shift()
    )

    low_close = np.abs(
        df['low']
        -
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

    # =====================================
    # RSI
    # =====================================

    delta = df['close'].diff()

    gain = delta.clip(lower=0)

    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()

    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss

    df['rsi'] = (
        100
        -
        (
            100
            /
            (1 + rs)
        )
    )

    # =====================================
    # Time Features
    # =====================================

    df['hour'] = df.index.hour

    df['session'] = np.where(
        df['hour'] < 12,
        0,
        1
    )

    # =====================================
    # Candle Features
    # =====================================

    df['candle_range'] = (

        df['high']

        -

        df['low']

    )

    # =====================================
    # Body Strength
    # =====================================

    df['body_strength'] = (

        abs(

            df['close']

            -

            df['open']

        )

        /

        df['candle_range']

    )

    # =====================================
    # Upper Wick
    # =====================================

    df['upper_wick'] = (

        df['high']

        -

        df[['open', 'close']].max(axis=1)

    ) / df['candle_range']

    # =====================================
    # Lower Wick
    # =====================================

    df['lower_wick'] = (

        df[['open', 'close']].min(axis=1)

        -

        df['low']

    ) / df['candle_range']

    # =====================================
    # Volume Features
    # =====================================

    if 'volume' in df.columns:

        # Relative Volume

        df['relative_volume'] = (

            df['volume']

            /

            df['volume']
            .rolling(20)
            .mean()

        )

        # Volume ZScore

        volume_mean = (

            df['volume']
            .rolling(20)
            .mean()

        )

        volume_std = (

            df['volume']
            .rolling(20)
            .std()

        )

        df['volume_zscore'] = (

            (df['volume'] - volume_mean)

            /

            volume_std

        )

        # Volume Momentum

        df['volume_momentum'] = (

            df['volume']
            .pct_change(5)

        )

    # =====================================
    # Volatility Regime
    # =====================================

    volatility_rank = (

        df['volatility']
        .rolling(100)
        .rank(pct=True)

    )

    df['volatility_regime'] = 0

    df.loc[
        volatility_rank > 0.8,
        'volatility_regime'
    ] = 1

    df.loc[
        volatility_rank < 0.2,
        'volatility_regime'
    ] = -1

    # =====================================
    # RSI Exhaustion
    # =====================================

    df['rsi_exhaustion'] = 0

    df.loc[
        df['rsi'] > 75,
        'rsi_exhaustion'
    ] = -1

    df.loc[
        df['rsi'] < 25,
        'rsi_exhaustion'
    ] = 1

    # =====================================
    # Candle Expansion
    # =====================================

    df['candle_expansion'] = (

        df['candle_range']

        /

        df['candle_range']
        .rolling(20)
        .mean()

    )

    # =====================================
    # Trend Persistence
    # =====================================

    returns_direction = np.sign(

        df['returns']

    )

    df['trend_persistence'] = (

        returns_direction
        .rolling(5)
        .sum()

    )

    # =====================================
    # Trend Exhaustion
    # =====================================

    df['trend_exhaustion'] = (

        abs(df['trend_persistence'])

        *

        df['candle_expansion']

    )

    # =====================================
    # NEW FEATURE:
    # Volatility Expansion
    # =====================================

    df['volatility_expansion'] = (

        df['atr']

        /

        df['atr']
        .rolling(20)
        .mean()

    )

    # =====================================
    # NEW FEATURE:
    # Trend Acceleration
    # =====================================

    df['trend_acceleration'] = (

        df['trend_persistence']
        .diff()

    )

    # =====================================
    # NEW FEATURE:
    # Downside Pressure
    # =====================================

    df['downside_pressure'] = (

        np.where(

            df['returns'] < 0,

            abs(df['returns']),

            0

        )

    )

    # =====================================
    # NEW FEATURE:
    # Range Expansion
    # =====================================

    df['range_expansion'] = (

        (df['high'] - df['low'])

        /

        df['close']

    )

    # =====================================
    # NEW FEATURE:
    # Momentum Exhaustion
    # =====================================

    momentum_std = (

        df['momentum']
        .rolling(10)
        .std()

    )

    df['momentum_exhaustion'] = (

        df['momentum']

        /

        momentum_std

    )

    return df