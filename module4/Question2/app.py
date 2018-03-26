# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 01:53:53 2018

@author: niki
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime as dt
from scipy import stats


riverData = pd.read_csv('https://raw.githubusercontent.com/NNedd/DATA608/master/module4/Data/riverkeeper_data_2013.csv', parse_dates=['Date'])
riverData['Date']=riverData['Date'].dt.strftime('%Y-%m-%d')
maxDate = max(riverData['Date'])

# Data Cleaning  Attempt
# It is noticed that some values in the EnteroCount column have non numeric values.  In particular the following values are non-numeric:
# >2420, <1, <10, >24196.  The less than/more than sign will be removed from these values for better analysis.

riverData['EnteroCount'] = riverData['EnteroCount'].replace(['>2420'], '2420')
riverData['EnteroCount'] = riverData['EnteroCount'].replace(['>24196'], '24196')
riverData['EnteroCount'] = riverData['EnteroCount'].replace(['<1'], '1')
riverData['EnteroCount'] = riverData['EnteroCount'].replace(['<10'], '10')

riverData['EnteroCount']  = pd.to_numeric(riverData['EnteroCount'])


app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='DATA 608 Project 4 - Question 2'),
    
    html.H4(children='Submitted by N. Nedd'),
    
    html.P('''
           This time you are building an app for scientists. You’re a public health researcher analyzing
           this data. You would like to know if there’s a relationship between the amount of rain and
           water quality. Create an exploratory app that allows other researchers to pick different sites
           and compare this relationship.
    '''),
           
    html.Br(),
    html.Br(),
    
    html.H3(children='Select site for comparison'),
    
    dcc.Dropdown(id='dropdown', options=[
        {'label': i, 'value': i} for i in riverData.Site.unique()
    ], placeholder='Filter by Site...'),
    
    html.Br(),
    
            
    #dcc.Graph(id='Site-Data'),
    
    html.Br(),
    
    dcc.Graph(id='river-data-site-table'),
    
    html.H3(children='Scatter Graph of Four Day Rain Total vs. EnteroCount for Selected Site'),
    
    dcc.Graph(id='river-data-site-graph'),
    
    html.H3(children='Scatter Graph of Four Day Rain Total vs. EnteroCount for Selected Site (logged values)'),
    
    dcc.Graph(id='river-data-site-graph-logs'),
    
    html.Div(id='correlation'),
    
    dcc.Graph(
        id='river-data-table2',
        figure={
            'data': [
                go.Table(
                        header=dict(values=riverData.columns,
                                    fill = dict(color='#C2D4FF'),
                                    align = ['left'] * 5),
                        cells=dict(values=[riverData.Site, riverData.Date, riverData.EnteroCount, riverData.FourDayRainTotal, riverData.SampleCount],
                                   fill = dict(color='#F5F8FF'),
                                   align = ['left'] * 5))
            ],
            'layout': {
                'title': 'All River Data Table'
            }
        }
    )
])


@app.callback(
    dash.dependencies.Output('river-data-site-table', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')])


def update_figure_table(dropdown_value):
    riverDataFilter = riverData[riverData.Site == dropdown_value]
    return {
        'data': [
                go.Table(
                        header=dict(values=riverDataFilter.columns,
                                    fill = dict(color='#C2D4FF'),
                                    align = ['left'] * 5),
                        cells=dict(values=[riverDataFilter.Site, 
                                           riverDataFilter.Date, 
                                           riverDataFilter.EnteroCount, 
                                           riverDataFilter.FourDayRainTotal, 
                                           riverDataFilter.SampleCount],
                                   fill = dict(color='#F5F8FF'),
                                   align = ['left'] * 5))
            ],
            'layout': {
                'title': 'River Data Table filtered by selected site'
            }
        }

@app.callback(
    dash.dependencies.Output('river-data-site-graph', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')])

def update_figure_graph(dropdown_value):
    riverDataFilter = riverData[riverData.Site == dropdown_value]
      
    return {
        'data': [
                go.Scatter(
                    x=riverDataFilter['EnteroCount'],
                    y=riverDataFilter['FourDayRainTotal'],
                    mode='markers',
                    marker={
                        'size': 15,
                        'opacity': 0.5,
                        'line' :{'width':0.5, 'color': 'white'}
                    }
            )],
            'layout': 
                go.Layout(
                    xaxis ={
                        'title': 'EnteroCount'
                    },
                    yaxis = {
                        'title': 'Four Day Rain Total',
                    }
                )
        }
                
@app.callback(
    dash.dependencies.Output('river-data-site-graph-logs', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')])

def update_figure_logs(dropdown_value):
    riverDataFilter = riverData[riverData.Site == dropdown_value]
    

    return {
        'data': [
                go.Scatter(
                    x=riverDataFilter['EnteroCount'],
                    y=riverDataFilter['FourDayRainTotal'],
                    mode='markers',
                    marker={
                        'size': 15,
                        'opacity': 0.5,
                        'line' :{'width':0.5, 'color': 'white'}
                    }
            )],
            'layout': 
                go.Layout(
                    xaxis ={
                        'title': 'EnteroCount',
                        'type': 'log'
                    },
                    yaxis = {
                        'title': 'Four Day Rain Total',
                    }
                )
        }

@app.callback(
    dash.dependencies.Output('correlation', 'children'),
    [dash.dependencies.Input('dropdown', 'value')])

def set_correlation_value (dropdown_value):
    riverDataFilter = riverData[riverData.Site == dropdown_value]
    return 'The correlation between EnteroCount and Four Day Rain Total for the site named {} is {}'.format(
            dropdown_value, riverDataFilter['EnteroCount'].corr(riverDataFilter['FourDayRainTotal'])
            )
#def update_figure(selected_date):
#    riverDataSelected = riverData[riverData.Date == selected_date]
#    riverDataSelected = riverDataSelected[riverDataSelected.EnteroCount <=30]
#    return {
#        'data': [
#                go.Table(
#                        header=dict(values=['Site', 'EnteroCount'],
#                                    fill = dict(color='#C2D4FF'),
#                                    align = ['left'] * 5),
#                        cells=dict(values=[riverDataSelected.Site,  
#                                           riverDataSelected.EnteroCount],
#                                   fill = dict(color='#F5F8FF'),
#                                   align = ['left'] * 5))
#            ],
#            'layout': {
#                'title': 'Recommendations'
#            }
#        }
#    
    

app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

if __name__ == '__main__':
    app.run_server(debug=False)
