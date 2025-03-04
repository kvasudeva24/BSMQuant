import pandas as pd

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

# Display the DataFrame
print(df)
