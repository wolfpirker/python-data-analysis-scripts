import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# Fetch data (returns MultiIndex DataFrame)
assets = ['BTC-USD', '^GSPC', 'GC=F', 'SI=F']
data = yf.download(assets, period='12mo', interval='1wk')

# Extract 'Close' prices (since 'Adj Close' isn't available)
close_prices = data['Close'].copy()
close_prices.columns = ['BTC', 'SP500', 'Gold', 'Silver']  # Rename columns

# Calculate weekly returns
returns = close_prices.pct_change().dropna()

# Compute rolling 4-week correlations
correlations = pd.DataFrame({
    'Date': returns.index,
    'BTC_SP500_Correlation': returns['BTC'].rolling(window=4).corr(returns['SP500']),
    'BTC_Gold_Correlation': returns['BTC'].rolling(window=4).corr(returns['Gold']),
    'BTC_Silver_Correlation': returns['BTC'].rolling(window=4).corr(returns['Silver'])
}).dropna()

# Save to CSV
correlations.to_csv('bitcoin_correlations.csv', index=False)

# Plot
plt.figure(figsize=(12, 6))
plt.plot(correlations['Date'], correlations['BTC_SP500_Correlation'], label='BTC vs S&P 500')
plt.plot(correlations['Date'], correlations['BTC_Gold_Correlation'], label='BTC vs Gold')
plt.plot(correlations['Date'], correlations['BTC_Silver_Correlation'], label='BTC vs Silver')
plt.title('Bitcoin 4-Week Rolling Correlation with US Stocks, Gold, and Silver (Past 12 Months)')
plt.xlabel('Date')
plt.ylabel('Correlation')
plt.legend()
plt.grid(True)
plt.show()
