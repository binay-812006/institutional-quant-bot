from sklearn.model_selection import (
    train_test_split
)


def build_dataset(df, features):

    X = df[features].dropna()

    y = df.loc[
        X.index,
        'tb_target'
    ]

    return X, y


def split_data(X, y):

    return train_test_split(
        X,
        y,
        test_size=0.2,
        shuffle=False
    )