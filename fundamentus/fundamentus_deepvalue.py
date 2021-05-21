import pandas as pd
import datetime

# Build a data frame with the csv data
df = pd.read_csv('output.csv')
# change columns to numeric to find NaN values
df['Cotação']       = df['Cotação'].apply(pd.to_numeric, errors='coerce')
df['EV/EBIT']       = df['EV/EBIT'].apply(pd.to_numeric, errors='coerce')
df['M.EBIT']        = df['M.EBIT'].apply(pd.to_numeric, errors='coerce')
df['Volume Médio']  = df['Volume Médio'].apply(pd.to_numeric, errors='coerce')
# Delete rows with any NaN value
df=df.dropna()
# Delete any row with daily volume lower than R$ 200 000.00
df.drop(df[df['Volume Médio'] < 200000].index, inplace = True)
# Delete any row with negative EBIT margin
df.drop(df[df['M.EBIT'] < 0].index, inplace = True)
# Delete company in voluntary arrangement
df=df[df['Situação Judicial'].str.contains('JUDICIAL')==False]
# Delete stock with lower daily volume from the same company
df=df.sort_values(by=['Empresa','Volume Médio']).reset_index(drop=True)
for i in range(1,len(df['Empresa'])):
    if df['Empresa'][i-1]==df['Empresa'][i]:
        remover=df['Ticker'][i-1]
        #print(remover)
        df=df[df['Ticker'].str.contains(remover)==False]
    else:
        pass
# Sort Columns by EV/EBIT, Company name and daily volume
df=df.sort_values(by=['EV/EBIT'])#,'Empresa','Volume Médio'])
# Reset dataframe index
df=df.reset_index(drop=True)
# Print first 50 rows
print(df.head(50))
# Save data to a csv file
df.to_csv('deepvalue-fundamentus.csv',index=False)
# Write a backup csv file with current date
today = str(datetime.datetime.now().date())
df.to_csv('deepvalue-fundamentus-' + today + ".csv",index=False)
