import requests
import lxml.html as lh
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
import time
from others import create_excel_file, print_df_to_excel
from scholarly import scholarly

name = 'Lim Kang Hui'

namesplit = name.split()
search = namesplit[0]
for i in range(1, len(namesplit)):
    search += '+' + namesplit[i]
URL = 'https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors={}&btnG='.format(search)
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
print(soup.prettify())
div = soup.find('div', attrs={'id': 'gsc_sa_ccl'})
numberofprofilessearched = 0
for row in div.find_all('div', attrs={'class': 'gsc_1usr'}):
    numberofprofilessearched += 1
if numberofprofilessearched > 1:
    print('more than one, {}, profiles found'.format(numberofprofilessearched))
probabilityprofilecorrect = 1/numberofprofilessearched
urltoprofile = div.a['href']
URL = 'https://scholar.google.com{}'.format(urltoprofile)
page = requests.get(URL)
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
