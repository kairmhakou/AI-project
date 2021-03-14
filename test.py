# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 11:41:19 2021

@author: dehan
"""

import glob
arr = glob.glob(".\csv\*.csv")
for f in arr:
    file = f.split('\\')[-1]
    filename = file.split('.')[0]
    print(filename)