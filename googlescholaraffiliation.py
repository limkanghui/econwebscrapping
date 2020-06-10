from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
import time, pickle
from others import create_excel_file, print_df_to_excel
import random
import requests
from fake_useragent import UserAgent
from stem import Signal
from stem.control import Controller

# First index is 1, index is number of current authors
indextostart = 1664

start = time.time()

headers = {'User-Agent': UserAgent().random}
proxies = {
    'http': 'socks5://127.0.0.1:9150',
    'https': 'socks5://127.0.0.1:9150'
}

with open('./IDEASdataComplete.pkl', 'rb') as handle:
    data_store = pickle.load(handle)
df = pd.DataFrame(data=data_store[1], columns=data_store[0])

data_store_columns = ['Name', 'Title', 'Email']

numberofauthors = len(df['name'])
personaldata = []
authorsduplicate = []


for authors in range(numberofauthors - indextostart + 1):

    name = df['name'][authors + indextostart - 1]
    print('Scrapping for {}...'.format(name))

    personaldetails = []

    namesplit = name.split()
    search = namesplit[0]
    for i in range(1, len(namesplit)):
        search += '+' + namesplit[i]
    URL = 'https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors={}&btnG='.format(search)

    # random time lag for requests
    random.seed(1)
    sleeptimerandom = 3 * random.random()
    if sleeptimerandom < 0.6:
        sleeptimerandom + 0.6
    time.sleep(sleeptimerandom)

    # Get new IP address
    #with Controller.from_port(port=9151) as c:
    #    c.authenticate()
    #    c.signal(Signal.NEWNYM)

    page = requests.get(URL, proxies=proxies, headers=headers)

    # reconnect if page can't be reached
    while True:
        if page.ok:
            soup = BeautifulSoup(page.content, 'html.parser')
            IPaddress = requests.get('https://ident.me', proxies=proxies).text
            print("Connection Successful with {}".format(IPaddress))
            break
        else:
            with Controller.from_port(port=9151) as c:
                c.authenticate()
                c.signal(Signal.NEWNYM)
            page = requests.get(URL, proxies=proxies, headers=headers)
            IPaddress = requests.get('https://ident.me', proxies=proxies).text
            print('Connection failed, retrying with {}...'.format(IPaddress))


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
        urltoprofile = div.a['href']
        URLofprofile = 'https://scholar.google.com{}'.format(urltoprofile)

        # Get new IP address
       #with Controller.from_port(port=9151) as c:
       #    c.authenticate()
       #    c.signal(Signal.NEWNYM)
        url100 = '{}&cstart=0&pagesize=100'.format(URLofprofile)
        page = requests.get(url100, proxies=proxies, headers=headers)

        # reconnect if page can't be reached
        while True:
            if page.ok:
                soup = BeautifulSoup(page.content, 'html.parser')
                IPaddress = requests.get('https://ident.me', proxies=proxies).text
                print("Connection Successful with {}".format(IPaddress))
                break
            else:
                with Controller.from_port(port=9151) as c:
                    c.authenticate()
                    c.signal(Signal.NEWNYM)
                page = requests.get(url100, proxies=proxies, headers=headers)
                IPaddress = requests.get('https://ident.me', proxies=proxies).text
                print('Connection failed, retrying with {}...'.format(IPaddress))

        affiliationtable = soup.find('div', attrs={'class': 'gsc_prf_il'})
        title = affiliationtable.text
        #print(title)
        verifiedemail = soup.find('div', attrs={'id': 'gsc_prf_ivh'})
        email = verifiedemail.text

    else:
        title = 'NA'
        email = 'NA'

    personaldetails.append(name)
    personaldetails.append(title)
    personaldetails.append(email)

    personaldata.append(personaldetails)

    with open('GSaffiliationscrap{}.pkl'.format(indextostart), 'wb') as handle:
        pickle.dump([data_store_columns, personaldata], handle, protocol=pickle.HIGHEST_PROTOCOL)

    print('Progress: {} out of {} for {} done'.format(authors + indextostart, numberofauthors, name))

    #if authors > 3:
    #    break


write_excel = create_excel_file('./results/{}_results.xlsx'.format('GSAffiliationScrap'))
wb = openpyxl.load_workbook(write_excel)
ws = wb[wb.sheetnames[-1]]
print_df_to_excel(df=pd.DataFrame(data=personaldata, columns=data_store_columns), ws=ws)
wb.save(write_excel)


elapsed = (time.time() - start) / 3600
print(f"Elapsed time: {elapsed} hours")