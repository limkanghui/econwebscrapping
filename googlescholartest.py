from typing import Union

import requests
import lxml.html as lh
from bs4 import BeautifulSoup, NavigableString
import pandas as pd
import openpyxl
import time, pickle
from others import create_excel_file, print_df_to_excel
from scholarly import scholarly
from random import randint
from lxml.html import fromstring
import requests
from itertools import cycle
import traceback


URL = 'https://free-proxy-list.net/'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
table = soup.find('table', attrs={'id': 'proxylisttable'})
#print(table.prettify())
proxies = []
for tr in table.tbody.findAll('tr'):
    td = tr.find('td')
    proxies.append(td.text)

proxy_pool = cycle(proxies)

name = 'Lim Kang Hui'

namesplit = name.split()
search = namesplit[0]
for i in range(1, len(namesplit)):
    search += '+' + namesplit[i]
URL = 'https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors={}&btnG='.format(search)
sleeptimerandom = randint(1, 2)
time.sleep(sleeptimerandom)
#for i in range(len(proxies)):
#    proxy = next(proxy_pool)
#    try:
#        page = requests.get(URL, proxies={"http": "http://{}".format(proxy), "https": "https://{}".format(proxy)})
#    except:
#        print("Skipping. Connnection error")

page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
print(soup.prettify())

# Check if profile exists
GSprofilee = True
try:
    div = soup.find('div', attrs={'id': 'gsc_sa_ccl'})
except:
    print('Profile not in Google Scholar')
    GSprofilee = True


div = soup.find('div', attrs={'id': 'gsc_sa_ccl'})
numberofprofilessearched = 0
for row in div.find_all('div', attrs={'class': 'gsc_1usr'}):
    numberofprofilessearched += 1
if numberofprofilessearched > 1:
    print('more than one, {}, profiles found'.format(numberofprofilessearched))
    with open('data_store.pkl', 'wb') as handle:
        pickle.dump([['Authors with more than 1 profile in GS'], name], handle, protocol=pickle.HIGHEST_PROTOCOL)
probabilityprofilecorrect = 1/numberofprofilessearched
urltoprofile = div.a['href']
URL = 'https://scholar.google.com{}'.format(urltoprofile)
page = requests.get(URL)
sleeptimerandom = randint(0, 5)
time.sleep(sleeptimerandom)
soup = BeautifulSoup(page.content, 'html.parser')
#print(soup.prettify())

def read_author_data(author_name):
    print("reading data for {0:s}".format(author_name))
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