import requests
import lxml.html as lh
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
import time, pickle
from others import create_excel_file, print_df_to_excel
import gender_guesser.detector as gender
import json
from urllib.request import urlopen
from genderize import Genderize
import numpy as np

d = gender.Detector()

start = time.time()
URL = 'https://ideas.repec.org/i/etwitter.html'
# Create a handle, page, to handle the contents of the website
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

links = []
names = []

for tr in soup.findAll('tr'):
    if None in tr:
        continue
    for a in tr.findAll('a'):
        links.append(a['href'])
        if len(a.text) > 2:
            names.append(a.text)
print(len(links))
print(len(names))

personaldata = []
counter = 1
for i in links:
    #i = '/e/pan29.html'
    URL = 'https://ideas.repec.org{}'.format(i)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    #print(soup.prettify())
    table = soup.find('table', attrs={'class': 'table table-condensed'})
    tabledata = table.findAll('tr')
    personaldetails = []
    name = []
    personaldatacount = 1
    for row in tabledata:
        if personaldatacount == 11:
            break
        second_column = row.findAll('td')[1].text
        personaldetails.append(second_column)
        personaldatacount += 1
    if personaldetails[1] == '':
        name = [personaldetails[0] + ' ' + personaldetails[2]]
    else:
        name = [personaldetails[0] + ' ' + personaldetails[1] + ' ' + personaldetails[2]]
    personaldetails = name + personaldetails

    div = soup.find('div', attrs={'id': 'affiliation'})
    affiliationpage = True
    try:
        h3 = div.find('h3')
    except AttributeError:
        affiliationpage = False
        pass
    if affiliationpage:
        h3 = div.find_all('h3')
        affiliation = ''
        #affiliation = []
        for row in h3:
            affiliation += row.text + '/'
            #affiliation.append(row.text)

        location_counter = 1
        location = div.find_all('span', attrs={'class': 'locationlabel'})
        locationdata = ''
        #locationdata = []
        for row in location:
            #locationdata += '{}) '.format(location_counter) + row.text + '\n'
            locationdata += row.text + '/'
            location_counter += 1
            #locationdata.append(row.text)
    else:
        affiliation = 'NA'
        locationdata = 'NA'


    #print(affiliation)
    #print(locationdata)
    personaldetails.append(affiliation)
    personaldetails.append(locationdata)

    personaldata.append(personaldetails)

    print('Progress: {} out of {} for {} done'.format(counter, len(names), name))
    counter += 1

    #if counter == 5:
    #    break

data_store_columns = ['name', 'first name', 'middle name', 'last name', 'suffix', 'repecshortID', 'email',
                      'homepage', 'postal address', 'phone', 'twitterhandle', 'affiliation', 'locationdata']

write_excel = create_excel_file('./results/{}_results.xlsx'.format('IDEASaffiliation'))
wb = openpyxl.load_workbook(write_excel)
ws = wb[wb.sheetnames[-1]]
print_df_to_excel(df=pd.DataFrame(data=personaldata, columns=data_store_columns), ws=ws)
wb.save(write_excel)

# store in pkl for future retrieve (no need to rerun code again)
with open('IDEASaffiliationSecondVariant.pkl', 'wb') as handle:
    pickle.dump([data_store_columns, personaldata], handle, protocol=pickle.HIGHEST_PROTOCOL)

elapsed = (time.time() - start)/3600
print(f"Elapsed time: {elapsed} hours")