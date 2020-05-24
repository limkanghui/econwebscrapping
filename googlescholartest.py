from typing import Union
import requests
import lxml.html as lh
from bs4 import BeautifulSoup, NavigableString
import pandas as pd
import openpyxl
import time, pickle
from others import create_excel_file, print_df_to_excel
from scholarly import scholarly
from random import randint, random, seed
from lxml.html import fromstring
import requests
from itertools import cycle
import traceback


#URL = 'https://free-proxy-list.net/'
#page = requests.get(URL)
#soup = BeautifulSoup(page.content, 'html.parser')
#table = soup.find('table', attrs={'id': 'proxylisttable'})
##print(table.prettify())
#proxies = []
#for tr in table.tbody.findAll('tr'):
#    td = tr.find('td')
#    proxies.append(td.text)
#
#proxy_pool = cycle(proxies)

start = time.time()

with open('./IDEASdataComplete.pkl', 'rb') as handle:
    data_store = pickle.load(handle)
df = pd.DataFrame(data = data_store[1], columns = data_store[0])

personaldata = []

for authors in range(len(df['name'])):
    name = df['name'][authors]

    personaldetails = []

    namesplit = name.split()
    search = namesplit[0]
    for i in range(1, len(namesplit)):
        search += '+' + namesplit[i]
    URL = 'https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors={}&btnG='.format(search)

    # random time lag for requests
    seed(1)
    sleeptimerandom = 3 * random()
    if sleeptimerandom < 0.6:
        sleeptimerandom + 0.6
    time.sleep(sleeptimerandom)

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    #print(soup.prettify())

    # Check if profile exists
    GSprofile = True
    div = soup.find('div', attrs={'id': 'gsc_sa_ccl'})
    try:
        textsearch = div.p.text
        GSprofile = False
    except AttributeError:
        pass

    if GSprofile:
        div = soup.find('div', attrs={'id': 'gsc_sa_ccl'})
        numberofprofilessearched = 0
        for row in div.find_all('div', attrs={'class': 'gsc_1usr'}):
            numberofprofilessearched += 1
        if numberofprofilessearched > 1:
            print('more than one, {}, profiles found for {}'.format(numberofprofilessearched, name))
            with open('data_store.pkl', 'wb') as handle:
                pickle.dump([['Authors with more than 1 profile in GS'], name], handle, protocol=pickle.HIGHEST_PROTOCOL)
        probabilityprofilecorrect = 1/numberofprofilessearched
        urltoprofile = div.a['href']
        URL = 'https://scholar.google.com{}'.format(urltoprofile)
        page = requests.get(URL)
        sleeptimerandom = randint(1, 5)
        time.sleep(sleeptimerandom)
        soup = BeautifulSoup(page.content, 'html.parser')
        #print(soup.prettify())

    def read_author_data(author_name):
        print("reading data for {0:s}...".format(author_name))
        author = next(scholarly.search_author(author_name)).fill()
        a_data = {
            "name": author.name,
            "affiliation": author.affiliation,
            "cites_per_year": author.cites_per_year,
            "citedby": author.citedby,
            "citedby5y": author.citedby5y,
            "hindex": author.hindex,
            "hindex5y": author.hindex5y,
            "i10index": author.i10index,
            "i10index5y": author.i10index5y,
            "url_picture": author.url_picture,
            "pubs": [
                {"title": pub.bib['title'],
                 "year": pub.bib['year'] if "year" in pub.bib  else -1,
                 "citedby": pub.citedby if hasattr(pub, "citedby") else 0,
                 "link": pub.id_citations if hasattr(pub, "id_citations") else ""
                 }
                for pub in author.publications]
        }
        return a_data


    if GSprofile:
        a_data = read_author_data(name)

        totalcitations = a_data["citedby"]
        totalcitations5y = a_data["citedby5y"]
        hindex = a_data["hindex"]
        hindex5y = a_data["hindex5y"]
        i10index = a_data["i10index"]
        i10index5y = a_data["i10index5y"]
        pub = a_data["pubs"]
        GStitle = ''
        GSyear = ''
        for i in range(0, len(pub)):
            publication = pub[i]
            GStitle += '{}) '.format(i + 1) + publication['title'] + '\n'
            GSyear += '{}) '.format(i + 1) + publication['year'] + '\n'
        numberofpublicationsfromGS = len(pub)
    else:
        totalcitations = 'na'
        totalcitations5y = 'na'
        hindex = 'na'
        hindex5y = 'na'
        i10index = 'na'
        i10index5y = 'na'
        GStitle = 'na'
        GSyear = 'na'
        numberofpublicationsfromGS = 'na'
        probabilityprofilecorrect = 'na'

    personaldetails.append(totalcitations)
    personaldetails.append(totalcitations5y)
    personaldetails.append(hindex)
    personaldetails.append(hindex5y)
    personaldetails.append(i10index)
    personaldetails.append(i10index5y)
    personaldetails.append(GStitle)
    personaldetails.append(GSyear)
    personaldetails.append(numberofpublicationsfromGS)
    personaldetails.append(probabilityprofilecorrect)

    personaldata.append(personaldetails)

    if authors > 0:
        break

data_store_columns = ['Total Citations', 'Total Citations (5 years)', 'h-index', 'h-index (5 years)', 'i10-index',
                      'i10-index (5 years)', 'Journal Titles', 'Journal Years', 'Number of publications',
                      'Probability of correct profile']


write_excel = create_excel_file('./results/{}_results.xlsx'.format('GSWebScrap'))
wb = openpyxl.load_workbook(write_excel)
ws = wb[wb.sheetnames[-1]]
print_df_to_excel(df=pd.DataFrame(data=personaldata, columns=data_store_columns), ws=ws)
wb.save(write_excel)

elapsed = (time.time() - start)/3600
print(f"Elapsed time: {elapsed} hours")