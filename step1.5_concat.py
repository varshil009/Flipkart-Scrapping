# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 11:57:28 2023

@author: Varshil
"""

# 1==> Concate all csvs
import pandas as pd
df_main  = pd.DataFrame()
for x in range(1, 41): 
    file = f"E:\skill based learning\DATA SCIENCE\FlipKart Scrapping\page{x}.csv"
    df = pd.read_csv(file)
    df_main = pd.concat([df_main, df], axis = 0)
    
df_main.to_csv('E:\skill based learning\DATA SCIENCE\FlipKart Scrapping\combined.csv', index = False)