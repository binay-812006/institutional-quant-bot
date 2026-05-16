import numpy as np


def calculate_metrics(test_df):

    returns = (
        test_df['equity_curve']
        .pct_change()
        .dropna()
    )

    sharpe = (
        np.sqrt(252)
        *
        returns.mean()
        /
        returns.std()
    )

    running_max = (
        test_df['equity_curve']
        .cummax()
    )

    drawdown = (
        test_df['equity_curve']
        -
        running_max
    ) / running_max

    max_drawdown = (
        drawdown.min()
    )

    total_return = (
        (
            test_df[
                'equity_curve'
            ].iloc[-1]
            /
            100000
        ) - 1
    ) * 100

    return {
        "Sharpe": sharpe,
        "MaxDrawdown": max_drawdown,
        "TotalReturn": total_return
    }