import SimBase
import pandas as pd
import StaticStrategySettings as CONST
import numpy as np
import statsmodels.api as sm

class BaseField(SimBase.DataField):
    def __init__(self,baseFieldName):
        super().__init__(baseFieldName,[])
    def createField(self,data):
        return data

class Diff(SimBase.DataField):
    def __init__(self,_firstField,_secondField,name=''):
        if len(name)==0:
            fieldName = _firstField.name + '_' + str(_secondField.name) + '_Diff'
        else:
            fieldName = name
        super().__init__(fieldName ,[_firstField,_secondField])
    def createField(self,data):
        data[self.name] = data[self.inputFields[0].name] - data[self.inputFields[1].name]
        return data
        
class Add(SimBase.DataField):
    def __init__(self,_firstField,_secondField,name=''):
        if len(name)==0:
            fieldName = fieldName = _firstField.name + '+' + str(_secondField.name)
        else:
            fieldName = name
        super().__init__(fieldName,[_firstField,_secondField])
    def createField(self,data):
        data[self.name] = data[self.inputFields[0].name] + data[self.inputFields[1].name]
        return data
        
class Multiply(SimBase.DataField):
    def __init__(self,_firstField,_secondField,name = ''):
        if len(name)==0:
            fieldName = _firstField.name + '_' + str(_secondField.name) + '_Multiply' 
        else:
            fieldName = name
        super().__init__(fieldName,[_firstField,_secondField])
    def createField(self,data):
        data[self.name] = data[self.inputFields[0].name] * data[self.inputFields[1].name]
        return data
    
class Divide(SimBase.DataField):
    def __init__(self,_firstField,_secondField,name = ''):
        if len(name)==0:
            fieldName = _firstField.name + '_' + str(_secondField.name) + '_Divide' 
        else:
            fieldName = name
        super().__init__(fieldName,[_firstField,_secondField])
    def createField(self,data):
        data[self.name] = data[self.inputFields[0].name] / data[self.inputFields[1].name]
        return data
        


class NormPrice(SimBase.DataField):
    def __init__(self,inputField):
        super().__init__('NormPrice_' + inputField.name,[inputField,AdjClose()])
    def createField(self,data):
        data[self.name] = data[self.inputFields[0].name] / data[self.inputFields[1].name]
        return data

class NormVol(SimBase.DataField):
    def __init__(self,inputField,name=''):
        fieldName = ''
        if len(name)==0:
            fieldName = 'NormVol_' + inputField.name
        else:
            fieldName = name
        super().__init__(fieldName,[inputField,SD(CONST.NORM_SD_LENGTH,PcntChange(1,False,AdjClose()))])
    def createField(self,data):
        data[self.name] = data[self.inputFields[0].name] / data[self.inputFields[1].name]
        return data

class Norm(SimBase.DataField):
    def __init__(self,inputField,name=''):
        fieldName = ''
        if len(name)==0:
            fieldName = 'Norm_' + inputField.name
        else:
            fieldName = name
        super().__init__(fieldName,[inputField,SD(CONST.NORM_SD_LENGTH,inputField)])
    def createField(self,data):
        data[self.name] = data[self.inputFields[0].name] / data[self.inputFields[1].name]
        return data

class Lag(SimBase.DataField):
    lagLength = 10
    def __init__(self,_inputField,_lagLength,name=''):
        fieldName = ''
        if len(name)==0:
            fieldName = _inputField.name + '_Lag_' + str(_lagLength)
        else:
            fieldName = name
        super().__init__(fieldName,[_inputField])
        self.lagLength = _lagLength
    def createField(self,data):
        data[self.name] = data[self.inputFields[0].name].shift(self.lagLength)
        return data

class Rank(SimBase.DataField):
    def __init__(self,inputField,name=''):
        fieldName = ''
        if len(name)==0:
            fieldName = inputField.name + '_RANK'
        else:
            fieldName = name
        super().__init__(fieldName,[inputField])
    def createField(self,data):
        data.loc[:,self.name] = data.groupby(level = 'Date')[self.inputFields[0].name].rank(ascending=True)
        return data

class PcntChange(SimBase.DataField):
    changePeriod = 10
    isFuture = True
    def __init__(self,changePeriod,isFuture,inputField,name=''):
        fieldName = ''
        if len(name)==0:
            futureOrPast = 'FUT' if isFuture else 'PAST'
            fieldName = 'PcntChange_' + str(futureOrPast) + '_' +str(changePeriod)
        else:
            fieldName = name
        super().__init__(fieldName,[inputField])
        self.changePeriod = changePeriod
        self.isFuture = isFuture
    def createField(self,data):
        if self.isFuture:
            data[self.name] = data[self.inputFields[0].name].shift(-self.changePeriod).pct_change(self.changePeriod)
        else:
            data[self.name] = data[self.inputFields[0].name].pct_change(self.changePeriod)
        return data

## Returns rolling max of a given input field over a given length of time.
class RollingMax(SimBase.DataField):
    length = 10
    def __init__(self,length,inputField,name=''):
        fieldName = ''
        if len(name)==0:
            fieldName = 'RollingMax_'+str(length) + '_' + inputField.name
        else:
            fieldName = name
        super().__init__(fieldName,[inputField])
        self.length = length
    def createField(self,data):
        data.loc[:,self.name] = data[self.inputFields[0].name].rolling(window=self.length,center=False).max()
        return data

## Returns rolling min of a given input field over a given length of time.
class RollingMin(SimBase.DataField):
    length = 10
    def __init__(self,length,inputField,name=''):
        fieldName = ''
        if len(name)==0:
            fieldName = 'RollingMin_'+str(length) + '_' + inputField.name
        else:
            fieldName = name
        super().__init__(fieldName,[inputField])
        self.length = length
    def createField(self,data):
        data.loc[:,self.name] = data[self.inputFields[0].name].rolling(window=self.length,center=False).min()
        return data

class Duration(SimBase.DataField):
    length = 10
    def __init__(self,length,inputField,name=''):
        fieldName = ''
        if len(name)==0:
            fieldName = 'Duration_'+str(length)+ '_' + inputField.name
        else:
            fieldName = name
        super().__init__(fieldName,[inputField])
        self.length = length
    def createField(self,data):
        ## every time it changes, data resets min value is 1
        data.loc[:,self.name] = 0
        duration = 1 
        numRows = len(data[self.inputFields[0].name])
        inputFldCol = data.columns.get_loc(self.inputFields[0].name)
        fldCol = data.columns.get_loc(self.name)
        prevVal = data.iat[0,inputFldCol]
        for i in range(0,numRows):
            curVal = data.iat[i,inputFldCol]
            if curVal == prevVal:        
                data.iat[i, fldCol] = duration
            else:
                duration = 1
                prevVal = curVal
                data.iat[i,fldCol] = duration
            duration += 1
            if duration > self.length:
                duration = 1
                prevVal = curVal
        return data

class ExtremeDuration(SimBase.DataField):
    length = 10
    isMax = True
    def __init__(self,length,inputField,isMax,name=''):
        fieldName = ''
        if len(name)==0:
            extrema = 'Max' if isMax else 'Min'
            fieldName = extrema + '_Duration_' + str(length) + '_' + inputField.name
        else:
            fieldName = name
        super().__init__(fieldName,[inputField])
        self.length = length
        self.isMax = isMax
    def createField(self,data):
        if self.isMax:
            data.loc[:,self.name] = data[self.inputFields[0].name].rolling(window=self.length,center=False).apply(func=lambda x:self.length-1-np.argmax(x))
        else:
            data.loc[:,self.name] = data[self.inputFields[0].name].rolling(window=self.length,center=False).apply(func=lambda x:self.length-1-np.argmin(x))            
        return data
        
## Returns simple moving average of a given input field
class SMA(SimBase.DataField):
    length = 10
    def __init__(self,length,inputField,name=''):
        fieldName = ''
        if len(name)==0:
            fieldName = 'SMA_'+str(length) + '_' + inputField.name
        else:
            fieldName = name
        super().__init__(fieldName,[inputField])
        self.length = length
    def createField(self,data):
        data[self.name] = data[self.inputFields[0].name].rolling(window=self.length,center=False).mean()
        return data


## Returns SD of a given input field over a given period length
class SD(SimBase.DataField):
    length = 10
    def __init__(self,length,inputField,name=''):
        fieldName = ''
        if len(name)==0:
            fieldName = 'SD_'+str(length) + '_' + inputField.name
        else:
            fieldName = name
        super().__init__(fieldName,[inputField])
        self.length = length
    def createField(self,data):
        data[self.name] = data[self.inputFields[0].name].rolling(window=self.length,center=False).std()
        return data


## Returns the Pcnt Difference between the closing price and the rolling high/low.
class RetracementPcnt(SimBase.DataField):
    length = 10
    isRetracedFromHigh = True
    def __init__(self,length,isRetracedFromHigh,name=''):
        fieldName = ''
        if len(name)==0:
            fieldName = 'RetPcnt_'+str(isRetracedFromHigh)+'_' + str(length)
        else:
            fieldName = name
        if(isRetracedFromHigh):
            super().__init__(fieldName,[AdjClose(),RollingMax(length,AdjClose())])
        else:
            super().__init__(fieldName,[AdjClose(),RollingMin(length,AdjClose())])
        self.length = length
        self.isRetracedFromHigh = isRetracedFromHigh
    def createField(self,data):
        if(self.isRetracedFromHigh):
            data[self.name] = (data[self.inputFields[1].name] - data[self.inputFields[0].name]) / data[self.inputFields[0].name]
        else:
            data[self.name] = (data[self.inputFields[0].name] - data[self.inputFields[1].name]) / data[self.inputFields[0].name]
        return data

class Close(SimBase.DataField):
    def __init__(self):
        super().__init__('Close',[])
    def createField(self,data):
        return data

class Open(SimBase.DataField):
    def __init__(self):
        super().__init__('Open',[])
    def createField(self,data):
        return data

class Low(SimBase.DataField):
    def __init__(self):
        super().__init__('Low',[])
    def createField(self,data):
        return data
        
class High(SimBase.DataField):
    def __init__(self):
        super().__init__('High',[])
    def createField(self,data):
        return data
        
class AdjClose(SimBase.DataField):
    def __init__(self):
        super().__init__('Adj_Close',[])
    def createField(self,data):
        return data

class Volume(SimBase.DataField):
    def __init__(self):
        super().__init__('Volume',[])
    def createField(self,data):
        return data

class AdjScalar(SimBase.DataField):
    def __init__(self):
        super().__init__('Adj_Scalar',[AdjClose(),Close()])
    def createField(self,data):
        data[self.name] = data[self.inputFields[0].name] / data[self.inputFields[1].name]
        return data 
    
class AdjOpen(SimBase.DataField):
    def __init__(self):
        super().__init__('Adj_Open',[Open(),AdjScalar()])
    def createField(self,data):
        data[self.name] = data[self.inputFields[0]] * data[self.inputFields[1]]
        return data

class AdjHigh(SimBase.DataField):
    def __init__(self):
        super().__init__('Adj_High',[High(),AdjScalar()])
    def createField(self,data):
        data.loc[:,self.name] = data[self.inputFields[0]] * data[self.inputFields[1]]
        return data
        
class AdjLow(SimBase.DataField):
    def __init__(self):
        super().__init__('Adj_Low',[Low(),AdjScalar()])
    def createField(self,data):
        data[self.name] = data[self.inputFields[0]] * data[self.inputFields[1]]
        return data

class AdjVolume(SimBase.DataField):
    def __init__(self):
        super().__init__('Adj_Volume',[Volume(),AdjScalar()])
    def createField(self,data):
        data[self.name] = data[self.inputFields[0].name] / data[self.inputFields[1].name]
        return data

class DollarVolume(SimBase.DataField):
    def __init__(self):
        super().__init__('Dolarized_Volume',[AdjClose(),Volume()])
    def createField(self,data):
        data[self.name] = data[self.inputFields[0].name] * data[self.inputFields[1].name]
        return data

class RollingMovement(SimBase.DataField):
    length = 10
    isUpMovement=True
    def __init__(self,length,isUpMovement,name=''):
        fieldName = ''
        if len(name)==0:
            fieldName = 'RollingMovement_' + str(isUpMovement) + '_' + str(length)
        else:
            fieldName = name
        self.length = length
        self.isUpMovement = isUpMovement
        super().__init__(fieldName,[PcntChange(1),SD(CONST.NORM_SD_LENGTH)])
    def createField(self,data):
        direction = data[self.inputFields[0].name]
        if self.isUpMovement:
            direction = direction[direction > 0]
        else:
            direction = -direction[direction > 0]
        movement = direction * data[self.inputFields[0].name] / data[self.inputFields[1].name]
        movement.rolling(window=self.length,center=False).sum()            
        data[self.name] = data[self.inputFields[0].name] * data[self.inputFields[1].name]
        return data                         

class OBV(SimBase.DataField):
    length = 10    
    def __init__(self,length,name=''):
        fieldName = ''
        if len(name)==0:
            fieldName = 'OBV_'+str(length)
        else:
            fieldName = name
        super().__init__(fieldName,[PcntChange(1,False,AdjClose()),AdjVolume()])
        self.length = length
    def createField(self,data):
        upShock = data[self.inputFields[0].name] > 0
        downShock = data[self.inputFields[0].name] <= 0
        adjVolume = data[self.inputFields[1].name]
        obv = upShock*adjVolume - downShock*adjVolume
        data[self.name] = obv.rolling(window=self.length,center=False).sum()
        return data

##class OBV_V2(SimBase.DataField):
##    length = 10
##    def __init__(self,length):
    ##        self.length = length
##        super().__init__('OBV_V2'+str(length),inputFields[PcntChange(1),Volume(),AdjClose(),AdjOpen(),AdjHigh(),AdjLow()])
##    def createField(self,data):
##        direction = data[inputFields[0].name]
##        direction[direction > 0] = direction[direction > 0]
##        direction[direction < 0] = -direction[direction < 0]
##        volume = data[inputFields[1].name]
##        obv = direction*volume*max(open,high+low / 2
##                                Penalize for Ending on the lows. Also Penalize for Never going higher than open
##        data[self.name] = obv.rolling(window=self.length,center=False).sum()
##        return data



## penalize volume that occurs on days with middle of the road finishes   

class RSI(SimBase.DataField):
    length = 14
    def __init__(self,_length):
        super().__init__('RSI_'+to_string(length),[ClosingChng])
        self.length = _length
    def createField(self,data):
        delta = data[self.inputFields[0].name].diff()
        u = delta * 0
        d = u.copy()
        u[delta > 0] = delta[delta > 0]
        d[delta < 0] = -delta[delta < 0]
        u[u.index[period-1]] = np.mean( u[:length] ) #first value is sum of avg gains
        u = u.drop(u.index[:(period-1)])
        d[d.index[period-1]] = np.mean( d[:length] ) #first value is sum of avg losses
        d = d.drop(d.index[:(period-1)])
        rs = pd.stats.moments.ewma(u, com=length-1, adjust=False) / pd.stats.moments.ewma(d, com=length-1, adjust=False)
        rsi = 100 - 100 / (1 + rs)
        data[self.name] = rsi
        return data
    
## What properties Do I want to investigate?
## What Determines good flowx
## RSI = 100 - 100/(1+RS) where RS = Average Up Day Close / Average Down Day Close
