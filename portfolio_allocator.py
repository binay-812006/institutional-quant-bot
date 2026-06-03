# =====================================
# Portfolio Allocator
# =====================================

def allocate_portfolio(

    bullish_capital,

    bearish_capital,

    bullish_weight=0.7,

    bearish_weight=0.3

):

    portfolio_capital = (

        bullish_capital * bullish_weight

        +

        bearish_capital * bearish_weight

    )

    print(

        "\n===== PORTFOLIO ALLOCATION ====="

    )

    print(

        f"Bullish Capital: {bullish_capital:.2f}"

    )

    print(

        f"Bearish Capital: {bearish_capital:.2f}"

    )

    print(

        f"Bullish Weight: {bullish_weight}"

    )

    print(

        f"Bearish Weight: {bearish_weight}"

    )

    print(

        f"Portfolio Capital: {portfolio_capital:.2f}"

    )

    return portfolio_capital