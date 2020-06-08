import pandas as pd
import openpyxl
import pickle
from others import create_excel_file, print_df_to_excel


with open('./GSauthorduplicate1.pkl', 'rb') as handle:
    data_store = pickle.load(handle)
df = pd.DataFrame(data=data_store[1], columns=data_store[0])

with open('./GSauthorduplicate107.pkl', 'rb') as handle:
    data_store = pickle.load(handle)
df2 = pd.DataFrame(data=data_store[1], columns=data_store[0])

with open('./GSauthorduplicate118.pkl', 'rb') as handle:
    data_store = pickle.load(handle)
df3 = pd.DataFrame(data=data_store[1], columns=data_store[0])

with open('./GSauthorduplicate126.pkl', 'rb') as handle:
    data_store = pickle.load(handle)
df4 = pd.DataFrame(data=data_store[1], columns=data_store[0])

with open('./GSauthorduplicate130.pkl', 'rb') as handle:
    data_store = pickle.load(handle)
df5 = pd.DataFrame(data=data_store[1], columns=data_store[0])

with open('./GSauthorduplicate132.pkl', 'rb') as handle:
    data_store = pickle.load(handle)
df6 = pd.DataFrame(data=data_store[1], columns=data_store[0])

with open('./GSauthorduplicate143.pkl', 'rb') as handle:
    data_store = pickle.load(handle)
df7 = pd.DataFrame(data=data_store[1], columns=data_store[0])

with open('./GSauthorduplicate222.pkl', 'rb') as handle:
    data_store = pickle.load(handle)
df8 = pd.DataFrame(data=data_store[1], columns=data_store[0])

with open('./GSauthorduplicate268.pkl', 'rb') as handle:
    data_store = pickle.load(handle)
df9 = pd.DataFrame(data=data_store[1], columns=data_store[0])


personaldata = df
personaldata = personaldata.append(df2)
personaldata = personaldata.append(df3)
personaldata = personaldata.append(df4)
personaldata = personaldata.append(df5)
personaldata = personaldata.append(df6)
personaldata = personaldata.append(df7)
personaldata = personaldata.append(df8)
personaldata = personaldata.append(df9)



data_store_columns = ['Name', 'Total Citations', 'Total Citations (5 years)', 'h-index', 'h-index (5 years)',
                      'i10-index', 'i10-index (5 years)', 'Journal Authors', 'Journal Titles', 'Journal Names',
                      'Journal Years', 'Number of publications', 'Probability of correct profile']

with open('GSauthorduplicateComplete.pkl', 'wb') as handle:
    pickle.dump([data_store_columns, personaldata.values], handle, protocol=pickle.HIGHEST_PROTOCOL)

write_excel = create_excel_file('./results/{}_results.xlsx'.format('GSauthorduplicateComplete'))
wb = openpyxl.load_workbook(write_excel)
ws = wb[wb.sheetnames[-1]]
print_df_to_excel(df=pd.DataFrame(data=personaldata, columns=data_store_columns), ws=ws)
wb.save(write_excel)
