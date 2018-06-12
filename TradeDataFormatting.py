import pandas as pd
import numpy as np

def formatDataFrame(data):    
    data.sort_index(inplace=True,ascending=True)
    data['Adj_Close'] = pd.to_numeric(data['Adj_Close'])
    data['Close'] = pd.to_numeric(data['Close'])
    data['High'] = pd.to_numeric(data['High'])
    data['Low'] = pd.to_numeric(data['Low'])
    data['Open'] = pd.to_numeric(data['Open'])
    data['Volume'] = pd.to_numeric(data['Volume'])
    data['Adj_Open'] = data['Open'] * data['Adj_Close'] / data['Close']
    data['Adj_High'] = data['High'] * data['Adj_Close'] / data['Close']
    data['Adj_Low'] = data['Low'] * data['Adj_Close'] / data['Close']
    data['Adj_Volume'] = data['Volume'] * data['Close'] / data['Adj_Close']

    return data
