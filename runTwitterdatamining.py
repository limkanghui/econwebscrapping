# Run this line in terminal:
# twitterscraper Trump -bd 2017-01-01 -ed 2017-06-01 -o tweets.json
# twitterscraper JustinWolfers --user -o tweets_JustinWolfers.json
# twitterscraper from:JustinWolfers --output=JustinWolfers.json
# twitterscraper from:JustinWolfers -bd 2011-07-01 -ed 2012-07-01 --output=JustinWolferspart1.json 5402
# twitterscraper from:JustinWolfers -bd 2012-07-01 -ed 2013-07-01 --output=JustinWolferspart2.json 5145
# twitterscraper from:JustinWolfers -bd 2013-07-01 -ed 2014-07-01 --output=JustinWolferspart3.json 4117
# twitterscraper from:JustinWolfers -bd 2014-07-01 -ed 2015-07-01 --output=JustinWolferspart4.json 3113
# twitterscraper from:JustinWolfers -bd 2015-07-01 -ed 2016-07-01 --output=JustinWolferspart5.json 2735
# twitterscraper from:JustinWolfers -bd 2016-07-01 -ed 2017-07-01 --output=JustinWolferspart6.json 3317
# twitterscraper from:JustinWolfers -bd 2017-07-01 -ed 2018-07-01 --output=JustinWolferspart7.json 1702
# twitterscraper from:JustinWolfers -bd 2018-07-01 -ed 2019-07-01 --output=JustinWolferspart8.json  ----error 1114
# twitterscraper from:JustinWolfers -bd 2019-07-01 -ed 2020-05-19 --output=JustinWolferspart9.json  ----error 1383
# twitterscraper from:JustinWolfers -bd 2011-07-01 -ed 2012-07-01 --output=JustinWolferspart1.json && twitterscraper from:JustinWolfers -bd 2012-07-01 -ed 2013-07-01 --output=JustinWolferspart2.json && twitterscraper from:JustinWolfers -bd 2013-07-01 -ed 2014-07-01 --output=JustinWolferspart3.json && twitterscraper from:JustinWolfers -bd 2014-07-01 -ed 2015-07-01 --output=JustinWolferspart4.json && twitterscraper from:JustinWolfers -bd 2015-07-01 -ed 2016-07-01 --output=JustinWolferspart5.json && twitterscraper from:JustinWolfers -bd 2016-07-01 -ed 2017-07-01 --output=JustinWolferspart6.json && twitterscraper from:JustinWolfers -bd 2017-07-01 -ed 2018-07-01 --output=JustinWolferspart7.json && twitterscraper from:JustinWolfers -bd 2018-07-01 -ed 2019-07-01 --output=JustinWolferspart8.json && twitterscraper from:JustinWolfers -bd 2019-07-01 -ed 2020-05-19 --output=JustinWolferspart9.json


import codecs, json
import pandas as pd
import openpyxl
from others import create_excel_file, print_df_to_excel

parts = 9

with codecs.open('JustinWolferspart{}.json'.format(1), 'r', 'utf-8') as f:
    tweets = json.load(f, encoding='utf-8')
df = pd.read_json('JustinWolferspart{}.json'.format(1), encoding='utf-8')
print(df)


for partnumber in range(2, parts+1, 1):
    with codecs.open('JustinWolferspart{}.json'.format(partnumber),'r','utf-8') as f:
        tweets = json.load(f, encoding='utf-8')
    dfread = pd.read_json('JustinWolferspart{}.json'.format(partnumber), encoding='utf-8')
    print(dfread)
    df = df.append(dfread)


name = 'JustinWolfers'
write_excel = create_excel_file('./results/{}_results.xlsx'.format(name))
wb = openpyxl.load_workbook(write_excel)
ws = wb[wb.sheetnames[-1]]
print_df_to_excel(df=df, ws=ws)
wb.save(write_excel)