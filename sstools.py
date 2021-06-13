import pandas as pd
import shutil

def csv_to_df(df):
    # Convert to numeric to turn strings into nan
    df = pd.read_csv(df)
    df['Cotação'] = df['Cotação'].apply(pd.to_numeric, errors='coerce')
    df['EV/EBIT'] = round(df['EV/EBIT'].apply(pd.to_numeric, errors='coerce'),2)
    df['M.EBIT']  = df['M.EBIT'].apply(pd.to_numeric, errors='coerce')
    df['Volume Médio']  = round(df['Volume Médio'].apply(pd.to_numeric, errors='coerce')/10**6,2)
    df=df.rename(columns = {'Volume Médio': 'Vol.(Mi)'}, inplace = False)
    return df

def rec_jud(df):
    df=df[df[6].str.contains('JUDICIAL')==False].reset_index(drop=True)
    df=df[df[13].str.contains('JUDICIAL')==False].reset_index(drop=True)
    df=df.dropna().reset_index(drop=True)
    df=df.drop([6,13],axis=1)
    return df

def filter(df,drop_col):
    df=df.dropna().reset_index(drop=True)
    df.drop(df[df['Vol.(Mi)'] < 0.2].index, inplace = True)
    df.drop(df[df['EV/EBIT'] < 0].index, inplace = True)
    df.drop(df[df['M.EBIT'] < 0].index, inplace = True)
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

def csv_save(df,file):
    df.to_csv("dv_"+file+".csv",index=False)
    shutil.move('dv_'+file+'.csv', 'csv/dv_'+file+'.csv')