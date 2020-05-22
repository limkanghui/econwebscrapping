import requests
import lxml.html as lh
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
import time
from others import create_excel_file, print_df_to_excel
workingpapers = []
articles = []
chapters = []
books = []

URL = 'https://ideas.repec.org/e/pap38.html'
#Create a handle, page, to handle the contents of the website
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
div = soup.find('div' ,attrs={'class':'tab-pane fade show active'})
possiblepublications = []
for a in div.findAll('a'):
    possiblepublications.append(a.text)
if possiblepublications[0] == 'Working papers':
    table = soup.find('li' ,attrs={'class':'list-group-item downfree'})
    publications = table.findAll('b')
    for a in publications.findAll('a'):








#for i in range(indices[0]):
#    if possiblepublications[i] == 'Working papers':
#        bullet = 1
#        smartcount += 1
#        for j in range(indices[smartcount - 1] + 1, indices[smartcount], 2):
#            titlewithjournal = str(bullet) + ')' + ' ' + possiblepublications[j] + ', ' + possiblepublications[j + 1]
#            workingpapers.append(titlewithjournal)
#            bullet += 1
#    if possiblepublications[i] == 'Articles':
#        bullet = 1
#        smartcount += 1
#        for j in range(indices[smartcount - 1] + 1, indices[smartcount], 2):
#            titlewithjournal = str(bullet) + ')' + ' ' + possiblepublications[j] + ', ' + possiblepublications[j + 1]
#            articles.append(titlewithjournal)
#            bullet += 1








