import numpy as np
import pandas as pd
import requests


#alpha vantage key: QMRWLT6SQ6Y1WBWX

function = "TIME_SERIES_DAILY"
symbol = "XOM"
outputsize = "full" #to test the code (returns the last 100 trading days vs 20+years of data)
apikey = "QMRWLT6SQ6Y1WBWX"

url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&outputsize={outputsize}&apikey={apikey}"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    time_series = data.get("Time Series (Daily)", {})
    df= pd.DataFrame.from_dict(time_series, orient="index")
    df.columns = ["Open", "High", "Low", "Close", "Volume"]
    df.index = pd.to_datetime(df.index)
    df = df.sort_index(ascending=False)
    df = df.astype(float)
    df_252 = df.head(252)
    print(df_252)
else:
    print(f"Error: {response.status_code}")

#output works correctly, gives us the last 252 trading days of data
# Now I want to get the volatility of the last 252 trading days based on the close value

def get_volatility(df):
    volatility = np.std(df["Close"].values)
    return volatility

print(get_volatility(df_252))
    
