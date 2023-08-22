# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from bs4 import BeautifulSoup as bs
import requests as r 
import pandas as pd

# extract data from 40 pages
for p in range(13,41):
    # put URL and get response
    url = f"https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&param=7564&ctx=eyJjYXJkQ29udGV4dCI6eyJhdHRyaWJ1dGVzIjp7InRpdGxlIjp7Im11bHRpVmFsdWVkQXR0cmlidXRlIjp7ImtleSI6InRpdGxlIiwiaW5mZXJlbmNlVHlwZSI6IlRJVExFIiwidmFsdWVzIjpbIlJlYWxtZSJdLCJ2YWx1ZVR5cGUiOiJNVUxUSV9WQUxVRUQifX19fX0%3D&otracker=clp_metro_expandable_1_5.metroExpandable.METRO_EXPANDABLE_Realme_mobile-phones-store_Q1PDG4YW86MF_wp3&fm=neo%2Fmerchandising&iid=M_3f543f2a-6910-4e73-9d82-bd387f4dd7a8_5.Q1PDG4YW86MF&ppt=clp&ppn=mobile-phones-store&ssid=rvs36tk54w0000001692021418540&page={p}"
    response = r.get(url)
    
    # get response
    parsed_data = bs(response.text, 'html.parser')
    
    # find all div tags and extract mobile phones data from it
    divs = parsed_data.find_all('div')
    
    mobile_cells = []
    
    # _36fx1h _6t1WkM _3HgJxg
    # _1YokD2 _3Mn1G
    # _1AtVbE col-12-12
    # _13oc-S
    for x in divs:
        if x.get('class') == None:
            pass
        elif x.get('class') == ['_13oc-S']:
            mobile_cells.append(x)
    
    # making list for different features
    name = []
    rting = []
    features_all, features_ind = [], []
    price = []
    
    # iterate over all div tags in page
    for x in mobile_cells:
        
        # finds all div tags in a cell
        cell_items = x.find_all('div')
        
        # iterates over every div tag finds corresponding item
        for item in cell_items:
            # get the class
            y = item.get('class')
            
            # ignore Nones
            if y == None:
                pass
        
            # extract name header
            elif y[0] == '_4rR01T':
                name.append(item.text)
    
            # extract ratings & reviews
            elif y[0] == 'gUuXy-':
                rting.append(item.text)
                
            # extract features
            elif y[0] == 'fMghEO':
                for f in item.find_all('li'):
                    features_ind.append(f.text)
                features_all.append(features_ind)
                features_ind = [] 
                
            # extract prices
            elif len(y) == 3:
                price.append(item.text)
                
    # simlyfy nested list of feature
    feat1, feat2, feat3, feat4, feat5, feat6 = [], [], [], [], [], []
    for x in range(len(features_all)):
        feat1.append(features_all[x][0])
        feat2.append(features_all[x][1])
        feat3.append(features_all[x][2])
        
        if len(features_all[x]) < 4:
            feat4.append(None)
        else:
            feat4.append(features_all[x][3])
        
        # some have <5 feature so to handle index error
        if len(features_all[x]) < 5:
            feat5.append(None)
        else:
            feat5.append(features_all[x][4])
        
        # some have <6 feature so to handle index error
        if len(features_all[x]) < 6:
            feat6.append(None)
        else:
            feat6.append(features_all[x][5])
    
    # make a dataframe    
    pd.DataFrame(zip(name, rting, feat1, feat2, feat3, feat4, feat6, price)).to_csv(f"E:\skill based learning\DATA SCIENCE\FlipKart Scrapping\page{p}.csv")
    
