import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import numpy as np
import pandas as pd

from configparser import ConfigParser
from algotradingstuff.accounts import get_account
from algotradingstuff.sessions import OandaSession


def extract_candle_from_response(response):
    candles = response.get('candles')
    times = []
    opens = []
    highs = []
    lows = []
    closes = []
    for candle in candles:
        times.append(candle.get('time'))
        mid_candle = candle.get('mid')
        opens.append(mid_candle.get('o'))
        highs.append(mid_candle.get('h'))
        lows.append(mid_candle.get('l'))
        closes.append(mid_candle.get('c'))
    df = pd.DataFrame({'time': times,
                       'open': opens,
                       'high': highs,
                       'low': lows,
                       'close': closes},
                      dtype=np.float32)
    return df


parser = ConfigParser()
parser.read('oanda.txt')
api_key = parser.get('oanda', 'api_key')
account_id = parser.get('oanda', 'primary_account')
base_url = parser.get('oanda', 'base_url')

oanda_account = get_account(account_id, api_key, base_url)
oanda_session = OandaSession()
candle_request = oanda_account.get_candles('GBP_USD', granularity='D', count=10)
candles, lti = oanda_session.send(candle_request)
print(candles)
candle_df = extract_candle_from_response(candles)
print(candle_df.head())
# exit()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.line(candle_df, x="time", y="close")

app.layout = html.Div(children=[
    html.H1(children='Forex Monitor'),

    html.Div(children='''
        Monitoring close prices for GBP/USD
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)#, host='0.0.0.0')
