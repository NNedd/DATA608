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
    html.H1(children='DATA 608 Project 4 - Question 1'),
    
    html.H4(children='Submitted by N. Nedd'),
    html.Br(),
    html.Br(),
    
    html.P('''
           You’re a civic hacker and kayak enthusiast who just came across this dataset. You’d like to
           create an app that recommends launch sites to users. Ideally an app like this will use live
           data to give current recommendations, but you’re still in the testing phase. Create a
           prototype that allows a user to pick a date, and will give its recommendations for that
           particular date.
           '''),
     
    html.Br(),
    html.H5(children='Select Date'),

    dcc.DatePickerSingle(
            id='filter-date',
            date=maxDate
    ),
    
    html.Br(),
    
    html.H3('The recommendations are as follows:'),
    dcc.Graph(id='display-recommendation'),
    
    html.P('''
           Please note that the recommendations are in order from most recommended to least recommended.  
           These were selected by them having at most 30 Enterococcus/100 mL)
    '''),
    
    html.Br(),
    
    dcc.Graph(id='river-data-table'),
    
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
    dash.dependencies.Output('river-data-table', 'figure'),
    [dash.dependencies.Input('filter-date', 'date')])


def update_figure(selected_date):
    riverDataFilter = riverData[riverData.Date == selected_date]
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
                'title': 'River Data Table filtered by selected date'
            }
        }

@app.callback(
    dash.dependencies.Output('display-recommendation', 'figure'),
    [dash.dependencies.Input('filter-date', 'date')])

def update_figure_recommendations(selected_date):
    riverDataSelected = riverData[riverData.Date == selected_date]
    riverDataSelected = riverDataSelected[riverDataSelected.EnteroCount <=30]
    riverDataSelected = riverDataSelected.sort_values('EnteroCount')
    return {
        'data': [
                go.Table(
                        header=dict(values=['Site', 'EnteroCount'],
                                    fill = dict(color='#C2D4FF'),
                                    align = ['left'] * 5),
                        cells=dict(values=[riverDataSelected.Site,  
                                           riverDataSelected.EnteroCount],
                                   fill = dict(color='#F5F8FF'),
                                   align = ['left'] * 5))
            ],
            'layout': {
                'title': 'Recommendations'
            }
        }
    
    

app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

if __name__ == '__main__':
    app.run_server(debug=False)
