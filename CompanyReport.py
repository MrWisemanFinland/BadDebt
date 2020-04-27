# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 15:20:57 2020

@author: Mikko
"""

from datetime import date

class CompanyReport:
    def __init__(self, cno, cname):
        self.cno = cno
        self.cname = cname
        self.currs = 0.0
        self.ovds = 0.0
        self.ovdd = []
    
    def addCur(self, amount):
        self.currs += amount
    
    def addOvd(self, amount):
        self.ovds += amount
    
    def addOvdd(self, days):
        self.ovdd.append(days)
        