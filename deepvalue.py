import pandas as pd
from tabulate import tabulate
from sstools import *

df1 = csv_to_df('csv/statusinvest.csv')
df2 = csv_to_df('csv/investsite.csv')
df3 = csv_to_df('csv/fundamentus.csv')
#print(df1),print(df2),print(df3)

df=pd.concat([df1,df2,df3],axis=1, ignore_index=True)
df=rec_jud(df)

df=low_vol(df)
df=ebit_margin(df)

df1,df2,df3=df.iloc[0:,:6],df.iloc[0:,6:12],df.iloc[0:,12:]
df1,df2,df3=df1.rename(columns={0:'Empresa', 1:'Ticker', 2:'Price', 3:'E.Y.', 4:'M.EBIT', 5:'Vol.(Mi)'}),df2.rename(columns={7:'Empresa', 8:'Ticker', 9:'Price', 10:'E.Y.', 11:'M.EBIT', 12:'Vol.(Mi)'}),df3.rename(columns={14:'Empresa', 15:'Ticker', 16:'Price', 17:'E.Y.', 18:'M.EBIT', 19:'Vol.(Mi)'})
df1,df2,df3=higher_liq(df1),higher_liq(df2),higher_liq(df3)
df_new=pd.DataFrame({'Empresa':df[0], 'Ticker':df[1], 'Price':round((df[2]+df[9]+df[16])/3,2), 'E.Y.':round((df[3]+df[10]+df[17])/3,2), 'M.EBIT':round((df[4]+df[11]+df[18])/3,2), 'Vol.(Mi)':round((df[5]+df[12]+df[19])/3,2)})
df_new=higher_liq(df_new)

### OUTPUT Files ####
df1.to_csv("dv_statusinv.csv",index=False), shutil.move('dv_statusinv.csv', 'csv/dv_statusinv.csv')
df2.to_csv("dv_investsite.csv",index=False), shutil.move('dv_investsite.csv', 'csv/dv_investsite.csv')
df3.to_csv("dv_fundamentus.csv",index=False), shutil.move('dv_fundamentus.csv', 'csv/dv_fundamentus.csv')
df_new.to_csv("dv_crossed.csv",index=False), shutil.move('dv_crossed.csv', 'csv/dv_crossed.csv')
#### OUTPUT SCREEN ####
rank = pd.concat([df1.iloc[0:,:4], df2.iloc[0:,:4], df3.iloc[0:,:4], df_new.iloc[0:,:4]], axis=1)
rank.index = rank.index +1

print('--  ---------- Status Invest ----------  ----------- Investsite ------------  ----------- Fundamentus -----------  ---------- 3 Sites Mean -----------')
print(tabulate(rank.head(20), headers='keys', floatfmt=".2f"))#, tablefmt='plain'))
print('--  -----------------------------------  -----------------------------------  -----------------------------------  -----------------------------------')
print(tabulate(rank[20:30], headers='keys', floatfmt=".2f"))#, tablefmt='plain'))
print('--  -----------------------------------  -----------------------------------  -----------------------------------  -----------------------------------')
print(tabulate(rank[30:40], headers='keys', floatfmt=".2f"))#, tablefmt='plain'))

