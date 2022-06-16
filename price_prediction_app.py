# Imports

import streamlit as st
from datetime import date
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.set_page_config(layout="wide")

st.title("Deepsight Stock Prediction App")

# All present S&P 500 Companies as a list of tuples
stocks = ('AAPL', 'GLW', 'FISV', 'CLX',	'MDT',	'LH',	'APH',	'BEN', \
    'MSFT',	'VICI',	'ATVI',	'GNRC',	'SCHW',	'MLM',	'RSG',	'CBOE', \
    'GOOG',	'OKE',	'OXY',	'CAG',	'LOW',	'DRE',	'TEL',	'HAS', \
    'GOOGL',	'AMP',	'FIS',	'SWKS',	'ANTM',	'NTRS',	'IQV',	'NI', \
    'AMZN',	'FANG',	'ITW',	'DGX',	'LMT',	'CF',	'O',	'SNA', \
    'TSLA',	'PPG',	'NSC',	'SYF',	'CAT',	'LYV',	'HES',	'LUMN', \
    'BRK.B',	'MTD',	'EQIX',	'TRMB',	'AXP',	'WAT',	'ADSK',	'IPG', \
    'META',	'ALB',	'MPC',	'CE',	'SPGI',	'VTR',	'KR',	'WRK', \
    'JNJ',	'ROST',	'VLO',	'ATO',	'AMT',	'PPL',	'CTAS',	'SBNY', \
    'UNH',	'AVB',	'EW',	'INCY',	'INTU',	'MOS',	'XEL',	'RE', \
    'V',	'EQR',	'HUM',	'SEDG',	'DE',	'MPWR',	'EA',	'CRL', \
    'XOM',	'DFS',	'FCX',	'TER',	'GS',	'IT',	'DLR',	'CCL', \
    'NVDA',	'APTV',	'AON',	'KMX',	'C',	'ALGN',	'CTSH',	'ABMD', \
    'JPM',	'AME',	'APD',	'L',	'BLK',	'GPC',	'PRU',	'TAP', \
    'CVX',	'WY',	'HCA',	'BIO',	'NOW',	'CTLT',	'WELL',	'AAP', \
    'WMT',	'CTRA',	'ICE',	'AKAM',	'EL',	'GRMN',	'DLTR',	'HSIC', \
    'PG',	'VRSK',	'PSA',	'NTAP',	'ADP',	'CINF',	'HPQ',	'QRVO', \
    'MA',	'LVS',	'DG',	'DRI',	'AMAT',	'URI',	'WBA',	'RCL', \
    'HD',	'HRL',	'ETN',	'BXP',	'PYPL',	'MAA',	'A',	'MKTX', \
    'LLY',	'CPRT',	'BSX',	'EVRG',	'CB',	'AMCR',	'AFL',	'CMA', \
    'PFE',	'TROW',	'EMR',	'TTWO',	'MO',	'CMS',	'JCI',	'REG', \
    'KO',	'KEYS',	'MET',	'POOL',	'SBUX',	'RF',	'BKR',	'AIZ', \
    'BAC',	'AWK',	'PSX',	'LNT',	'PLD',	'RJF',	'MSI',	'PHM', \
    'ABBV',	'ENPH',	'NEM',	'NDAQ',	'MDLZ',	'CEG',	'BAX',	'NRG', \
    'PEP',	'GWW',	'MAR',	'CAH',	'BKNG',	'IR',	'WBD',	'DISH', \
    'MRK',	'SIVB',	'GM',	'PKG',	'CI',	'HPE',	'MCHP',	'LW', \
    'AVGO',	'EBAY',	'MRNA',	'XYL',	'DUK',	'PWR',	'CMG',	'NWS', \
    'VZ',	'FITB',	'F',	'IRM',	'MMM',	'DOV',	'ALL',	'NWSA', \
    'COST',	'FRC',	'MCO',	'LKQ',	'EOG',	'WRB',	'HLT',	'JNPR', \
    'TMO',	'ROK',	'KLAC',	'CPB',	'ADI',	'CFG',	'HAL',	'FFIV', \
    'ORCL',	'EIX',	'MNST',	'IEX',	'CHTR',	'VRSN',	'BK',	'ETSY', \
    'ACN',	'DHI',	'DVN',	'SJM',	'SYK',	'VFC',	'PH',	'RHI', \
    'ABT',	'K',	'ADM',	'DPZ',	'GE',	'HBAN',	'BF.B',	'AOS', \
    'CMCSA', 'DTE',	'AEP',	'FMC',	'ZTS',	'FLT',	'AJG',	'UHS', \
    'CSCO',	'CBRE',	'SRE',	'CHRW',	'NFLX',	'PKI',	'SBAC',	'ALLE', \
    'MCD',	'STT',	'SNPS',	'UDR',	'MMC',	'CNP',	'LYB',	'GL', \
    'DHR',	'MKC',	'CNC',	'HWM',	'GILD',	'FOX',	'MSCI',	'WHR', \
    'ADBE',	'ARE',	'KHC',	'CPT',	'BA',	'FOXA',	'SPG',	'SEE', \
    'NKE',	'LUV',	'NXPI',	'LDOS',	'SO',	'TDY',	'GPN',	'DVA', \
    'DIS',	'ZBH',	'MCK',	'OMC',	'NOC',	'HOLX',	'ED',	'CZR', \
    'CRM',	'CDW',	'STZ',	'FDS',	'CME',	'JBHT',	'YUM',	'AAL', \
    'TMUS',	'FE',	'LHX',	'AVY',	'ISRG',	'COO',	'DD',	'OGN', \
    'BMY',	'HIG',	'FTNT',	'TXT',	'CCI',	'ESS',	'TSN',	'BWA', \
    'INTC',	'ETR',	'HSY',	'JKHY',	'USB',	'PARA',	'CARR',	'LNC', \
    'PM',	'WTW',	'ECL',	'TYL',	'BDX',	'EXPD',	'PEG',	'HII', \
    'UPS',	'AEE',	'DOW',	'NVR',	'TJX',	'KEY',	'NUE',	'NLSN', \
    'LIN',	'TSCO',	'PAYX',	'NLOK',	'TGT',	'PAYC',	'IFF',	'FBHS', \
    'QCOM',	'EXR',	'COF',	'TECH',	'PGR',	'STX',	'ILMN',	'TPR', \
    'COP',	'BALL',	'KMB',	'PEAK',	'MU',	'IP',	'TT',	'MHK', \
    'TXN',	'EFX',	'EXC',	'AES',	'PNC',	'PFG',	'MTB',	'ZION', \
    'WFC',	'MTCH',	'AIG',	'MGM',	'PXD',	'SWK',	'ABC',	'PNW', \
    'AMD',	'WST',	'SYY',	'VTRS',	'CSX',	'ROL',	'RMD',	'XRAY', \
    'NEE',	'STE',	'CTVA',	'EMN',	'VRTX',	'J',	'OTIS',	'NWL', \
    'T',	'MRO',	'KMI',	'HST',	'LRCX',	'EPAM',	'PCAR',	'PNR', \
    'RTX',	'ULTA',	'ROP',	'UAL',	'CL',	'BBY',	'WEC',	'FRT', \
    'MS',	'DAL',	'GIS',	'MAS',	'TFC',	'ZBRA',	'TDG',	'BBWI', \
    'UNP',	'FTV',	'TRV',	'KIM',	'SLB',	'WAB',	'BIIB',	'IVZ', \
    'AMGN',	'VMC',	'AZO',	'TFX',	'D',	'BR',	'TWTR',	'DXC', \
    'HON',	'LEN',	'CDNS',	'CTXS',	'WM',	'APA',	'ANET',	'RL', \
    'IBM',	'ANSS',	'WMB',	'PTC',	'GD',	'EXPE',	'FAST',	'CDAY', \
    'CVS',	'CHD',	'ORLY',	'NDSN',	'SHW',	'BRO',	'ES',	'DXCM', \
    'UA',	'UAA',	'PVH',	'NCLH',	'FDX',	'WDC',	'CMI',	'WYNN', \
    'ALK',	'ODFL',	'PENN',	'IPGP',	'REGN',	'MOH',	'IDXX',	'VNO', \
    'ETH-USD', 'BTC-USD')
    

# Import Raw Data
select_stock = st.selectbox("Select a Stock for Prediction", stocks)

timeframe_selector = st.slider("Select a Timeframe for Prediction (In Years)", 1 , 4)
period = timeframe_selector * 365

@st.cache
def load_stock_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

data_load_state =st.text("Loading Data...")
data = load_stock_data(select_stock)
data_load_state.text("Loading Data...Done!")

st.subheader("Raw Price Data")
st.write(data)

def plot_raw_data():
    figure = go.Figure()
    figure.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='stock_open'))
    figure.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='stock_close'))
    figure.layout.update(title_text='Time Series Data', width=1200, height=600, xaxis_rangeslider_visible=True)
    st.plotly_chart(figure)

plot_raw_data()

# Data Training for Forecasting
df_train = data[['Date', 'Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

model = Prophet()
model.fit(df_train)
future = model.make_future_dataframe(periods=period)

forecast = model.predict(future)

st.markdown("""---""")

st.subheader('Forecast Data')
st.write(forecast)

figure_1 = plot_plotly(model, forecast)
figure_1.layout.update(title_text='Forecast Plot', width=1200, height=600, xaxis_rangeslider_visible=True)
st.plotly_chart(figure_1)

st.markdown("""---""")

st.write("Forecast Components")
figure_2 = model.plot_components(forecast)
st.write(figure_2)