import pandas as pd
import datetime

# import csv file with stocks data
df = pd.read_csv('output.csv')
# header for the data frame
header = ['Empresa', 'Ticker', 'Cotação', 'EV/EBIT', 'M. EBIT', 'Volume Diário', 'Situação']
# Remove all NaN (not a number) that comes in csv file
df=df.dropna().reset_index(drop=True)
# convert string columns into float columns
col4 = df['EV/EBIT']/100
col5 = [i.replace(',','.').replace('%','') for i in df['Margem EBIT']]
col6 = [float(i.replace(',','').replace('R$ ','').replace(' B','0000000').replace(' M','0000').replace(' mil','0')) for i in df['Volume Diário']]
# Create an empty data frame to store the new numeric columns
df1=pd.DataFrame([],columns=header)
# merge nem numeric columns with string ones
df1[header[0]],df1[header[1]],df1[header[2]],df1[header[3]],df1[header[4]],df1[header[5]],df1[header[6]]=df['Empresa'],df['Ticker'],df['Cotação'],col4,col5,col6,df['Situação']
# reveal possible NaNs
df1[header[3]] = df1[header[3]].apply(pd.to_numeric, errors='coerce')
df1[header[5]] = df1[header[5]].apply(pd.to_numeric, errors='coerce')
df1[header[4]] = df1[header[4]].apply(pd.to_numeric, errors='coerce')
# remove the possible NaNs
df1=df1.dropna().reset_index(drop=True)
# remove all stocks lower than R$ 200K of traded volume
df1.drop(df1[df1['Volume Diário'] < 200000].index, inplace = True)
# remove all companies with EBIT margin lower than 0
df1.drop(df1[df1['M. EBIT'] < 0].index, inplace = True)
# sort stocks from lower to higher EV/EBIT
df1=df1.sort_values(by=['EV/EBIT','Ticker'])
df1['EV/EBIT'] = round(df1['EV/EBIT'],2)
# Remove all companies in voluntary arrangement
df1=df1[df1["Situação"].str.contains('JUDICIAL')==False].reset_index(drop=True)
# For companies with more than 1 ticker remove the ones with lower daily volume
for i in range(1,50):
    if df1['Empresa'][i-1]==df1['Empresa'][i]:
        remover=df1['Ticker'][i-1]
        df1=df1[df1["Ticker"].str.contains(remover)==False]
    else:
        pass
# Reset indexes
df1=df1.reset_index(drop=True)
# print first 50 stocks from lower to higher EV/EBIT on screen
print(df1.head(40))
# Write the data to an output csv file
df1.to_csv("deepvalue-output.csv",index=False)
# Write a backup csv file with current date
today = str(datetime.datetime.now().date())
df1.to_csv('deepvalue-output-' + today + ".csv",index=False)