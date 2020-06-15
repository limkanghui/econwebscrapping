import googlemaps
import json
import time, pickle
import pandas as pd
from others import create_excel_file, print_df_to_excel
import openpyxl
import numpy as np

start = time.time()

gmaps = googlemaps.Client(key='AIzaSyA3HH2p-xeU9J9hfyJUmJkfzEWvNNbMcDA')

state1data = []
state2data = []
countrydata = []

def getstatecountry(geocode_result):
    state1 = "NA"
    state2 = "NA"
    country = "NA"
    for i in range(len(geocode_result[0]['address_components'])):
        if 'locality' in geocode_result[0]['address_components'][i]['types']:
            state1 = (geocode_result[0]['address_components'][i]['long_name'])
        if 'administrative_area_level_1' in geocode_result[0]['address_components'][i]['types']:
            state2 = (geocode_result[0]['address_components'][i]['long_name'])
        if 'country' in geocode_result[0]['address_components'][i]['types']:
            country = (geocode_result[0]['address_components'][i]['long_name'])
    return state1, state2, country

df = pd.read_excel(r'./pkl/run2/2020.06.12-GSWebScrapComplete_results.xlsx')


GStitles = df['Title'].to_list()
for i in range(len(GStitles)):
    # Geocoding an address
    try:
        if np.isnan(GStitles[i]):
            state1 = 'NA'
            state2 = 'NA'
            country = 'NA'
    except:
        geocode_result = gmaps.geocode(GStitles[i])
        try:
            state1, state2, country = getstatecountry(geocode_result)
        except:
            state1 = 'Cannot retrieve'
            state2 = 'Cannot retrieve'
            country = 'Cannot retrieve'

    state1data.append(state1)
    state2data.append(state2)
    countrydata.append(country)
    #if i == 10:
    #    break

data = {'state1': state1data,
        'state2': state2data,
        'country': countrydata}

write_excel = create_excel_file('./results/{}_results.xlsx'.format('GScitystatedata'))
wb = openpyxl.load_workbook(write_excel)
ws = wb[wb.sheetnames[-1]]
print_df_to_excel(df=pd.DataFrame(data), ws=ws)
wb.save(write_excel)

elapsed = (time.time() - start) / 3600
print(f"Elapsed time: {elapsed} hours")

