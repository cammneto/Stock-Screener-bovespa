import pandas as pd
import shutil
import numpy as np
def csv_to_numeric(csv_file):
    # Convert to numeric to turn strings into nan
    df = pd.read_csv(csv_file)
    df['Cotação'] = df['Cotação'].apply(pd.to_numeric, errors='coerce')
    df['EV/EBIT'] = round(df['EV/EBIT'].apply(pd.to_numeric, errors='coerce'),2)
    df['M.EBIT']  = df['M.EBIT'].apply(pd.to_numeric, errors='coerce')
    df['Volume Médio']  = round(df['Volume Médio'].apply(pd.to_numeric, errors='coerce')/10**6,2)
    df=df.rename(columns = {'Volume Médio': 'Vol.(Mi)'}, inplace = False)
    return df

def filter(df,drop_col):
    df=df.dropna().reset_index(drop=True)
    df.drop(df[df['Vol.(Mi)'] < 0.2].index, inplace = True)
    df.drop(df[df['EV/EBIT'] < 0].index, inplace = True)
    df.drop(df[df['M.EBIT'] < 0].index, inplace = True)
    df=df[df['Situação'].str.contains('JUDICIAL')==False].reset_index(drop=True)
    df=df.sort_values(by=['Empresa','Vol.(Mi)']).reset_index(drop=True)
    for i in range(1,len(df['Empresa'])):
        if df['Empresa'][i-1]==df['Empresa'][i]:
            remover=df['Ticker'][i-1]
            df=df[df['Ticker'].str.contains(remover)==False]
        else:
            pass
    df=df.sort_values(by=['EV/EBIT'])
    df=df.reset_index(drop=True)
    df=df.drop(drop_col,axis=1)
    return df

df1 = csv_to_numeric('csv/statusinvest.csv')
df2 = csv_to_numeric('csv/fundamentus.csv')
df3 = csv_to_numeric('csv/investsite.csv')
print(len(df1),len(df2),len(df3))
rows=[]
for i in range(len(df1.Ticker)):
    evebit= round(np.mean([df1['EV/EBIT'][i],df2['EV/EBIT'][i],df3['EV/EBIT'][i]]),2)
    margem= round(np.mean([df1['M.EBIT'][i],df2['M.EBIT'][i],df3['M.EBIT'][i]]),2)
    volume= round(np.mean([df1['Vol.(Mi)'][i],df2['Vol.(Mi)'][i],df3['Vol.(Mi)'][i]]),2)
    situac=df1['Situação'][i]+'/'+df2['Situação'][i]+'/'+df3['Situação'][i]
    row = [df1.Empresa[i],df1.Ticker[i],evebit,margem,volume,situac]
    rows.append(row)
df = pd.DataFrame(rows, columns= ['Empresa','Ticker', 'EV/EBIT', 'M.EBIT', 'Vol.(Mi)','Situação'])
df1 = filter(df1,['Empresa','Situação','Cotação'])
df2 = filter(df2,['Empresa','Situação','Cotação'])
df3 = filter(df3,['Empresa','Situação','Cotação'])
df  = filter(df ,['Empresa','Situação'])

def remove_eq(df1,df2):
    new_df=df1
    for i in df2.Ticker:
        new_df=new_df[new_df['Ticker'].str.contains(i)==False]
    return new_df
df1_2=remove_eq(df1,df2)
df1_3=remove_eq(df1,df3)
df2_1=remove_eq(df2,df1)
df2_3=remove_eq(df2,df3)
df3_1=remove_eq(df3,df1)
df3_2=remove_eq(df1,df2)
df_new=pd.concat([df1_2,df1_3,df2_1,df2_3,df3_1,df3_2], axis=0)
df=remove_eq(df,df_new).reset_index(drop=True)
df1=remove_eq(df1,df_new).reset_index(drop=True)
df2=remove_eq(df2,df_new).reset_index(drop=True)
df3=remove_eq(df3,df_new).reset_index(drop=True)
print(len(df1),len(df2),len(df3))

# OUTPUT Files ####
df1.to_csv("deepvalue_statusinv.csv",index=False)
shutil.move('deepvalue_statusinv.csv', 'csv/deepvalue_statusinv.csv')
df2.to_csv("deepvalue_fundamentus.csv",index=False)
shutil.move('deepvalue_fundamentus.csv', 'csv/deepvalue_fundamentus.csv')
df3.to_csv("deepvalue_investsite.csv",index=False)
shutil.move('deepvalue_investsite.csv', 'csv/deepvalue_investsite.csv')
df.to_csv("deepvalue_filtered.csv",index=False)
shutil.move('deepvalue_filtered.csv', 'csv/deepvalue_filtered.csv')
#### OUTPUT SCREEN ####
bar = pd.DataFrame({'| | | ':40*['| | | ']})
print('\n    statusinvest.com.br                | | |   fundamentus.com.br                 | | |   investsite.com.br                  | | |   Em comun nos 3 sites')
print('---------------------------------------| | |--------------------------------------| | |-------------------------------------| | |------------------------------------')
print(pd.concat([df1, bar, df2, bar, df3, bar, df], axis=1).head(20))
print('--------------------------------------| | |--------------------------------------| | |--------------------------------------| | |------------------------------------')
print(pd.concat([df1, bar, df2, bar, df3, bar, df], axis=1)[20:40])
