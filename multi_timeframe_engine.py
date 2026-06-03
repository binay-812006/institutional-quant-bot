import pandas as pd

# =========================
# Market Regime
# =========================


def create_multi_timeframe_features(df):

    # =========================
    # 1H TIMEFRAME
    # =========================

    df_1h = df.resample('1h').agg({

        'open': 'first',

        'high': 'max',

        'low': 'min',

        'close': 'last',


    })

    # 1H EMA

    df_1h['ema_20_1h'] = (
        df_1h['close']
        .ewm(span=20)
        .mean()
    )

    # 1H Volatility

    df_1h['volatility_1h'] = (
        df_1h['close']
        .pct_change()
        .rolling(20)
        .std()
    )

    # =========================
    # 4H TIMEFRAME
    # =========================

    df_4h = df.resample('4h').agg({

        'open': 'first',

        'high': 'max',

        'low': 'min',

        'close': 'last',


    })

    # 4H EMA

    df_4h['ema_50_4h'] = (
        df_4h['close']
        .ewm(span=50)
        .mean()
    )

    # 4H Trend Strength

    df_4h['trend_strength_4h'] = (
        df_4h['close'] -
        df_4h['ema_50_4h']
    )

    # =========================
    # MERGE 1H FEATURES
    # =========================

    df = df.merge(

        df_1h[
            [
                'ema_20_1h',
                'volatility_1h'
            ]
        ],

        left_index=True,

        right_index=True,

        how='left'

    )

    # =========================
    # MERGE 4H FEATURES
    # =========================

    df = df.merge(

        df_4h[
            [
                'ema_50_4h',
                'trend_strength_4h'
            ]
        ],

        left_index=True,

        right_index=True,

        how='left'

    )

    # =========================
    # FORWARD FILL
    # =========================

    df[
        [
            'ema_20_1h',
            'volatility_1h',
            'ema_50_4h',
            'trend_strength_4h'
        ]
    ] = df[
        [
            'ema_20_1h',
            'volatility_1h',
            'ema_50_4h',
            'trend_strength_4h'
        ]
    ].ffill()

        # =========================
    # Market Regime
    # =========================

    df['market_regime'] = 0

    df.loc[
        df['close'] > df['ema_20_1h'],
        'market_regime'
    ] = 1

    df.loc[
        df['close'] < df['ema_20_1h'],
        'market_regime'
    ] = -1

    return df