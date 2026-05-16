import pandas as pd


def load_data(filepath):

    df = pd.read_csv(filepath)

    # Datetime conversion

    df['date'] = pd.to_datetime(df['date'])

    # Set index

    df.set_index('date', inplace=True)

    # Sort

    df.sort_index(inplace=True)

    return df