import pandas as pd
from tabulate import tabulate
from sstools import *

df1 = csv_to_df('csv/statsinvst.csv')
df2 = csv_to_df('csv/investsite.csv')
df3 = csv_to_df('csv/fundaments.csv')
#print(df1),print(df2),print(df3)

df=pd.concat([df1,df2,df3],axis=1, ignore_index=True)
df=rec_jud(df)

df=low_vol(df)
df=ebit_margin(df)
df=higher_liq(df)
df=neg_ebit(df)

df1,df2,df3=df.iloc[0:,:6],df.iloc[0:,6:12],df.iloc[0:,12:]
df1,df2,df3=df1.rename(columns={0:'Empresa', 1:'Ticker', 2:'Price', 3:'EV/EBIT', 4:'M.EBIT', 5:'Vol.(Mi)'}),df2.rename(columns={7:'Empresa', 8:'Ticker', 9:'Price', 10:'EV/EBIT', 11:'M.EBIT', 12:'Vol.(Mi)'}),df3.rename(columns={14:'Empresa', 15:'Ticker', 16:'Price', 17:'EV/EBIT', 18:'M.EBIT', 19:'Vol.(Mi)'})
df_new=pd.DataFrame({'Empresa':df[0], 'Ticker':df[1], 'Price':df[9], 'EV/EBIT':(df[3]+df[10]+df[17])/3, 'M.EBIT':(df[4]+df[11]+df[18])/3, 'Vol.(Mi)':(df[5]+df[12]+df[19])/3})
df1,df2,df3 = earning_y(df1),earning_y(df2),earning_y(df3)
df_new = earning_y(df_new)
### OUTPUT Files ####
df1.to_csv   ("dv_statsinvst.csv",index=False), shutil.move('dv_statsinvst.csv', 'csv/dv_statsinvst.csv')
df2.to_csv   ("dv_investsite.csv",index=False), shutil.move('dv_investsite.csv', 'csv/dv_investsite.csv')
df3.to_csv   ("dv_fundaments.csv",index=False), shutil.move('dv_fundaments.csv', 'csv/dv_fundaments.csv')
df_new.to_csv("dv_df-average.csv",index=False), shutil.move('dv_df-average.csv', 'csv/dv_df-average.csv')
#### OUTPUT SCREEN ####
rank = pd.concat([df1.iloc[0:,[0,2]], df2.iloc[0:,[0,2]], df3.iloc[0:,[0,2]], df_new.iloc[0:,[0,2,1]]], axis=1)
rank.index = rank.index +1
print('-- | Status Invest  ||   Investsite   ||   Fundamentus  ||  3 Sites Avg   |  |Stock|')
print(tabulate(rank.head(20), headers='keys', floatfmt=".2f"))#, tablefmt='plain'))
print('--  ----------------  ----------------  ----------------  ----------------  -------')
print(tabulate(rank[20:30], headers='keys', floatfmt=".2f"))#, tablefmt='plain'))
print('--  ----------------  ----------------  ----------------  ----------------  -------')
print(tabulate(rank[30:45], headers='keys', floatfmt=".2f"))#, tablefmt='plain'))

