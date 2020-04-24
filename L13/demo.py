# -*- coding: utf-8 -*-
# @File  : demo.py
# @Author: LVFANGFANG
# @Date  : 2020/4/23 9:28
# @Desc  :

import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output

df = pd.read_csv('data/data.csv')

app = dash.Dash()
auth = dash_auth.BasicAuth(
    app,
    [('guest', '******')]
)

app.layout = html.Div([
    html.H1('全国各城区房价走势'),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='my-dropdown',
                options=[
                    {'label': x, 'value': x} for x in df['province'].unique()
                ],
                value='北京'
            )],
            style={'width': '49%', 'display': 'inline-block'}
        ),
        html.Div([
            dcc.Dropdown(
                id='my-dropdown2',
                options=[
                    {'label': x, 'value': x} for x in df['province'].unique()
                ],
                value='北京'
            )],
            style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
    ]),

    html.Div([dcc.Graph(id='my-graph')])

])


@app.callback(Output('my-dropdown2', 'options'), [Input('my-dropdown', 'value')])
def update_choice(selected_dropdown_value):
    citys = df[df['province'] == selected_dropdown_value]['city'].unique()
    options = [{'label': x, 'value': x} for x in citys]
    return options


@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown2', 'value')])
def update_graph(selected_dropdown_value):
    data = df[df["city"] == selected_dropdown_value]

    return {
        'data': [
            dict(x=data["date"],
                 y=data["price"],
                 mode='lines',
                 opacity=1,
                 name='实际价格',
                 textposition='bottom center'),
            dict(x=data.iloc[6:]["date"],
                 y=data.iloc[6:]["forecast"],
                 mode="lines+markers",
                 opacity=0.5,
                 # line={
                 #     "color": "#385965",
                 #     "width": 1.5
                 # },
                 name='预测价格',
                 textposition='bottom center')
        ],
        'layout': dict(
            height=600,
            title=f"{selected_dropdown_value}房价走势及预测",
            xaxis={"title": "Date",
                   'rangeselector': {
                       'buttons': list([{'count': 1, 'label': '1M', 'step': 'month', 'stepmode': 'backward'},
                                        {'count': 6, 'label': '6M', 'step': 'month', 'stepmode': 'backward'},
                                        {'count': 1, 'label': 'YTD', 'step': 'year', 'stepmode': 'todate'},
                                        {'count': 1, 'label': '1Y', 'step': 'year', 'stepmode': 'backward'},
                                        {'step': 'all'}])},
                   # 'rangeslider': {'visible': True},
                   'type': 'date'},
            yaxis={"title": "Price"}
        )
    }


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8051)
