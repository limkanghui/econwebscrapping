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
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# First index is 1, index is number of current authors
indextostart = 1

start = time.time()

headers = {'User-Agent': UserAgent().random}
proxies = {
    'http': 'socks5://127.0.0.1:9150',
    'https': 'socks5://127.0.0.1:9150'
}

with open('./DuplicateAuthorsComplete.pkl', 'rb') as handle:
    data_store = pickle.load(handle)
df = pd.DataFrame(data=data_store[1], columns=data_store[0])

with open('./IDEASaffiliationComplete.pkl', 'rb') as handle:
    data_store = pickle.load(handle)
df2 = pd.DataFrame(data=data_store[1], columns=data_store[0])

data_store_columns = ['Name', 'Total Citations', 'Total Citations (5 years)', 'h-index', 'h-index (5 years)',
                      'i10-index', 'i10-index (5 years)', 'Journal Authors', 'Journal Titles', 'Journal Names',
                      'Journal Years', 'Number of publications', 'Probability of correct profile', 'Keywords match',
                      'Title', 'Email']

numberofauthors = len(df['Names'])
personaldata = []
keywords = 'labor economics industrial organization Monetaria Financiera monetary financial'

for authors in range(numberofauthors - indextostart + 1):

    name = df['Names'][authors + indextostart - 1]
    #name = 'Julio Cesar Arteaga'
    print('Scrapping for {}...'.format(name))

    namesplit = name.split()
    search = namesplit[0]
    for i in range(1, len(namesplit)):
        search += '+' + namesplit[i]
    URL = 'https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors="{}"&btnG='.format(search)

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
#
    page = requests.get(URL, proxies=proxies, headers=headers)

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
    GSperfectmatchprofile = True
    div = soup.find('div', attrs={'id': 'gsc_sa_ccl'})
    try:
        textsearch = div.p.text
        GSperfectmatchprofile = False
    except AttributeError:
        pass
    URLs = []
    #print('perfectmatch == {}'.format(GSperfectmatchprofile))
    if GSperfectmatchprofile:
        div = soup.find('div', attrs={'id': 'gsc_sa_ccl'})
        numberofprofilessearched = 0
        score = []
        for row in div.find_all('div', attrs={'class': 'gsc_1usr'}):
            profiletext = row.find('div', attrs={'class': 'gs_ai_aff'})
            researchinterests = row.find('div', attrs={'class': 'gs_ai_int'})
            profilewords = profiletext.text + ' ' + researchinterests.text
            #print(profilewords)
            keywords2 = df2.loc[df2['name'] == name, 'affiliation'].iloc[0]
            score.append(0.4 * fuzz.partial_token_sort_ratio(keywords, profilewords) + 0.6 *
                         fuzz.partial_token_sort_ratio(keywords2, profilewords))
            numberofprofilessearched += 1
            urltoprofile = row.a['href']
            URLs.append(urltoprofile)
        #print(score)
        maxIndex, maxValue = max(enumerate(score), key=lambda v: v[1])
        URLofprofile = 'https://scholar.google.com{}'.format(URLs[maxIndex])
        #if 'disabled' not in soup.find('button', arial='Next').attrs:
        probabilityprofilecorrect = 1 / numberofprofilessearched
    else:
        URL = 'https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors={}&btnG='.format(search)

        # random time lag for requests
        random.seed(1)
        sleeptimerandom = 3 * random.random()
        if sleeptimerandom < 0.6:
            sleeptimerandom + 0.6
        time.sleep(sleeptimerandom)

        # Get new IP address
        # with Controller.from_port(port=9151) as c:
        #    c.authenticate()
        #    c.signal(Signal.NEWNYM)
        #
        page = requests.get(URL, proxies=proxies, headers=headers)

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

        div = soup.find('div', attrs={'id': 'gsc_sa_ccl'})
        numberofprofilessearched = 0
        score = []
        for row in div.find_all('div', attrs={'class': 'gsc_1usr'}):
            profiletext = row.find('div', attrs={'class': 'gs_ai_aff'})
            researchinterests = row.find('div', attrs={'class': 'gs_ai_int'})
            profilewords = profiletext.text + ' ' + researchinterests.text
            keywords2 = df2.loc[df2['name'] == name, 'affiliation'].iloc[0]
            score.append(0.4 * fuzz.partial_token_sort_ratio(keywords, profilewords) + 0.6 *
                         fuzz.partial_token_sort_ratio(keywords2, profilewords))
            numberofprofilessearched += 1
            urltoprofile = row.a['href']
            URLs.append(urltoprofile)
        maxIndex, maxValue = max(enumerate(score), key=lambda v: v[1])
        URLofprofile = 'https://scholar.google.com{}'.format(URLs[maxIndex])
        # if 'disabled' not in soup.find('button', arial='Next').attrs:
        probabilityprofilecorrect = 1 / numberofprofilessearched


    # Get citations etc.

    personaldetails = []

    #with Controller.from_port(port=9151) as c:
    #    c.authenticate()
    #    c.signal(Signal.NEWNYM)
    url100 = '{}&cstart=0&pagesize=100'.format(URLofprofile)

    page = requests.get(url100, proxies=proxies, headers=headers)
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
            page = requests.get(URLofprofile, proxies=proxies, headers=headers)
            IPaddress = requests.get('https://ident.me', proxies=proxies).text
            print('Connection failed, retrying with {}...'.format(IPaddress))
    # Check if citation table exists
    citationtableexists = True
    table = soup.find('table', attrs={'id': 'gsc_rsb_st'})
    try:
        td = table.find('td', attrs={'class': 'gsc_rsb_std'})
    except AttributeError:
        citationtableexists = False
        pass
    # print(soup.prettify())
    citationcounts = []
    journalextracteddata = []
    journalyeardata = []
    journalname = []
    #print(URLofprofile)
    if citationtableexists:
        citationtable = soup.find('table', attrs={'id': 'gsc_rsb_st'})
        for td in citationtable.find_all('td', attrs={'class': 'gsc_rsb_std'}):
            citationcounts.append(td.text)
    pubstart = 0
    while True:
        for row in soup.find_all('tr', class_='gsc_a_tr'):
            journalextracted = []
            #print(row.prettify())
            journaldata = row.find('td', class_='gsc_a_t')
            a = journaldata.find('a')
            journalname.append(a.text)
            for div in journaldata.find_all('div', recursive=False):
                if len(journalextracted) == 2:
                    break
                journalextracted.append(div.text)
            journalextracteddata.append(journalextracted[0])
            journalextracteddata.append(journalextracted[1])
            journalyear = row.find('td', class_='gsc_a_y')
            journalyeardata.append(journalyear.text)
        if 'disabled' not in soup.find('button', id='gsc_bpf_more').attrs:
            pubstart += 100
            URLofprofile = '{0}&cstart={1}&pagesize=100'.format(
                URLofprofile, pubstart)
            #with Controller.from_port(port=9151) as c:
            #    c.authenticate()
            #    c.signal(Signal.NEWNYM)
            page = requests.get(URLofprofile, proxies=proxies, headers=headers)
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
                    page = requests.get(URLofprofile, proxies=proxies, headers=headers)
                    IPaddress = requests.get('https://ident.me', proxies=proxies).text
                    print('Connection failed, retrying with {}...'.format(IPaddress))
        else:
            break
    for row in soup.find_all('tr', class_='gsc_a_tr'):
        journalextracted = []
        #print(row.prettify())
        journaldata = row.find('td', class_='gsc_a_t')
        a = journaldata.find('a')
        journalname.append(a.text)
        for div in journaldata.find_all('div', recursive=False):
            if len(journalextracted) == 2:
                break
            journalextracted.append(div.text)
        journalextracteddata.append(journalextracted[0])
        journalextracteddata.append(journalextracted[1])
        journalyear = row.find('td', class_='gsc_a_y')
        journalyeardata.append(journalyear.text)
    if citationtableexists:
        totalcitations = citationcounts[0]
        totalcitations5y = citationcounts[1]
        hindex = citationcounts[2]
        hindex5y = citationcounts[3]
        i10index = citationcounts[4]
        i10index5y = citationcounts[5]
    else:
        totalcitations = 'na'
        totalcitations5y = 'na'
        hindex = 'na'
        hindex5y = 'na'
        i10index = 'na'
        i10index5y = 'na'
    GStitle = ''
    GSAuthors = ''
    GSjournalname = ''
    GSyear = ''
    for i in range(0, len(journalname)):
        GStitle += '{}) '.format(i + 1) + journalname[i] + '\n'
        GSyear += '{}) '.format(i + 1) + journalyeardata[i] + '\n'
    for i in range(0, len(journalname)):
        GSAuthors += '{}) '.format(i + 1) + journalextracteddata[i * 2] + '\n'
    for i in range(0, len(journalname)):
        GSjournalname += '{}) '.format(i + 1) + journalextracteddata[i * 2 + 1] + '\n'
    numberofpublicationsfromGS = len(journalname)
    personaldetails.append(name)
    personaldetails.append(totalcitations)
    personaldetails.append(totalcitations5y)
    personaldetails.append(hindex)
    personaldetails.append(hindex5y)
    personaldetails.append(i10index)
    personaldetails.append(i10index5y)
    personaldetails.append(GSAuthors)
    personaldetails.append(GStitle)
    personaldetails.append(GSjournalname)
    personaldetails.append(GSyear)
    personaldetails.append(numberofpublicationsfromGS)
    personaldetails.append(probabilityprofilecorrect)
    personaldetails.append(maxValue)

    # get affiliationdata
    affiliationtable = soup.find('div', attrs={'class': 'gsc_prf_il'})
    title = affiliationtable.text
    # print(title)
    verifiedemail = soup.find('div', attrs={'id': 'gsc_prf_ivh'})
    email = verifiedemail.text

    personaldetails.append(title)
    personaldetails.append(email)

    personaldata.append(personaldetails)
    with open('GSauthorduplicate{}.pkl'.format(indextostart), 'wb') as handle:
        pickle.dump([data_store_columns, personaldata], handle, protocol=pickle.HIGHEST_PROTOCOL)

    print('Progress: {} out of {} for {} done'.format(authors + indextostart, numberofauthors, name))

    #if authors > 3:
    #    break


write_excel = create_excel_file('./results/{}_results.xlsx'.format('GSauthorduplicate'))
wb = openpyxl.load_workbook(write_excel)
ws = wb[wb.sheetnames[-1]]
print_df_to_excel(df=pd.DataFrame(data=personaldata, columns=data_store_columns), ws=ws)
wb.save(write_excel)

elapsed = (time.time() - start) / 3600
print(f"Elapsed time: {elapsed} hours")