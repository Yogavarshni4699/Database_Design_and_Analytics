# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 22:49:56 2023

@author: VENKATACHALAM N
"""
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic

from TitanicWindow import TitanicWindow
from TitanicWindowDD import TitanicWindowDD
from TitanicWindowReport import TitanicWindowReport

class LandingWindow(QDialog):
    def __init__(self):
            super().__init__()
            self.ui = uic.loadUi('Landing_page.ui')
            
            self.overview_dialog = TitanicWindow()
            self.drilldown_dialog = TitanicWindowDD()
            self.report_dialog = TitanicWindowReport()
                        
            self.ui.pushButton.clicked.connect(self.show_overview_dialog)
            self.ui.pushButton_2.clicked.connect(self.show_drilldown_dialog)
            self.ui.pushButton_3.clicked.connect(self.show_report_dialog)
            
    def show_overview_dialog(self):
        self.overview_dialog.show_dialog()
        
    def show_drilldown_dialog(self):
        self.drilldown_dialog.show_dialog()
        
    def show_report_dialog(self):
        self.report_dialog.show_dialog()
        
    def show_dialog(self):
        self.ui.show()