from typing import Union
import requests
import lxml.html as lh
from bs4 import BeautifulSoup, NavigableString
import pandas as pd
import openpyxl
import time, pickle
from others import create_excel_file, print_df_to_excel
from scholarly import scholarly
import random
from lxml.html import fromstring
import requests
from itertools import cycle
import traceback
from fake_useragent import UserAgent
from stem import Signal
from stem.control import Controller
import numpy as np

with open('./GSauthorduplicate1.pkl', 'rb') as handle:
    data_store = pickle.load(handle)
df = pd.DataFrame(data=data_store[1], columns=data_store[0])

with open('./GSauthorduplicate107.pkl', 'rb') as handle:
    data_store = pickle.load(handle)
df2 = pd.DataFrame(data=data_store[1], columns=data_store[0])

with open('./GSauthorduplicate118.pkl', 'rb') as handle:
    data_store = pickle.load(handle)
df3 = pd.DataFrame(data=data_store[1], columns=data_store[0])

with open('./GSauthorduplicate126.pkl', 'rb') as handle:
    data_store = pickle.load(handle)
df4 = pd.DataFrame(data=data_store[1], columns=data_store[0])

with open('./GSauthorduplicate130.pkl', 'rb') as handle:
    data_store = pickle.load(handle)
df5 = pd.DataFrame(data=data_store[1], columns=data_store[0])

with open('./GSauthorduplicate132.pkl', 'rb') as handle:
    data_store = pickle.load(handle)
df6 = pd.DataFrame(data=data_store[1], columns=data_store[0])

with open('./GSauthorduplicate143.pkl', 'rb') as handle:
    data_store = pickle.load(handle)
df7 = pd.DataFrame(data=data_store[1], columns=data_store[0])

with open('./GSauthorduplicate222.pkl', 'rb') as handle:
    data_store = pickle.load(handle)
df8 = pd.DataFrame(data=data_store[1], columns=data_store[0])

with open('./GSauthorduplicate268.pkl', 'rb') as handle:
    data_store = pickle.load(handle)
df9 = pd.DataFrame(data=data_store[1], columns=data_store[0])


personaldata = df
personaldata = personaldata.append(df2)
personaldata = personaldata.append(df3)
personaldata = personaldata.append(df4)
personaldata = personaldata.append(df5)
personaldata = personaldata.append(df6)
personaldata = personaldata.append(df7)
personaldata = personaldata.append(df8)
personaldata = personaldata.append(df9)

#print(personaldata)

#data1 = df.values
#data2 = df2.values
#
#testset = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
#testdata = np.vstack((data1, testset))
#print(testdata)
#for i in range(len(data2)):
#    data1 = np.vstack((data1, data2[i]))
#
#personaldata = data1
#print(len(personaldata))

data_store_columns = ['Name', 'Total Citations', 'Total Citations (5 years)', 'h-index', 'h-index (5 years)',
                      'i10-index', 'i10-index (5 years)', 'Journal Authors', 'Journal Titles', 'Journal Names',
                      'Journal Years', 'Number of publications', 'Probability of correct profile']

with open('GSauthorduplicateComplete.pkl', 'wb') as handle:
    pickle.dump([data_store_columns, personaldata.values], handle, protocol=pickle.HIGHEST_PROTOCOL)

write_excel = create_excel_file('./results/{}_results.xlsx'.format('GSauthorduplicateComplete'))
wb = openpyxl.load_workbook(write_excel)
ws = wb[wb.sheetnames[-1]]
print_df_to_excel(df=pd.DataFrame(data=personaldata, columns=data_store_columns), ws=ws)
wb.save(write_excel)

