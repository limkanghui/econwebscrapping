import requests
import lxml.html as lh
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
import time
from others import create_excel_file, print_df_to_excel
import gender_guesser.detector as gender
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

femalerepecshortID = []

# Get data on female authors
URL = 'https://ideas.repec.org/top/top.women.html'
# Create a handle, page, to handle the contents of the website
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
# print(soup.prettify())
table = soup.find('table', attrs={'class': 'shorttop'})
tabledata = table.findAll('tr')
for row in tabledata:
    for a in row.findAll('a'):
        femalerepecshortID.append(a.get('name'))
print(femalerepecshortID)
personaldata = []
counter = 1
for i in links:
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
    if personaldetails[5] in femalerepecshortID:
        personaldetails.append('Top Female')
    else:
        personaldetails.append('')

    gender = d.get_gender(u"{}".format(personaldetails[1]))
    personaldetails.append(gender)

    workingpapers = []
    workingpapersauthors = []
    articles = []
    articlesauthors = []

    div = soup.find('div', attrs={'class': 'tab-pane fade show active'})
    possiblepublications = []
    for a in div.find_all('a', recursive=False):
        possiblepublications.append(a.text)

    workingpaperotherversion = []
    workingpapersauthorsotherversion = []
    articleotherversion = []
    articlesauthorsotherversion = []
    if possiblepublications[0] == 'Working papers':
        table = soup.find('ol', attrs={'class': 'list-group'})
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
        table = soup.find('ol', attrs={'class': 'list-group'})
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

    A = ''
    B = ''
    C = ''
    D = ''

    for i in range(0, len(workingpapersauthors)):
        A += '{})'.format(i + 1) + workingpapersauthors[i]
    for i in range(0, len(workingpapers)):
        B += '{}) '.format(i + 1) + workingpapers[i] + '\n'
    for i in range(0, len(articlesauthors)):
        C += '{}) '.format(i + 1) + articlesauthors[i]
    for i in range(0, len(articles)):
        D += '{}) '.format(i + 1) + articles[i] + '\n'

    personaldetails.append(A.replace(' "', ''))
    personaldetails.append(B)

    # Get Journal Year
    WPyear = ''
    WPyearcounter = 1
    for i in range(0, len(workingpapersauthors)):
        for word in workingpapersauthors[i].split():
            word = word.replace('.', '')
            if word.isdigit():
                WPyear += '{}) '.format(WPyearcounter) + word + '\n'
                WPyearcounter += 1

    personaldetails.append(WPyear)
    personaldetails.append(len(workingpapers))
    personaldetails.append(C.replace('"', ''))
    personaldetails.append(D)

    Ayear = ''
    Ayearcounter = 1
    for i in range(0, len(articlesauthors)):
        for word in articlesauthors[i].split():
            word = word.replace('.', '')
            if word.isdigit():
                Ayear += '{}) '.format(Ayearcounter) + word + '\n'
                Ayearcounter += 1

    personaldetails.append(Ayear)
    personaldetails.append(len(articles))

    personaldata.append(personaldetails)
    print('Progress: {} out of {} for {}'.format(counter, len(names), name))
    counter += 1

    if counter == 5:
       break

data_store_columns = ['name', 'first name', 'middle name', 'last name', 'suffix', 'repecshortID', 'email',
                      'homepage', 'postal address', 'phone', 'twitterhandle', 'Top Female', 'Gender',
                      'working papers authors and year', 'working papers title', 'working papers year',
                      '# of working papers', 'articles authors and year', 'articles tile', 'article year',
                      '# of articles']

write_excel = create_excel_file('./results/{}_results.xlsx'.format('EconomicsAuthors'))
wb = openpyxl.load_workbook(write_excel)
ws = wb[wb.sheetnames[-1]]
print_df_to_excel(df=pd.DataFrame(data=personaldata, columns=data_store_columns), ws=ws)
wb.save(write_excel)

elapsed = (time.time() - start)/3600
print(f"Elapsed time: {elapsed} hours")
