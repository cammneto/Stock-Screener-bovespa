import pandas as pd
from tabulate import tabulate
from sstools import *
import shutil

df1 = csv_to_df('csv/statsinvst.csv')
df2 = csv_to_df('csv/investsite.csv')
df3 = csv_to_df('csv/fundaments.csv')

if len(df1)==len(df2)==len(df3):
    pass
else:
    print('Fundamentus = ', len(df1), 'Investsite = ', len(df2), 'Status Invest = ', len(df3))

df=pd.concat([df1,df2,df3],axis=1, ignore_index=True)
df=rec_jud(df)
vol = float(input('Digite o limite de volume médio de transação diário em milhões de R$ (ex: para R$ 500mil digite 0.5)'))
df=low_vol(df,vol)
df=neg_ebit(df)
df=higher_liq(df)

df1,df2,df3=df.iloc[0:,:6],df.iloc[0:,6:12],df.iloc[0:,12:]
df1,df2,df3=df1.rename(columns={0:'Empresa', 1:'Ticker', 2:'Price', 3:'EV/EBIT', 4:'M.EBIT', 5:'Vol.(Mi)1m'}),df2.rename(columns={7:'Empresa', 8:'Ticker', 9:'Price', 10:'EV/EBIT', 11:'M.EBIT', 12:'Vol.(Mi)3m'}),df3.rename(columns={14:'Empresa', 15:'Ticker', 16:'Price', 17:'EV/EBIT', 18:'M.EBIT', 19:'Vol.(Mi)2m'})
df_new=pd.DataFrame({'Empresa':df[0], 'Ticker':df[1], 'Price':df[9], 'EV/EBIT':round((df[3]+df[10]+df[17])/3,2), 'M.EBIT':round((df[4]+df[11]+df[18])/3,2), 'Vol.(Mi)3m':df[12]})
df1,df2,df3 = earnings_yield(df1),earnings_yield(df2),earnings_yield(df3)
df_new = earnings_yield(df_new)
### OUTPUT Files ####
df1.to_csv   ("dv_statsinvst.csv",index=False), shutil.move('dv_statsinvst.csv', 'csv/dv_statsinvst.csv')
df2.to_csv   ("dv_investsite.csv",index=False), shutil.move('dv_investsite.csv', 'csv/dv_investsite.csv')
df3.to_csv   ("dv_fundaments.csv",index=False), shutil.move('dv_fundaments.csv', 'csv/dv_fundaments.csv')
df_new.to_csv("dv_df-average.csv",index=False), shutil.move('dv_df-average.csv', 'csv/dv_df-average.csv')
#### OUTPUT SCREEN ####
rank = pd.concat([df1.iloc[0:,[0,2,4]], df2.iloc[0:,[0,2,4]], df3.iloc[0:,[0,2,4]]], axis=1)#, df_new.iloc[0:,[0,2,1,4]]
rank.index = rank.index +1
print('--||---------------------------------||---------------------------------||---------------------------------|')
print('  ||          Status Invest          ||           Investsite            ||           Fundamentus           |')#'|                Average                |')
print('--||---------------------------------||---------------------------------||---------------------------------|')#' ----------------------------------------')
print(tabulate(rank.head(20), headers='keys', floatfmt=".2f"))#, tablefmt='plain'))
print('--||---------------------------------||---------------------------------||---------------------------------|')#' ----------------------------------------')
print(tabulate(rank[20:30], headers='keys', floatfmt=".2f"))#, tablefmt='plain'))
print('--||---------------------------------||---------------------------------||---------------------------------|')#' ----------------------------------------')
print(tabulate(rank[30:40], headers='keys', floatfmt=".2f"))#, tablefmt='plain'))

rank = df_new.iloc[0:,[0,2,1,4]]
rank.index = rank.index +1
print('|---------------------------------------------|')
print('|                   Average                   |')
print('|---------------------------------------------|')
print(tabulate(rank.head(20), headers='keys', floatfmt=".2f"))
print('|---------------------------------------------|')
print(tabulate(rank[20:30], headers='keys', floatfmt=".2f"))#, tablefmt='plain'))
print('|---------------------------------------------|')
print(tabulate(rank[30:], headers='keys', floatfmt=".2f"))#, tablefmt='plain'))
