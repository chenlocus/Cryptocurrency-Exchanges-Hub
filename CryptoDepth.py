#!/usr/bin/env python
# coding: utf-8

# In[ ]:



# coding: utf-8


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import pandas as pd
import os
import requests
from gevent.pywsgi import WSGIServer
import exchanges
import historicaldata as hisdata
from multiprocessing.pool import ThreadPool
import pkgutil

exchange_list = []
prefix = exchanges.__name__ + "."
for importer, modname, ispkg in pkgutil.iter_modules(exchanges.__path__,prefix):
    print ("Found submodule %s (is a package: %s)"% (modname, ispkg))
    module = __import__(modname, fromlist="exchanges")
    exchange_list.append(module)
    

symbols = {'BTC':'Bitcoin','ETH':'Ethereum','BCH':'Bitcoin Cash','LTC':'Litecoin',
           'EOS':'EOS','XRP':'Ripple','STEEM':'Steem','HIVE':'Hive','BSV':'Bitcoin SV','TRX':'TRON',
           'ADA':'Cardano','MIOTA':'IOTA','XMR':'Monero','BNB':'Binance Coin',
           'DASH':'Dash','XEM':'NEM','ETC':'Ethereum Classic','NEO':'NEO','WAVES':'Waves','ZEC':'Zcash'}

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
    for exchange in exchange_list:
        print(exchange)
        results.append(pool.apply_async(exchange.getUSDPrice, args = (symbol,)))

    price_list = [r.get() for r in results if r is not None and r.get() is not None]
    pool.close()
    pool.join()

    if not price_list:
        return None
    
    df = pd.DataFrame(price_list)
    print(df)
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
app.title = 'Cryptocurrency Exchanges Depth'

app.layout = html.Div(
[  

        html.Div(
        className="app-header",
        children=[
            html.Div('Cryptocurrency Exchanges Depth', className="app-header--title")
        ]
        ),

        html.Div(
        [
                html.Label('Symbol'),
                dcc.Dropdown(
                    id='symbol',
                    options=[
                        {'label': symbol+' '+name, 'value': symbol} for symbol,name in symbols.items()
                    ],value='BTC')
        ],style={'width': '20%', 'display': 'inline-block'}),
        
        html.Div(
        [
            html.Div(id='my-table',style={'width': '40%', 'display': 'inline-block'}),
            html.Div(
                [
                    dcc.Tabs(id="tabs-history", value='tab-history', children=[
                    dcc.Tab(label='24 hours trend', value='tab-24-hours',style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='1 month trend', value='tab-1-month',style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='3 month trend', value='tab-3-month',style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='1 year trend', value='tab-1-year',style=tab_style, selected_style=tab_selected_style),
                    ],style=tabs_styles),
                    dcc.Graph(id='trend-chart')
                ],style={'width': '40%', 'display': 'inline-block','float':'right'})
    
        ]),
        dcc.Interval(
                    id='interval-component',
                    interval=10*1000, # in milliseconds
                    n_intervals=0
                ),
        html.Div (  
               className="footer",
               children=[
                html.Div([
                    html.P('engineerman.club'),
                    html.P('2018 copyright'),
                ], style={'width': '49%', 'display': 'table-cell','vertical-align': 'middle'}),
                html.Div([
                    html.P('Donation'),
                    html.P('XBT： 3NCc5DXMBzSnaZgc97E6MKtwUf52HgFArK        '),
                    html.P('ETH： 0x0058501228fa553aa1aba12baf9f7c46b3822fef'),
                    html.P('LTC： MGDVgCeMRFWkDYyAki3Mm3WX4Pdp7D3kbe        ')
                ], style= {'width': '49%', 'display': 'table-cell'})
               ]
        ),
]

)

@app.callback(Output('my-table', 'children'), [Input('symbol', 'value'),Input('interval-component', 'n_intervals')])
def table_update(selected_dropdown_value,n):
    df1 = getRealtimeData(selected_dropdown_value)
    return generate_table(df1)

@app.callback(Output('trend-chart', 'figure'),
              [Input('tabs-history', 'value'),Input('symbol', 'value')])
def graph_update(tab,selected_dropdown_value):
    df = None
    if tab == 'tab-24-hours':
        df = getHistoricalData(selected_dropdown_value,'day')
    elif tab == 'tab-1-month':
        df = getHistoricalData(selected_dropdown_value,'month')
    elif tab == 'tab-3-month':
        df = getHistoricalData(selected_dropdown_value,'3 months')
    elif tab == 'tab-1-year':
        df = getHistoricalData(selected_dropdown_value,'year')
    #if df is not None:
    print("begin to draw")
    return {'data': [go.Scatter(x=df['time'],
                                    y=df['close'],
                                    mode='lines+markers')
                            ]
                }
    

if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()




