import requests
import lxml.html as lh
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
import time
from others import create_excel_file, print_df_to_excel
workingpapers = []
workingpapersauthors = []
articles = []
articlesauthors = []

URL = 'https://ideas.repec.org/f/pal663.html'
#Create a handle, page, to handle the contents of the website
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
#print(soup.prettify())
div = soup.find('div' ,attrs={'class':'tab-pane fade show active'})
possiblepublications = []
for a in div.find_all('a', recursive=False):
    possiblepublications.append(a.text)
print(possiblepublications)

workingpaperotherversion = []
workingpapersauthorsotherversion = []
articleotherversion = []
articlesauthorsotherversion = []
if possiblepublications[0] == 'Working papers':
    table = soup.find('ol' ,attrs={'class':'list-group'})
    for li in table.find_all('li', recursive=False):
        for div in li.findAll('div'):
            workingpaperotherversion.append(div.b.text)
            workingpapersauthorsotherversion.append(div.li.contents[0])
    for li in table.find_all('li', recursive=False):
        for b in li.findAll('b'):
            workingpapers.append(b.text)
    for li in table.find_all('li', recursive=True):
        workingpapersauthors.append(li.contents[0])
if possiblepublications[1] == 'Articles':
    table = soup.find('ol', attrs={'class': 'list-group'})
    table2 = table.find_next_sibling('ol')
    for li in table2.find_all('li', recursive=False):
        for div in li.findAll('div'):
            articleotherversion.append(div.b.text)
            articlesauthorsotherversion.append(div.li.contents[0])
    for li in table2.find_all('li', recursive=False):
        for b in li.findAll('b'):
            articles.append(b.text)
    for li in table2.find_all('li', recursive=True):
        articlesauthors.append(li.contents[0])
if possiblepublications[0] == 'Articles':
    table = soup.find('ol' ,attrs={'class':'list-group'})
    for li in table.find_all('li', recursive=False):
        for div in li.findAll('div'):
            articleotherversion.append(div.b.text)
            articlesauthorsotherversion.append(div.li.contents[0])
    for li in table.find_all('li', recursive=False):
        for b in li.findAll('b'):
            articles.append(b.text)
    for li in table.find_all('li', recursive=True):
        articlesauthors.append(li.contents[0])

for i in workingpaperotherversion:
    workingpapers.remove(i)
for i in articleotherversion:
    articles.remove(i)
for i in workingpapersauthorsotherversion:
    workingpapersauthors.remove(i)
for i in articlesauthorsotherversion:
    articlesauthors.remove(i)

B = ''
A = ''
for i in range(0, len(workingpapersauthors)):
    A += '{})'.format(i + 1) + workingpapersauthors[i]
for i in range(0, len(workingpapers)):
    B += '{})'.format(i + 1) + workingpapers[i] + '\n'

WPyear = ''
WPyearcounter = 1
for i in range(0, len(workingpapersauthors)):
    for word in workingpapersauthors[i].split():
        word = word.replace('.', '')
        if word.isdigit():
            WPyear += '{}) '.format(WPyearcounter) + word + '\n'
            WPyearcounter += 1
