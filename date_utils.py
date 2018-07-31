# -*- coding: utf-8 -*-
from datetime import datetime 

def stringToDate(string):
    #example '2018-07-22'
    dt = datetime.strptime(string, "%Y-%m-%d")
    #print dt
    return dt

''''' Date(datetime) to String '''

def dateToString(date):
    ds = date.strftime('%Y-%m-%d')
    return ds
