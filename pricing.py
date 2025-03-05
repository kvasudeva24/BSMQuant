import pandas as pd
import numpy as np
from scipy.stats import norm as N

# Creating the dataframe
data = {
    "Name": [
        "Exxon Mobil Corporation", "Chevron Corporation", "Shell plc", "Shell plc", "TotalEnergies SE",
        "TotalEnergies SE", "ConocoPhillips", "China Shenhua Energy Company Limited", "Enbridge Inc.",
        "Enbridge Inc.", "BP p.l.c.", "BP p.l.c.", "Petróleo Brasileiro S.A. - Petrobras",
        "Petróleo Brasileiro S.A. - Petrobras", "Enterprise Products Partners L.P.", "EOG Resources, Inc.",
        "The Williams Companies, Inc.", "Energy Transfer LP", "Equinor ASA", "Equinor ASA",
        "Kinder Morgan, Inc.", "Canadian Natural Resources Limited", "Schlumberger Limited", "ONEOK, Inc.",
        "MPLX LP"
    ],
    "Ticker": [
        "XOM", "CVX", "SHEL", "RYDAF", "TTE", "TTFNF", "COP", "CSUAY", "ENB", "EBBNF", "BP", "BPAQF", "PBR",
        "PBR-A", "EPD", "EOG", "WMB", "ET", "EQNR", "STOHF", "KMI", "CNQ", "SLB", "OKE", "MPLX"
    ],
    "Stock Price": [
        107.7600, 153.0900, 66.4600, 33.3125, 59.8300, 60.0700, 92.6300, 15.2900, 42.6700,
        22.8000, 31.8100, 5.2800, 13.1400, 11.9700, 33.7300, 120.5400, 57.6000, 19.0300,
        22.6600, 23.1400, 27.1400, 26.7200, 39.8200, 96.7600, 54.2600
    ],
    "Volatility": [
        4.709508, 6.327055, 3.338817, 1.724221, 5.457186, 5.539572, 9.226661, 1.299858, 3.280997,
        0.852750, 3.176880, 0.529013, 0.995754, 1.150275, 1.808595, 5.187098, 7.326992, 1.712594,
        1.849751, 1.818995, 3.756201, 19.098849, 4.336511, 10.776069, 4.107592
    ]
}

df = pd.DataFrame(data)

risk_free = 0.0416  

user_ticker = input("Enter the ticker symbol: ").strip().upper()
while user_ticker not in df['Ticker'].values:
    print("Ticker not found.")
    user_ticker = input("Please enter a valid ticker symbol: ").strip().upper()

while True:
    try:
        user_strike = float(input("Please enter the strike price for your desired option: $").strip())
        if user_strike > 0:
            break
        else:
            print("Strike price must be positive.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

while True:
    try:
        user_time = input("Please enter the time frame for your desired option (in years): ").strip()
        user_time = 1.0 if user_time == "" else float(user_time)
        if user_time > 0:
            break
        else:
            print("Time frame must be positive.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

put_or_call = input("Please enter the type of option (p/c): ").strip().lower()
while put_or_call not in ['p', 'c']:
    print("Invalid option type.")
    put_or_call = input("Please enter 'p' for put or 'c' for call: ").strip().lower()

def black_scholes(user_ticker, user_strike, user_time, option_type):
    volatility = df.loc[df['Ticker'] == user_ticker, 'Volatility'].values[0] / 100
    stock_price = df.loc[df['Ticker'] == user_ticker, 'Stock Price'].values[0]

    d1 = (np.log(stock_price / user_strike) + (risk_free + (volatility ** 2) / 2) * user_time) / (volatility * np.sqrt(user_time))
    d2 = d1 - (volatility * np.sqrt(user_time))

    if option_type == 'c':  
        price = (stock_price * N.cdf(d1)) - (user_strike * np.exp(-risk_free * user_time) * N.cdf(d2))
    elif option_type == 'p': 
        price = (user_strike * np.exp(-risk_free * user_time) * N.cdf(-d2)) - (stock_price * N.cdf(-d1))
    
    return round(price, 2)

option_price = black_scholes(user_ticker, user_strike, user_time, put_or_call)

if put_or_call == 'p':
    print(f"The price of the **put** option is: **${option_price}** per share")
elif put_or_call == 'c':
    print(f"The price of the **call** option is: **${option_price}** per share")
