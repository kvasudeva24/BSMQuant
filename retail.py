import yfinance as yf
import pandas as pd 
import numpy as np  
from scipy.stats import norm as N

final_df = pd.DataFrame(columns=["Name", "Ticker", "Current Stock Price", "Volatility"])

retail_companies = [
    ("WMT", "Walmart"),
    ("AMZN", "Amazon.com"),
    ("COST", "Costco Wholesale"),
    ("KR", "The Kroger Co."),
    ("HD", "The Home Depot"),
    ("CVS", "CVS Health Corporation"),
    ("TGT", "Target"),
    ("WBA", "Walgreens Boots Alliance"),
    ("LOW", "Lowe's Companies"),
    ("ACI", "Albertsons Companies"),
    ("AAPL", "Apple Stores / iTunes"),
    ("ADRNY", "Royal Ahold Delhaize USA"),
    ("PUSH", "Publix Super Markets"),
    ("TJX", "TJX Companies"),
    ("BBY", "Best Buy"),
    ("DG", "Dollar General"),
    ("DLTR", "Dollar Tree"),
    ("SVNDY", "7-Eleven"),
    ("ACEHF", "Ace Hardware"),
    ("M", "Macy's"),
    ("BJ", "BJ's Wholesale Club"),
    ("T", "AT&T Wireless"),
    ("VZ", "Verizon Wireless"),
    ("ROST", "Ross Stores"),
    ("KSS", "Kohl's"),
    ("ORLY", "O'Reilly Auto Parts"),
    ("AZO", "AutoZone"),
    ("TSCO", "Tractor Supply Co."),
    ("JWN", "Nordstrom"),
    ("DKS", "Dick's Sporting Goods"),
    ("GAP", "Gap"),
    ("MCK", "McKesson Corporation"),
    ("SHW", "Sherwin-Williams"),
    ("ANCTF", "Alimentation Couche-Tard"),
    ("ULTA", "Ulta Beauty"),
    ("CHWY", "Chewy.com"),
    ("W", "Wayfair"),
    ("WINC", "WinCo Foods"),
    ("BURL", "Burlington"),
    ("GNPX", "Good Neighbor Pharmacy"),
    ("DELL", "Dell Technologies")
]

for ticker, company_name in retail_companies:
    try:
        data = yf.Ticker(ticker)
        close = data.history(period="252d")["Close"]
        volatility = np.std(close)
        last_close_price = close.iloc[-1]
        new_row = [company_name, ticker, last_close_price, volatility]
        final_df.loc[len(final_df)] = new_row
    
    except Exception as e:
        print(f"Error processing {ticker} ({company_name}): {e}")

risk_free = 0.0416  # Risk-free rate

while True:
    try:
        user_ticker = input("Enter the ticker symbol: ").strip().upper()
        if user_ticker in final_df["Ticker"].values:
            break
        print("Invalid ticker symbol. Please enter a valid ticker symbol.")
    except ValueError:
        print("Invalid input. Please enter a valid ticker symbol.")


while True:
    try:
        user_strike = float(input("Enter the strike price: $").strip())
        if user_strike > 0:
            break
        print("Strike price must be positive.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")



# User input for time frame
while True:
    try:
        user_time = input("Enter the time frame (years, default=1): ").strip()
        user_time = 1.0 if user_time == "" else float(user_time)
        if user_time > 0:
            break
        print("Time frame must be positive.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

# User input for option type (put/call)
while True:
    put_or_call = input("Enter option type (p for put, c for call): ").strip().lower()
    if put_or_call in ['p', 'c']:
        break
    print("Invalid option type. Enter 'p' for put or 'c' for call.")

# Black-Scholes function
def black_scholes(user_ticker, user_strike, user_time, option_type):
    stock_row = final_df.loc[final_df["Ticker"] == user_ticker]

    stock_price = stock_row["Current Stock Price"].values[0]
    volatility = stock_row["Volatility"].values[0] / 100  

    d1 = (np.log(stock_price / user_strike) + (risk_free + (volatility ** 2) / 2) * user_time) / (volatility * np.sqrt(user_time))
    d2 = d1 - (volatility * np.sqrt(user_time))

    if option_type == 'c':  
        price = (stock_price * N.cdf(d1)) - (user_strike * np.exp(-risk_free * user_time) * N.cdf(d2))
    else:  
        price = (user_strike * np.exp(-risk_free * user_time) * N.cdf(-d2)) - (stock_price * N.cdf(-d1))

    return round(price, 2)

# Calculate and display option price
option_price = black_scholes(user_ticker, user_strike, user_time, put_or_call)
option_type_str = "put" if put_or_call == 'p' else "call"
print(f"The price of the {option_type_str} option is: ${option_price} per share.")