import numpy as np


def run_portfolio_backtest(

    df,

    portfolio_signals,

    allocations,

    initial_capital=100000

):

    capital = initial_capital

    capital_history = []

    trades = []

    position = 0

    entry_price = 0

    allocation = 0

    for i in range(len(df)):

        signal = portfolio_signals[i]

        price = df['close'].iloc[i]

        # Entry

        if position == 0 and signal != 0:

            position = signal

            entry_price = price

            allocation = allocations[i]

        # Exit

        elif position == 1 and signal == 0:

            pnl = (

                (price - entry_price)

                / entry_price

            ) * capital * allocation

            capital += pnl

            trades.append(pnl)

            position = 0

        elif position == -1 and signal == 0:

            pnl = (

                (entry_price - price)

                / entry_price

            ) * capital * allocation

            capital += pnl

            trades.append(pnl)

            position = 0

        capital_history.append(capital)

    print(

        "\n===== PORTFOLIO RESULTS ====="

    )

    print(

        "Final Capital:",

        round(capital, 2)

    )

    print(

        "Total Trades:",

        len(trades)

    )

    if len(trades) > 0:

        print(

            "Average Trade:",

            round(np.mean(trades), 2)

        )

    return (

        capital,

        capital_history,

        trades

    )