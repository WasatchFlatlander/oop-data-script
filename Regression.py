import SimBase
import pandas as pd
import numpy as np
import statsmodels.api as sm
import InputFields as ifld


class Regression(object):
    name = ''
    regFieldSuffix = ''
    length = 10
    inputField = ifld.AdjClose()
    regFunctionDict = {}
    regFields = {}

    def __init__(self,length,inputField,name=''):
        self.length = length
        self.inputField = inputField
        self.name = ''
        self.regFields={}
        if len(name)==0:
            self.name = 'Reg_'+str(self.length) + '_' + self.inputField.name
        else:
            self.name = name
        self.fieldSuffix = str(self.length) + '_' + self.inputField.name
        self.regFuncDict = {'Reg_Fit_' + self.fieldSuffix:lambda x:x.fittedvalues[-1],
                           'Reg_SE_' + self.fieldSuffix:lambda x:x.scale,
                           'Reg_Slope_' + self.fieldSuffix:lambda x:x.params[1],
                           'Reg_RSquared_' + self.fieldSuffix:lambda x:x.rsquared}
        for key in self.regFuncDict:
            print('Adding RegField: ' + key)
            self.regFields[key] = ifld.BaseField(key)
            
    def getRegFields(self):
        return self.regFields
        
    def getRegFieldsList(self):
        return list(self.regFields.values())

    def getReg(self,yValues,regFunctionDict,regDataDict):
        regLen = len(yValues)
        xValues = np.asarray(range(0,regLen))
        xValues = sm.add_constant(xValues)
        model = sm.OLS(yValues,xValues).fit()
        for key in regFunctionDict:
            regDataDict[key].append(regFunctionDict[key](model))
        return 0

    def createRollingReg(self,data):
        regDataDict = {}
        for key in self.regFuncDict:
            data.loc[:,key] = np.NAN
            regDataDict[key] = []
        data[self.inputField.name].rolling(window=self.length,center=False).apply(func=lambda x:self.getReg(x,self.regFuncDict,regDataDict))
        for key in regDataDict:
            dataLen = len(regDataDict[key])
            if dataLen > 0:
                data.loc[(self.length-1):(self.length-1 + dataLen),key] = regDataDict[key]
        return data
    
def initializeRegData(data,linRegressions):
    dataFrames = []
    counter = 1
    totalSymbols = len(data.index.get_level_values('Symbol').unique())
    for symbol in data.index.get_level_values('Symbol').unique():
        symbolData = data.loc[data.index.isin([symbol], level='Symbol')].copy()
        symbolData.sort_index(axis=0,level='Date',ascending=True,inplace=True)  
        for reg in linRegressions:
            reg.createRollingReg(symbolData)
        symbolData = symbolData.dropna()    
        dataFrames.append(symbolData)
        print('FINISHED REG LOAD ' + symbol + " " + str(counter) + "/" + str(totalSymbols))
        counter += 1
    combinedData = pd.concat(dataFrames)
    combinedData.sort_index(axis=0,level='Date',ascending=True,inplace=True)
    return combinedData   
        
#testData = pd.DataFrame(allData['Adj_Close'][1:100])
#myReg = Regression(10,ifld.AdjClose())
#myReg.createRollingReg(testData)
