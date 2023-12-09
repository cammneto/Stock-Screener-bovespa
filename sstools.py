import pandas as pd

def tickers(InputFile):
    infile = open(InputFile, "r")
    tickers = [line.split() for line in infile]
    ticker = []
    for i in tickers:
        ticker.append(i[0])
    return ticker

def csv_to_df(df):
    # Converte os dados de strings pra float
    df = pd.read_csv(df)
    df['Cotação'] = df['Cotação'].apply(pd.to_numeric, errors='coerce')
    df['EV/EBIT'] = round(df['EV/EBIT'].apply(pd.to_numeric, errors='coerce'),2)
    df['M.EBIT']  = df['M.EBIT'].apply(pd.to_numeric, errors='coerce')
    df['Volume Médio']  = round(df['Volume Médio'].apply(pd.to_numeric, errors='coerce')/10**6,2)
    df=df.rename(columns = {'Volume Médio': 'Vol.(Mi)'}, inplace = False)
    return df

def rec_jud(df):#Remove empresas em recuperação judicial
#    df=df[df[6].str.contains('JUDICIAL')==False].reset_index(drop=True) #fonte statusinvest
    df=df[df[13].str.contains('JUDICIAL')==False].reset_index(drop=True) #fonte investsite
    df=df.dropna().reset_index(drop=True)
    df=df.drop([6,13],axis=1)
    return df

def low_vol(df,vol):#Remove empresas com liquidez média diária menor que R$ 200000,00
#    df.drop(df[df[5] < vol].index, inplace = True)  #fonte status invest (média 1 mês)
#    df.drop(df[df[19] < vol].index, inplace = True) #fonte fundamentus (média 2 meses)
    df.drop(df[df[12] < vol].index, inplace = True) #fonte investsite (média 3 meses)
    return df

def neg_ebit(df):#Remove empresas com EBIT e margem EBIT negativos
    df.drop(df[df[3] < 0].index, inplace = True) #fonte statusinvest
    df.drop(df[df[4] < 0].index, inplace = True) #fonte statusinvest
    df.drop(df[df[10] < 0].index, inplace = True) #fonte investsite
    df.drop(df[df[11] < 0].index, inplace = True) #fonte investsite
    df.drop(df[df[17] < 0].index, inplace = True) #fonte fundamentus
    df.drop(df[df[18] < 0].index, inplace = True) #fonte fundamentus
    return df

def higher_liq(df):#Organiza por empresa e liquidez removendo os tickers de menor liquidez de uma mesma empresa
    df=df.sort_values(by=[0,5]).reset_index(drop=True)
    for i in range(1,len(df[0])):
        if df[0][i-1]==df[0][i]:
            remove=df[1][i-1]
            df=df[df[1].str.contains(remove)==False]
        else:
            pass
    return df

def earnings_yield(df): #Organiza em ordem crescente de EV/EBIT (ivnerso do eranings yield) e remove a coluna com nome das empresas pra facilitar a visialização na tela
    df=df.sort_values(by=['EV/EBIT'])
    df['EV/EBIT']=df['EV/EBIT']
    df=df.drop('Empresa',axis=1)
    df=df.reset_index(drop=True)
    return df
