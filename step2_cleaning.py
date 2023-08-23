# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 12:13:42 2023

@author: Varshil
"""

# 2==> Data cleaning
import pandas as pd
df = pd.read_csv("E:\skill based learning\DATA SCIENCE\FlipKart Scrapping\Outputs\combined.csv")

df.drop('Unnamed: 0', axis = 1, inplace = True)
df.columns = ['name', 'rating', 'feat1', 'feat2', 'feat3', 'feat4', 'feat6', 'price']

#%%
df['maker'] = df.name.apply(lambda x : x.split()[0])
df.maker.value_counts()
#%%
import numpy as np
df['product_name'] = df.name.apply(lambda x : x.split()[1] if len(x.split()) > 1 else 0)
df['color'] = df.name.apply(lambda x: x.split("(")[1].split(",")[0]
                                         if "(" in x else 0)
#%%
df['ratings_'] = df.rating.apply(lambda x : x[:3])
df['num_ratings_given'] = df.rating.apply(lambda x : x.split()[0][3:])
#%%
df['num_reviews'] = df.rating.apply(lambda x : x.split("&")[1].split()[0])
#%%
# there are some reviews which have digits values for ratings. So those ratings are mixed up with nhumber of 
# ratings. thus cleaning up those here
def ratings_cleaner(df):
    ratings_new = list(df.ratings_)
    for i,x in enumerate(ratings_new):
        if "," in x:
            ratings_new[i] = 0

        elif x.isdigit(): 
            if int(x) > 5:
                ratings_new[i] = float(x[0])
    df['ratings_new'] = ratings_new
ratings_cleaner(df)
#%%
def num_ratings_cleaner(df):
    num_ratings_new = list(df.num_ratings_given)
    ratings_new = list(df.ratings_)
    for i,x in enumerate(ratings_new):
        if "," in x:
            num_ratings_new[i] = x + num_ratings_new[i]

        elif x.isdigit(): 
            if int(x) > 5:
                num_ratings_new[i] = x[1:] + num_ratings_new[i]
    df['num_ratings_new'] = num_ratings_new
num_ratings_cleaner(df)
#%%
# remove commas
df.num_ratings_new = df.num_ratings_new.apply(lambda x : "".join(x.split(",")))
#%%
# fill the nan values accordingly and replace faulty number of ratings
list1 = list(df.rating)
list2 = list(df['ratings_new'])
list3 = list(df['num_ratings_new'])


for i,x in enumerate(list2):
    if x == 0:
        print(i, x, list2[i], list1[i][0], list3[i], list3[i][1:])
        list2[i] = list1[i][0]
        list3[i] = list3[i][1:]
    else:
        pass
#%%
df['ratings_new'] = list2
(df['num_ratings_new']) = list3
#%%
# put 0 inplace of string showing no value available
df.iloc[683, 14] = 0
df.iloc[773, -2] = 0
df.iloc[928, -2] = 0

#%%
import re
def ram_rom_ext(df):
    ram = []
    rom = []
    expandable = []
    for x in list(df.feat1):
        ram_match = re.search(r'(\d+)\s*(M|G|T)B\s*RAM', x)
        rom_match = re.search(r'(\d+)\s*(M|G|T)B\s*ROM', x)
        exp_match = re.search(r'Expandable Upto (\d+) (T|G|M)B', x)
        
        if ram_match:
            ram.append(ram_match.group(0)[:-3])
        else:
            ram.append(0)
        
        if rom_match:
            rom.append(rom_match.group(0)[:-3])
        else:
            rom.append(0)
            
        if exp_match:
            expandable.append(exp_match.group(0).split('o')[1].strip())
        else:
            expandable.append(0)
    return ram, rom, expandable
        
ram1, rom1, exp1 = ram_rom_ext(df)
#%%
df['ROM'] = rom1
df['RAM'] = ram1
df['Expandable_ROM'] = exp1
#%%
# convert all into GB
def converter(y):
    y = y.strip()
    if re.search("(\d+) GB", y):
        return re.search("(\d+) GB", y).group(1)
    
    elif re.search("(\d+) TB", y):
        return int(re.search("(\d+) TB", y).group(1))*1024
    
    elif re.search("(\d+) MB", y):
        return int(re.search("(\d+) MB", y).group(1))/1024
    
    else:
        return 0

df['RAM'] = df.RAM.astype(str).apply(converter)
df['ROM'] = df.ROM.astype(str).apply(converter)
df['Expandable_ROM'] = df.Expandable_ROM.astype(str).apply(converter)
#%%
df.drop('Main_Camera', axis = 1, inplace = True)
#%%
for i,x in enumerate(front):
    if len(str(x).split()) > 1:
        front[i] = x.strip()[:-12]
    else:
        front[i] = '0MP'
#%%
# processing feature 2
df['Display_size'] = df.feat2.apply(lambda x : x.split(")")[0].strip())
df['Display_type'] = df.feat2.apply(lambda x : x.split(")")[1].strip())

#%%
feat3_ = df.feat3.to_list()
front, rear = [], []
for i,x in enumerate(feat3_):
    
    if len(x.split("|")) == 1:
        print(i,"no")
        front_match = re.search("(\d+)\s*MP\s*Front\s*Camera", x)
        rear_match = re.search("(\d+)\s*MP\s*Rear\s*Camera", x)
        
        if front_match:
            front.append(front_match.group(0).split("F")[0].strip())
            rear.append(0)
    
        elif rear_match:
            rear.append(rear_match.group(0).split("R")[0].strip())
            front.append(0)
        
        else:
            rear.append(0)
            front.append(0)
            
    elif len(x.split("|")) > 1:
        print(i,"yes")
        rear.append(x.split("|")[0].strip())
        front.append(x.split("|")[1].strip())
        
#%%
"""df['Rear_Camera'] = rear"""
df['Front_Camera'] = front
#%%
df['Battery_Backup'] = df.feat4
#%%
df['Price'] = df.price.apply(lambda x : re.search(r"₹?(\d+),?(\d+)₹?", x).group(0).strip('₹').replace(',',""))

#%%
# add missing value thats it
df.price[789] = "₹18,693₹2599928% offFree delivery by Today No Cost EMI from ₹3,116/month"
#%%
def battery(y):
    if re.search("(\d+) mAh", y):
        return re.search("(\d+) mAh", y).group(1)
    else:
        return 0
df['Battery_Backup'] = df.Battery_Backup.apply(battery)
#%%
df.rename(columns = {'Battery_Backup' : 'Battery_Backup_mAh'}, inplace = True)
#%%
df['Front_Camera'] = df.Front_Camera.apply(lambda x : x.replace('MP', ""))
#%%
def dual_cam(y):
    if re.search(r"(\d+)MP Dual Rear Camera\s*", y):
        return 1
    else:
        return 0
df['Rear_Dual_Camera'] = df['Rear_Camera'].astype(str).apply(dual_cam)
#%%
df['Rear_Camera'] = df.Rear_Camera.astype(str).apply(lambda x: re.search("(\d+)MP", x).group(1) if re.search("(\d+)MP", x) else 0)
#%%
df['Display_size'] = df.Display_size.apply(lambda x : re.search("(\d+).(\d+) cm", x).group(0).replace("cm", "").strip())
#%%
text = '16.56 cm (6.52 inch'
print(re.search("(\d+).(\d+) cm", text).group(0).replace("cm", "").strip())
#%%
df['num_reviews'] = df.num_reviews.apply(lambda x: x.replace(",", ""))
#%%
df.rename(columns = {'RAM' : 'RAM(GB)', 'ROM' : 'ROM(GB)', 'Expandable_ROM' : 'Expandable_ROM(GB)',
                     'Display_size' : 'Display_Size(cm)', 'Rear_Camera' : 'Rear_Camera)(MB)',
                     'Front_Camera' : 'Front_Camera(MB)', 'Battery_Backup' : 'Battery_Backup(mAh)',
                     'Price' : 'Price(₹)'}, inplace = True)
#%%
# improving some naming mistakes
df.rename(columns = {'Rear_Camera)(MB)' : 'Rear_Camera(MB)',
                     'Battery_Backup_mAh' : 'Battery_Backup(mAh)'}, inplace = True)
#%%
pre_cleaned_df = df.drop(['ratings_', 'num_ratings_given'], axis = 1)
cleaned_df = pre_cleaned_df.iloc[:,-16:]
#%%
cleaned_df.to_csv(r'E:\skill based learning\DATA SCIENCE\FlipKart Scrapping\Outputs\Cleaned_Data.csv', index = False)