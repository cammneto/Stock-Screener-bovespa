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

def low_vol(df):
    df.drop(df[df[5] < 0.2].index, inplace = True)
    df.drop(df[df[12] < 0.2].index, inplace = True)
    df.drop(df[df[19] < 0.2].index, inplace = True)
    return df

def ebit_margin(df):
    df.drop(df[df[4] < 0].index, inplace = True)
    df.drop(df[df[11] < 0].index, inplace = True)
    df.drop(df[df[18] < 0].index, inplace = True)
    return df

def neg_ebit(df):
    df.drop(df[df[3] < 0].index, inplace = True)
    df.drop(df[df[10] < 0].index, inplace = True)
    df.drop(df[df[17] < 0].index, inplace = True)
    return df

def higher_liq(df):
    df=df.sort_values(by=[0,5]).reset_index(drop=True)
    for i in range(1,len(df[0])):
        if df[0][i-1]==df[0][i]:
            remove=df[1][i-1]
            df=df[df[1].str.contains(remove)==False]
        else:
            pass
    return df

def earning_y(df):
    df=df.sort_values(by=['EV/EBIT'])
    df['EV/EBIT']=df['EV/EBIT']
    df=df.drop('Empresa',axis=1)
    df=df.reset_index(drop=True)
    return df
