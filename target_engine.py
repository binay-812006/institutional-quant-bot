def create_triple_barrier_labels(df):

    df['tb_target'] = 0

    take_profit_pct = 0.02

    stop_loss_pct = 0.01

    holding_period = 10

    for i in range(
        len(df) - holding_period
    ):

        entry_price = (
            df['close'].iloc[i]
        )

        tp_price = (
            entry_price *
            (1 + take_profit_pct)
        )

        sl_price = (
            entry_price *
            (1 - stop_loss_pct)
        )

        future_prices = df[
            'close'
        ].iloc[
            i+1 : i+1+holding_period
        ]

        label = 0

        for price in future_prices:

            if price >= tp_price:

                label = 1

                break

            elif price <= sl_price:

                label = -1

                break

        df.iloc[
            i,
            df.columns.get_loc(
                'tb_target'
            )
        ] = label

    return df