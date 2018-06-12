## DataCollection.py
import sys
import pandas as pd
import numpy as np
import yahoo_finance
import TradeDataFormatting
import SimBase

def download_base_data(symbols,startDate,endDate):
    dataFrames = []
    counter = 1
    for symbol in symbols:
        print('LOADING DATA FOR ' + symbol)
        print('Finished ' + str(counter) + ' out of ' + str(len(symbols)))
        counter += 1
        try:
            shareInfo = yahoo_finance.Share(symbol)
            print('MadeIt1')
            rawData = shareInfo.get_historical(startDate,endDate)
            print('MadeIt2')
            pdDf = pd.DataFrame(rawData)
            print('MadeIt3')
            if len(pdDf.axes[0])>0:
                print('MadeIt4')
                pdDf = TradeDataFormatting.formatDataFrame(pdDf)
                print('MadeIt5')
                filterCols = ['Date','Symbol','Volume','Close','Open','Low','High','Adj_Volume','Adj_Close','Adj_Open','Adj_Low','Adj_High']
                print('MadeIt6')
                pdDf = pdDf[filterCols]            
                print('MadeIt7')
                dataFrames.append(pdDf)      
        except Exception as e:
           print('LOADING ERROR For ' + symbol + ': ' + str(e))
    combinedData = pd.concat(dataFrames)
    combinedData = combinedData.dropna()
    return combinedData


## given a large composite data frame with multiple symbols, will return a formatted panda data frame with all desired
## collection input fields.
def initializeCollectionFields(data,collectionFields):
    dataFrames = []
    counter = 1
    totalSymbols = len(data.index.get_level_values('Symbol').unique())
    for symbol in data.index.get_level_values('Symbol').unique():
        symbolData = data.loc[data.index.isin([symbol], level='Symbol')].copy()
        symbolData.sort_index(axis=0,level='Date',ascending=True,inplace=True)    
        symbolData = SimBase.initializeDataFields(symbolData,collectionFields)
        symbolData = symbolData.dropna()    
        dataFrames.append(symbolData)
        print('FINISHED LOAD ' + symbol + " " + str(counter) + "/" + str(totalSymbols))
        counter += 1
    combinedData = pd.concat(dataFrames)
    combinedData.sort_index(axis=0,level='Date',ascending=True,inplace=True)
    return combinedData

def attachBenchmarkData(data,benchmarkData,benchmarkPrefix):
    benchmarkData.columns = [str(benchmarkPrefix) + str(col) for col in benchmarkData.columns]        
    data = pd.merge(data, benchmarkData, right_index=True, left_index=True)
    data.sort_index(inplace=True,ascending=True)
    return data
    