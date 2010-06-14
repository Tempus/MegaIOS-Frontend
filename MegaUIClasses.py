# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui



class QHexSpinBox(QtGui.QDoubleSpinBox):

    class HexValidator(QtGui.QValidator):
        def __init__(self, min, max):
            QtGui.QValidator.__init__(self)
            self.valid = set('0123456789abcdef')
            self.min = min
            self.max = max
        
        def validate(self, input, pos):
            try:
                input = str(input).lower()
            except:
                return (self.Invalid, pos)
            valid = self.valid
            
            for char in input:
                if char not in valid:
                    return (self.Invalid, pos)
            
            value = int(input, 16)
            if value < self.min or value > self.max:
                return (self.Intermediate, pos)
            
            return (self.Acceptable, pos)
    

    class DecValidator(QtGui.QValidator):
        def __init__(self, min, max):
            QtGui.QValidator.__init__(self)
            self.valid = set('0123456789')
            self.min = min
            self.max = max
        
        def validate(self, input, pos):
            try:
                input = str(input).lower()
            except:
                return (self.Invalid, pos)
            valid = self.valid
            
            for char in input:
                if char not in valid:
                    return (self.Invalid, pos)
            
            value = int(input, 10)
            if value < self.min or value > self.max:
                return (self.Intermediate, pos)
            
            return (self.Acceptable, pos)

    
    def __init__(self, padding = 8, format='X', *args):
        self.format = format
        self.padding = padding
        self.mode = 'Hex'
        QtGui.QSpinBox.__init__(self, *args)
        self.validator = self.HexValidator(self.minimum(), self.maximum())
        self.setRange(2147483648, 3556769791)
        self.setDecimals(0)
    
    def setMinimum(self, value):
        self.validator.min = value
        QtGui.QDoubleSpinBox.setMinimum(self, value)
    
    def setMaximum(self, value):
        self.validator.max = value
        QtGui.QDoubleSpinBox.setMaximum(self, value)
    
    def setRange(self, min, max):
        self.validator.min = min
        self.validator.max = max
        QtGui.QDoubleSpinBox.setMinimum(self, min)
        QtGui.QDoubleSpinBox.setMaximum(self, max)
    
    def validate(self, text, pos):
        return self.validator.validate(text, pos)
    
    def textFromValue(self, value):
        if self.mode == 'Hex':
            string = '%0' + str(self.padding) + self.format
            return string % value
        elif self.mode == 'Dec':
            string = '%' + self.format
            return string % value
    
    def valueFromText(self, value):
        if self.mode == 'Hex':
            return int(str(value), 16)
        elif self.mode == 'Dec':
            return int(str(value), 10)
            
    def setPad(self, padvalue):
        self.padding = padvalue
        self.setValue(self.value())
        
            
    def setMode(self, string):
        self.mode = string
        if string == 'Hex':
            self.validator = self.HexValidator(self.minimum(), self.maximum())
            self.format = 'X'
        elif string == 'Dec':
            self.validator = self.DecValidator(self.minimum(), self.maximum())
            self.format = 'u'


#class QHexTableView(QtGui.QTableView):
#
#    Stuff goes here with lots of stuff going here.