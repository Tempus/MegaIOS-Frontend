# -*- coding: utf-8 -*-
# 
# Stuff goes here!

import sys
from PyQt4 import QtCore, QtGui
from MegaUI import MegaWindow

#class BootstrapClass(QtGui.QMainWindow):
#    def __init__(self, parent=None):
#        QtGui.QWidget.__init__(self, parent)
#        self.megaWindow = MegaWindow()

def main():
    app = QtGui.QApplication(sys.argv)
    Bootstrap = MegaWindow()
    Bootstrap.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
