# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 17:40:37 2020

@author: Mikko
"""
from datetime import date

class InvoiceData:
  
    
#    ino = "" # Invoice number
#    rno = "" # Receipt number
#    cno = 0 # Customer number
#    cname = "" #Customer name
#    cat = "" # Category
#    idate = date(1, 1, 1) # Invoice date
#    ddate = date(1, 1, 1) # Due date
#    sevat = 0.0 # Sum excluding VAT
#    vat = 0.0 # VAT
#    s = 0.0 # Sum
    
    def __init__(self, ino, rno, cno, cname, cat, idate, ddate, sevat, vat, s):
        
        self.ino = ino # Invoice number
        self.rno = rno # Receipt number
        self.cno = int(cno) # Customer number
        self.cname = cname #Customer name
        self.cat = cat # Category
        self.idate = self.splitdate(idate) # Invoice date
        self.ddate = self.splitdate(ddate) # Due date
        self.sevat = float(sevat) # Sum excluding VAT
        self.vat = float(vat) # VAT
        self.s = float(s)# Sum
    
    def splitdate(self, datein):

        
        da = datein.split("/")
        m = int(da[0])
        d = int(da[1])
        y = int(da[2])
        
        return date(y, m, d)

        
        
    