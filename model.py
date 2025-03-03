import numpy as np
import pandas as pd
import requests

# List of top 50 energy companies
energy_companies = [
    ("XOM", "Exxon Mobil Corporation"),
    ("CVX", "Chevron Corporation"),
    ("SHEL", "Shell plc"),
    ("RYDAF", "Shell plc"),
    ("TTE", "TotalEnergies SE"),
    ("TTFNF", "TotalEnergies SE"),
    ("COP", "ConocoPhillips"),
    ("CSUAY", "China Shenhua Energy Company Limited"),
    ("ENB", "Enbridge Inc."),
    ("EBBNF", "Enbridge Inc."),
    ("BP", "BP p.l.c."),
    ("BPAQF", "BP p.l.c."),
    ("PBR", "Petróleo Brasileiro S.A. - Petrobras"),
    ("PBR-A", "Petróleo Brasileiro S.A. - Petrobras"),
    ("EPD", "Enterprise Products Partners L.P."),
    ("EOG", "EOG Resources, Inc."),
    ("WMB", "The Williams Companies, Inc."),
    ("ET", "Energy Transfer LP"),
    ("EQNR", "Equinor ASA"),
    ("STOHF", "Equinor ASA"),
    ("KMI", "Kinder Morgan, Inc."),
    ("CNQ", "Canadian Natural Resources Limited"),
    ("SLB", "Schlumberger Limited"),
    ("OKE", "ONEOK, Inc."),
    ("MPLX", "MPLX LP"),
    ("PSX", "Phillips 66"),
    ("TNCAF", "TC Energy Corporation"),
    ("LNG", "Cheniere Energy, Inc."),
    ("MPC", "Marathon Petroleum Corporation"),
    ("SU", "Suncor Energy Inc."),
    ("TRP", "TC Energy Corporation"),
    ("FANG", "Diamondback Energy, Inc."),
    ("HES", "Hess Corporation"),
    ("OXY", "Occidental Petroleum Corporation"),
    ("EIPAF", "Eni S.p.A."),
    ("E", "Eni S.p.A."),
    ("BKR", "Baker Hughes Company"),
    ("TRGP", "Targa Resources Corp."),
    ("VLO", "Valero Energy Corporation"),
    ("IMO", "Imperial Oil Limited"),
    ("TPL", "Texas Pacific Land Corporation"),
    ("CQP", "Cheniere Energy Partners, L.P."),
    ("TCANF", "TC Energy Corporation"),
    ("WDS", "Woodside Energy Group Ltd."),
    ("PUTRY", "PTT Public Company Limited"),
    ("WOPEF", "Woodside Energy Group Ltd."),
    ("EQT", "EQT Corporation"),
    ("CVE", "Cenovus Energy Inc."),
    ("DVN", "Devon Energy Corporation"),
    ("HAL", "Halliburton Company")
]

# Extract tickers and company names
tickers = [company[0] for company in energy_companies]
company_names = [company[1] for company in energy_companies]

# API key and parameters
function = "TIME_SERIES_DAILY"
outputsize = "full"
apikey = "QMRWLT6SQ6Y1WBWX"

# Create a DataFrame to store the final results
final_df = pd.DataFrame(columns=["Name", "Ticker", "Stock Price", "Volatility"])

# Function to calculate volatility
def get_volatility(df):
    """Calculates standard deviation of closing prices"""
    return np.std(df["Close"].values) if not df.empty else np.nan

# Loop through each ticker and fetch data
for i in range(len(tickers)):
    symbol = tickers[i]
    company_name = company_names[i]

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
            continue

        df = pd.DataFrame.from_dict(time_series, orient="index")

        if df.empty:
            print(f"Warning: No trading data available for {symbol}")
            continue

        df.columns = ["Open", "High", "Low", "Close", "Volume"]

        df.index = pd.to_datetime(df.index)
        df = df.sort_index(ascending=False)
        df = df.astype(float)

        df_252 = df.head(min(252, len(df)))
        stock_price = df_252["Close"].iloc[0] if not df_252.empty else np.nan
        volatility = get_volatility(df_252)

        final_df.loc[len(final_df)] = [company_name, symbol, stock_price, volatility]
    else:
        print(f"Error fetching data for {symbol}: {response.status_code}")

print(final_df)



