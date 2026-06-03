import pandas as pd

import yfinance as yf


def load_data(

    filepath=None,

    symbol="^NSEI",

    use_yfinance=False,

    period="730d",

    interval="15m"

):

    # =========================
    # YFINANCE MODE
    # =========================

    if use_yfinance:

        df = yf.download(

            symbol,

            period=period,

            interval=interval

        )

        # Flatten columns if MultiIndex

        if isinstance(df.columns, pd.MultiIndex):

            df.columns = [

                col[0].lower()

                for col in df.columns

            ]

# =========================
# CSV MODE
# =========================

    else:

        df = pd.read_csv(filepath)

        # Detect datetime column

        date_column = df.columns[0]

        df[date_column] = pd.to_datetime(

            df[date_column]

        )

        df.set_index(

            date_column,

            inplace=True

        )

        # Lowercase all columns

        df.columns = [

            col.lower()

            for col in df.columns

        ]

        df.sort_index(

            inplace=True

        )

        return df