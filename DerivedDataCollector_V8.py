import sys
import os
main_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(main_dir)
import pandas as pd
import InputFields as ifld
import DataCollection
import Regression as reg
from datetime import datetime

##### COLLECTION_SETUP_BEGIN #####
collector_version = 'V8'
start_date = '2014-06-11'
end_date = '2016-06-11'
stock_data_file = main_dir + '/stock_data.csv'
output_file = main_dir + '/dd_collector_' + collector_version + '_' + datetime.now().strftime("%Y%m%d-%H%M%S") + '.csv'

##### MAKE FORMATING ADJUSTMENTS #####
print('FORMATTING_DATA_BEGIN')
stock_data = pd.read_csv(stock_data_file,index_col=[0],parse_dates=True)
stock_data.set_index('Symbol',append=True,inplace=True,drop=True)
stock_data.rename(columns={'Adj Close':'Adj_Close'}, inplace=True)
date_filter = (stock_data.index.get_level_values('Date') >= start_date) & (stock_data.index.get_level_values('Date') <= end_date)
stock_data = stock_data.loc[date_filter]
print('FORMATTING_DATA_END')

########DEFINE COLLECTION FIELDS##########
print('DATA_COLLECTION_BEGIN')
inputPeriods = [5,10,20,50,100,200]
pastReturnPeriods = [1,2,5,10,20,50,100]
retPeriods = [1,2,3,4,5,10,20,30,40,50]
adjClose = ifld.AdjClose()
longVolume = ifld.SMA(100,ifld.AdjVolume())
collectionFields = []

#import random
#randomSymbols = random.sample(list(stockData.index.get_level_values('Symbol').unique()),2)
#stockData = stockData[stockData.index.get_level_values('Symbol').isin(randomSymbols)]   

linRegressions = []
for period in inputPeriods:    
    linearReg = reg.Regression(period,adjClose)
    linRegressions.append(linearReg)
    collectionFields.extend(linearReg.getRegFieldsList())
    sdPeriod = ifld.SD(period,ifld.PcntChange(1,False,adjClose),'SD_PCNT_'+str(period))  
    rollingMin = ifld.RollingMin(period,adjClose)
    rollingMax = ifld.RollingMax(period,adjClose)
    minDuration = ifld.ExtremeDuration(period,adjClose,False,'Min_Duration_' + str(period))
    maxDuration = ifld.ExtremeDuration(period,adjClose,True,'Max_Duration_' + str(period))
    minDurationLag = ifld.Lag(minDuration,1,'Min_Duration_' + str(period) + '_Lag')
    maxDurationLag = ifld.Lag(maxDuration,1,'Max_Duration_' + str(period) + '_Lag')
    retracedFromHigh = ifld.Divide(ifld.RetracementPcnt(period,True),sdPeriod,'Ret_High_' + str(period))    
    retracedFromLow = ifld.Divide(ifld.RetracementPcnt(period,False),sdPeriod,'Ret_Low_' + str(period))
    regFit = linearReg.getRegFields()['Reg_Fit_' + str(period) + '_Adj_Close'] 
    regSE = linearReg.getRegFields()['Reg_SE_' + str(period) + '_Adj_Close']
    regSlope = linearReg.getRegFields()['Reg_Slope_' + str(period) + '_Adj_Close']
    regRsquared = linearReg.getRegFields()['Reg_RSquared_' + str(period) + '_Adj_Close']
    regPremiumSE = ifld.Divide(ifld.Diff(adjClose,regFit),regSE,'Reg_Premium_SE_' + str(period))
    regPremiumSD = ifld.Divide(ifld.Divide(ifld.Diff(adjClose,regFit),adjClose),sdPeriod,'Reg_Premium_SD_' + str(period))
    regSlopeSD = ifld.Divide(ifld.Divide(regSlope,ifld.AdjClose()),sdPeriod,'Reg_Slope_SD_' + str(period))    
    retFromHigh = ifld.Divide(ifld.RetracementPcnt(period,True),sdPeriod,'Ret_High_' + str(period))           
    retFromLow = ifld.Divide(ifld.RetracementPcnt(period,False),sdPeriod,'Ret_Low_' + str(period)) 
    sma = ifld.SMA(period,adjClose)    
    smaPremium = ifld.Divide(ifld.Divide(ifld.Diff(adjClose,sma),adjClose),sdPeriod,'SMA_Premium_'+str(period))
    volume = ifld.SMA(period,ifld.AdjVolume())
    normVolume = ifld.Divide(volume,longVolume,'NORM_Volume_' + str(period))
    obv = ifld.OBV(period)
    normObv = ifld.Divide(obv,longVolume,'NORM_OBV_' + str(period))    
    collectionFields.extend( [sdPeriod,minDuration,minDurationLag,maxDuration,maxDurationLag,rollingMin,rollingMax,
                             regRsquared,regSE,regFit,regSlope,regSlopeSD,regPremiumSE,regPremiumSD,
                             sma,smaPremium,
                             retracedFromLow,retracedFromHigh,
                             normVolume, normObv] )

sdPeriod = ifld.SD(20,ifld.PcntChange(1,False,adjClose),'SD_PCNT_20')
for pstRetPeriod in pastReturnPeriods:
    pastReturn = ifld.PcntChange(pstRetPeriod,False,adjClose)
    normRet = ifld.Divide(pastReturn,sdPeriod,'Past_Ret_' + str(pstRetPeriod) + '_NORM')
    collectionFields.append(normRet)

for retPeriod in retPeriods:
    futRetPcnt = ifld.PcntChange(retPeriod,True,ifld.AdjClose(),'Fut_Ret_'+str(retPeriod))
    futNorm = ifld.Divide(futRetPcnt,sdPeriod,'Fut_Ret_' + str(retPeriod) + '_NORM')
    collectionFields.extend([futRetPcnt,futNorm])

stock_data = reg.initializeRegData(stock_data,linRegressions)
stock_data = DataCollection.initializeCollectionFields(stock_data,collectionFields)                    
print('DATA_COLLECTION_END')
########DEFINE COLLECTION FIELDS##########

########LOG_DATA_COLLECTION###############
print('WRITING_OUTPUT')
stock_data.to_csv(output_file)
print('DATA_COLLECTION_FINISHED')
########LOG_DATA_COLLECTION###############
