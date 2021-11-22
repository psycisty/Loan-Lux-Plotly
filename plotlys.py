# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import dash

from dash import html as html
from dash import dcc as dcc
import pandas as pd
pd.options.mode.chained_assignment = None

app = dash.Dash()


df = pd.read_csv('https://raw.githubusercontent.com/psycisty/Loan-Lux-Plotly/main/LuxuryLoanPortfolio.csv')

df2 = df[['loan_id','funded_amount','funded_date','duration years','duration months','10 yr treasury index date funded'
    ,'interest rate','interest rate percent','payments','total past payments','loan balance','property value','purpose','title','employment length',
    'TOTAL UNITS','BUILDING CLASS CATEGORY','BUILDING CLASS AT PRESENT','TAX CLASS AT TIME OF SALE']]

df2['funded_date'] = pd.to_datetime(df2['funded_date'])
df2['year_month'] = df2['funded_date'].dt.strftime('%Y-%m')

df_l = df2.groupby('year_month').agg({'funded_amount':'sum'})
df_l.reset_index(inplace = True)

df_ltv = df2[['funded_date','property value','funded_amount','purpose']]
df_ltv['ltv'] = df2['funded_amount'] / df2['property value']
df_ltv['year_month'] = df_ltv['funded_date'].dt.strftime('%Y-%m')
df_ltv = df_ltv.sort_values(by="year_month")
df_ltv_avg = df_ltv.groupby('year_month').agg({'ltv':'mean'}).reset_index()

df2['lc'] = (df2['payments']*12)/df2['funded_amount']
df_lc = df2.groupby('year_month').agg({'lc':'mean'}).reset_index()

app.layout = html.Div(children =[html.H1(children = 'Business Metrics'),
                                 html.Div(children = ''''Monthly Funded'''),
                                          dcc.Graph(id='monthly_funded',
                                          figure = {'data' : [{'x' : df_l['year_month'],
                                                               'y':df_l['funded_amount'],
                                                               'type' : 'line',
                                                               'name' : 'Funded'
                                                              }],
                                                    'layout':{'title':'Monthly Funding', 
                                                              'yaxis': {'title': 'amount'},
                                                              'xaxis': {"title": 'date(month)'}}
                                                    }
                                          ),
                                          
                                          dcc.Graph(id='ltv_funded',
                                          figure = {'data' : [{'x' : df_ltv_avg['year_month'],
                                                               'y':df_ltv_avg['ltv']*100,
                                                               'type' : 'line',
                                                               'name' : 'LTV'
                                                              }],
                                                    'layout':{'title':'LTV by Month', 
                                                              'yaxis': {'title': 'percent'},
                                                              'xaxis': {"title": 'date (month)'}}
                                                    }
                                          ),
                                          
                                          dcc.Graph(id='cap_rate',
                                          figure = {'data' : [{'x' : df_lc['year_month'],
                                                               'y':df_lc['lc']*100,
                                                               'type' : 'line',
                                                               'name' : 'Loan Constant'
                                                              }],
                                                    'layout':{'title':'Loan Constant by Month', 
                                                              'yaxis': {'title': 'percent'},
                                                              'xaxis': {"title": 'date (month)'}}
                                                    }
                                          ),
                                          
                                          ])
                                          
if __name__ == '__main__':
    app.run_server(debug= True)