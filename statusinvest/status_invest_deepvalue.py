import pandas as pd
import datetime

# Build a data frame with the csv data
df = pd.read_csv('output.csv')
# change columns to numeric to find NaN values
df['Cotação']       = df['Cotação'].apply(pd.to_numeric, errors='coerce')
df['EV/EBIT']       = df['EV/EBIT'].apply(pd.to_numeric, errors='coerce')
df['Margem EBIT']   = df['Margem EBIT'].apply(pd.to_numeric, errors='coerce')
df['Volume Diário'] = df['Volume Diário'].apply(pd.to_numeric, errors='coerce')
# Delete rows with any NaN value
df=df.dropna().reset_index(drop=True)
# Delete any row with daily volume lower than R$ 200 000.00
df.drop(df[df['Volume Diário'] < 200000].index, inplace = True)
# Delete any row with negative EBIT margin
df.drop(df[df['Margem EBIT'] < 0].index, inplace = True)
# Sort Columns by EV/EBIT, Company name and daily volume
df=df.sort_values(by=['EV/EBIT','Empresa','Volume Diário'])
# Delete company in voluntary arrangement
df=df[df['Situação'].str.contains('JUDICIAL')==False].reset_index(drop=True)
# Delete stock with lower daily volume from the same company
for i in range(1,50):
    if df['Empresa'][i-1]==df['Empresa'][i]:
        remover=df['Ticker'][i-1]
        print(remover)
        df=df[df['Ticker'].str.contains(remover)==False]
    else:
        pass
# Reset dataframe index
df=df.reset_index(drop=True)
# Print first 50 rows
print(df.head(50))
# Save data to a csv file
df.to_csv('output.csv',index=False)
# Write a backup csv file with current date
today = str(datetime.datetime.now().date())
df.to_csv('deepvalue-output-' + today + ".csv",index=False)
