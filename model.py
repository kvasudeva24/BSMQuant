import numpy as np
import pandas as pd
import requests
import os
from scipy.stats import norm as N

# CSV filename
csv_filename = "energy_companies_stock_data.csv"

# List of energy companies
energy_companies = [
    ("XOM", "Exxon Mobil Corporation"), ("CVX", "Chevron Corporation"),
    ("SHEL", "Shell plc"), ("RYDAF", "Shell plc"), ("TTE", "TotalEnergies SE"),
    ("TTFNF", "TotalEnergies SE"), ("COP", "ConocoPhillips"), 
    ("CSUAY", "China Shenhua Energy Company Limited"), ("ENB", "Enbridge Inc."),
    ("EBBNF", "Enbridge Inc."), ("BP", "BP p.l.c."), ("BPAQF", "BP p.l.c."),
    ("PBR", "Petróleo Brasileiro S.A. - Petrobras"), ("PBR-A", "Petróleo Brasileiro S.A. - Petrobras"),
    ("EPD", "Enterprise Products Partners L.P."), ("EOG", "EOG Resources, Inc."),
    ("WMB", "The Williams Companies, Inc."), ("ET", "Energy Transfer LP"),
    ("EQNR", "Equinor ASA"), ("STOHF", "Equinor ASA"), ("KMI", "Kinder Morgan, Inc."),
    ("CNQ", "Canadian Natural Resources Limited"), ("SLB", "Schlumberger Limited"),
    ("OKE", "ONEOK, Inc."), ("MPLX", "MPLX LP"), ("PSX", "Phillips 66"),
    ("TNCAF", "TC Energy Corporation"), ("LNG", "Cheniere Energy, Inc."),
    ("MPC", "Marathon Petroleum Corporation"), ("SU", "Suncor Energy Inc."),
    ("TRP", "TC Energy Corporation"), ("FANG", "Diamondback Energy, Inc."),
    ("HES", "Hess Corporation"), ("OXY", "Occidental Petroleum Corporation"),
    ("EIPAF", "Eni S.p.A."), ("E", "Eni S.p.A."), ("BKR", "Baker Hughes Company"),
    ("TRGP", "Targa Resources Corp."), ("VLO", "Valero Energy Corporation"),
    ("IMO", "Imperial Oil Limited"), ("TPL", "Texas Pacific Land Corporation"),
    ("CQP", "Cheniere Energy Partners, L.P."), ("TCANF", "TC Energy Corporation"),
    ("WDS", "Woodside Energy Group Ltd."), ("PUTRY", "PTT Public Company Limited"),
    ("WOPEF", "Woodside Energy Group Ltd."), ("EQT", "EQT Corporation"),
    ("CVE", "Cenovus Energy Inc."), ("DVN", "Devon Energy Corporation"),
    ("HAL", "Halliburton Company")
]

# API 
function = "TIME_SERIES_DAILY"
outputsize = "full"
apikeys = ["QMRWLT6SQ6Y1WBWX", "9HUJ8R00XNDPFRKT"]

# volatility
def get_volatility(df):
    return np.std(df["Close"].values) if not df.empty else np.nan

# fetch data only if the CSV file does not exist
if not os.path.exists(csv_filename):
    print("Fetching stock data from API...")

    # df to store final results
    final_df = pd.DataFrame(columns=["Name", "Ticker", "Current Stock Price", "Volatility"])

    for i, (symbol, company_name) in enumerate(energy_companies):
        apikey = apikeys[i // 25]  # switch API key every 25 requests
        url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&outputsize={outputsize}&apikey={apikey}"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if "Error Message" in data or "Note" in data:
                print(f"API limit reached or invalid request for {symbol}. Skipping...")
                continue

            time_series = data.get("Time Series (Daily)", {})
            if not time_series:
                print(f"Warning: No data found for {symbol}")
                print(data)
                continue

            df = pd.DataFrame.from_dict(time_series, orient="index")
            df.columns = ["Open", "High", "Low", "Close", "Volume"]
            df = df.astype({"Open": float, "High": float, "Low": float, "Close": float, "Volume": int})
            df.index.name = "Date"
            df = df.reset_index()

            df_252 = df.head(min(252, len(df)))
            stock_price = df_252["Close"].iloc[0] if not df_252.empty else np.nan
            volatility = get_volatility(df_252)

            final_df.loc[len(final_df)] = [company_name, symbol, stock_price, volatility]
        else:
            print(f"Error fetching data for {symbol}: {response.status_code}")

    # Save to CSV
    final_df.to_csv(csv_filename, index=False)
    print("Data collection complete. CSV file saved.")

# Load stock data from CSV
df = pd.read_csv(csv_filename)
df.columns = ["Name", "Ticker", "Stock Price", "Volatility"]

risk_free = 0.0416  # Risk-free rate

# User input for ticker symbol
while True:
    user_ticker = input("Enter the ticker symbol: ").strip().upper()
    if user_ticker in df["Ticker"].values:
        break
    print("Ticker not found. Please enter a valid ticker.")

# User input for strike price
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
    stock_row = df.loc[df["Ticker"] == user_ticker]

    stock_price = stock_row["Stock Price"].values[0]
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
