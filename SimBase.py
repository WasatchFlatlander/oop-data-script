
class DataField(object):
    name = ""
    inputFields = []
    def __init__(self,name,inputFields):
        self.name = name
        self.inputFields = inputFields
        print('Init Field: ' + str(self.name))
    def isFieldDefined(self,definedFieldNames):
        for field in definedFieldNames:
            if field == self.name: return True
        return False

def isFieldDefined(fieldName,definedFieldNames):
    for defField in definedFieldNames:
        if defField == fieldName: return True
    return False   

class ConditionParameter(object):
    name = ""
    inputFields = []
    def __init__(self,name,inputFields):
            self.name = name
            self.inputFields = inputFields

def initInputFields(data,inputFields):
    modData = data
    for field in inputFields:
        definedFields = data.columns
        if not isFieldDefined(field.name,definedFields):
            modData = initInputFields(modData,field.inputFields)
            print(field.name + ' Created')
            modData = field.createField(modData)
    return modData

def initializeDataFields(data,inputs):
    for inpt in inputs:
        data = initInputFields(data,inpt.inputFields)
        data = inpt.createField(data)
    return data
