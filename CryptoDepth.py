
# coding: utf-8

# In[ ]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import pandas as pd
import os
import requests
from gevent.pywsgi import WSGIServer
import exchanges.binance as binance
import exchanges.bitfinex as bitfinex
import exchanges.BTCMarkets as BTCMarkets
import exchanges.independentreserve as independentreserve
import exchanges.OKEx as OKEx
import historicaldata as hisdata
from multiprocessing.pool import ThreadPool


symbols = ['BTC','ETH','EOS','XRP']

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

def getRealtimeData(symbol):
    results = []
    pool = ThreadPool()
    results.append(pool.apply_async(binance.getUSDPrice, args = (symbol,)))
    results.append(pool.apply_async(bitfinex.getUSDPrice, args = (symbol,)))
    results.append(pool.apply_async(BTCMarkets.getUSDPrice, args = (symbol,)))
    results.append(pool.apply_async(independentreserve.getUSDPrice, args = (symbol,)))
    results.append(pool.apply_async(OKEx.getUSDPrice, args = (symbol,)))

    price_list = [r.get() for r in results if r.get() is not None]
    pool.close()
    pool.join()

    df = pd.DataFrame(price_list)
    df = df[['source','bid','ask','trade']]
    df.columns=['Exchange','BestBid','BestAsk','Last Trade Price']
    return df
    
def getHistoricalData(symbol,interval):
    data_list = hisdata.getHistoricalData(symbol,interval)
    return pd.DataFrame(data_list)
    
def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Crypto Exchange Price Compare'
my_js_url = 'http://13.237.159.224/static/adsense.js'

app.layout = html.Div(
[  
        html.Div(
        [
                html.Label('Symbol'),
                dcc.Dropdown(
                    id='symbol',
                    options=[
                        {'label': symbol, 'value': symbol} for symbol in symbols
                    ],value='BTC')
        ],style={'width': '20%', 'display': 'inline-block'}),
    
        app.scripts.append_script({
            "external_url": my_js_url
        }),
        
        html.Div(
        [
            html.Div(id='my-table',style={'width': '40%', 'display': 'inline-block'}),
            html.Div(
                [
                    dcc.Tabs(id="tabs-history", value='tab-history', children=[
                    dcc.Tab(label='24 hours trend', value='tab-24-hours',style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='1 month trend', value='tab-1-month',style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='1 year trend', value='tab-1-year',style=tab_style, selected_style=tab_selected_style),
                    ],style=tabs_styles),
                    dcc.Graph(id='trend-chart')
                ],style={'width': '40%', 'display': 'inline-block','float':'right'})
    
        ]),
        dcc.Interval(
                    id='interval-component',
                    interval=10*1000, # in milliseconds
                    n_intervals=0
                )
]

)

@app.callback(Output('my-table', 'children'), [Input('symbol', 'value'),Input('interval-component', 'n_intervals')])
def table_update(selected_dropdown_value,n):
    df1 = getRealtimeData(selected_dropdown_value)
    return generate_table(df1)

@app.callback(Output('trend-chart', 'figure'),
              [Input('tabs-history', 'value'),Input('symbol', 'value')])
def graph_update(tab,selected_dropdown_value):
    if tab == 'tab-24-hours':
        df = getHistoricalData(selected_dropdown_value,'day')
    elif tab == 'tab-1-month':
        df = getHistoricalData(selected_dropdown_value,'month')
    elif tab == 'tab-1-year':
        df = getHistoricalData(selected_dropdown_value,'year')
    return {'data': [go.Scatter(x=df['time'],
                                    y=df['close'],
                                    mode='lines+markers')
                            ]
                }
    

if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
    

