import requests
import lxml.html as lh
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
import time
from others import create_excel_file, print_df_to_excel
from genderize import Genderize

genderize = Genderize(
    user_agent='GenderizeDocs/0.0',
    api_key='example_api_key',
    timeout=5.0)


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
    # print(soup.prettify())
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

    gender = genderize.get(personaldetails[1])

    personaldetails = personaldetails[0:13]


    #workingpapers = []
    #articles = []
#
    #div = soup.find('div', attrs={'class': 'tab-pane fade show active'})
    #possiblepublications = []
    #for a in div.findAll('a'):
    #    possiblepublications.append(a.text)
    #indices = [i for i, x in enumerate(possiblepublications) if x == ""]
    #print(possiblepublications)
    #if indices[0] == 0:
    #    # no publications
    #    personaldetails.append(["", ""])
    #else:
    #    smartcount = 0
    #    for i in range(indices[0]):
    #        print(i)
    #        if possiblepublications[i] == 'Working papers':
    #            bullet = 1
    #            smartcount += 1
    #            for j in range(indices[smartcount - 1] + 1, indices[smartcount], 2):
    #                titlewithjournal = str(bullet) + ')' + ' ' + possiblepublications[j] + ', ' + possiblepublications[
    #                    j + 1]
    #                workingpapers.append(titlewithjournal)
    #                bullet += 1
    #        if possiblepublications[i] == 'Articles':
    #            bullet = 1
    #            smartcount += 1
    #            for j in range(indices[smartcount - 1] + 1, indices[smartcount], 2):
    #                titlewithjournal = str(bullet) + ')' + ' ' + possiblepublications[j] + ', ' + possiblepublications[
    #                    j + 1]
    #                articles.append(titlewithjournal)
    #                bullet += 1
    #    personaldetails.append(workingpapers)
    #    personaldetails.append(articles)


    personaldata.append(personaldetails)
    print('Progress: {} out of {} for {}'.format(counter, len(names), name))
    counter += 1

    #if counter == 5:
    #   break

data_store_columns = ['name', 'first name', 'middle name', 'last name', 'suffix', 'repecshortID', 'email',
                      'homepage', 'postal address', 'phone', 'twitterhandle', 'Top Female', 'Gender']

write_excel = create_excel_file('./results/{}_results.xlsx'.format('EconomicsAuthors'))
wb = openpyxl.load_workbook(write_excel)
ws = wb[wb.sheetnames[-1]]
print_df_to_excel(df=pd.DataFrame(data=personaldata, columns=data_store_columns), ws=ws)
wb.save(write_excel)

elapsed = (time.time() - start)/3600
print(f"Elapsed time: {elapsed} hours")
