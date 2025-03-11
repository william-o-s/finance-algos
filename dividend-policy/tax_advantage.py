'''
Creates a 3D surface mapping the tax advantage of share repurchases relative to dividends at various
tax rates.
'''

import numpy as np
import pandas as pd
import plotly.express as px
from dataclasses import dataclass

# Global assumptions
NUM_SHARES = 1_000
BASIS_PRICE = 1
AVAILABLE_CAPITAL = 1_000

def tax_paid_on_dividends(dividend_paid: float, income_tax_rate: np.ndarray) -> np.ndarray:
    dividends_tax = dividend_paid * income_tax_rate
    return dividends_tax

def tax_paid_on_capital_gains(capital: float, capital_gains_tax_rate: np.ndarray, new_price: np.ndarray) -> np.ndarray:
    remaining_shares = NUM_SHARES - (capital // new_price)
    capital_gains = new_price - BASIS_PRICE
    capital_gains_tax = remaining_shares * capital_gains * capital_gains_tax_rate
    return capital_gains_tax

def tax_advantage_of_repurchases(income_tax_rate: np.ndarray, capital_gains_tax_rate: np.ndarray, new_price: np.ndarray) -> np.ndarray:
    dividends_tax = tax_paid_on_dividends(AVAILABLE_CAPITAL, income_tax_rate)
    capital_gains_tax = tax_paid_on_capital_gains(AVAILABLE_CAPITAL, capital_gains_tax_rate, new_price)
    tax_advantage = dividends_tax - capital_gains_tax
    return tax_advantage

def tax_advantage_graph(income_tax_rate: np.ndarray, capital_gains_tax_rate: np.ndarray, new_price: np.ndarray, tax_advantage: np.ndarray):
    df = pd.DataFrame({
        'income_tax_rate': income_tax_rate,
        'capital_gains_tax_rate': capital_gains_tax_rate,
        'new_price': new_price,
        'tax_advantage': tax_advantage,
    })

    fig = px.scatter_3d(
        df,
        x = 'income_tax_rate',
        y = 'capital_gains_tax_rate',
        z = 'new_price',
        color = 'tax_advantage',
    )

    fig.update_layout(
        height = 800,
        width = 800,
        title = 'Relative Tax Advantage of Share Repurchases vs. Issuing Dividends',
        scene = dict(
            xaxis_title = 'Income Tax Rate',
            yaxis_title = 'Capital Gains Tax Rate',
            zaxis_title = 'Realised Price',
        )
    )

    fig.show()

def main():
    # Generate configuration
    income_tax_rate = np.arange(0.1, 1.0, 0.1)
    capital_gains_tax_rate = np.arange(0.1, 1.0, 0.1)
    # new_price = np.arange(1, 11, 1)
    new_price = np.array([2, 5, 10])

    # Calculate tax advantage
    itr, cgtr, n = np.meshgrid(income_tax_rate, capital_gains_tax_rate, new_price)
    ta = tax_advantage_of_repurchases(itr, cgtr, n)

    print(f"pre-flatten -> itr: {itr.shape}, cgtr: {cgtr.shape}, n: {n.shape}, ta: {ta.shape}")
    itr = itr.flatten()
    cgtr = cgtr.flatten()
    n = n.flatten()
    ta = ta.flatten()
    print(f"post-flatten -> itr: {itr.shape}, cgtr: {cgtr.shape}, n: {n.shape}, ta: {ta.shape}")

    # Show results
    tax_advantage_graph(itr, cgtr, n, ta)

if __name__ == '__main__':
    main()
