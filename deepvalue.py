import pandas as pd
from sstools import *

df1 = csv_to_df('csv/statusinvest.csv')
df2 = csv_to_df('csv/investsite.csv')
df3 = csv_to_df('csv/fundamentus.csv')

df=pd.concat([df1,df2,df3],axis=1, ignore_index=True)
df=rec_jud(df)

df1,df2,df3=df.iloc[0:,:6],df.iloc[0:,6:12],df.iloc[0:,12:]
df1,df2,df3=df1.rename(columns={0:'Empresa', 1:'Ticker', 2:'Cotação', 3:'EV/EBIT', 4:'M.EBIT', 5:'Vol.(Mi)'}),df2.rename(columns={7:'Empresa', 8:'Ticker', 9:'Cotação', 10:'EV/EBIT', 11:'M.EBIT', 12:'Vol.(Mi)'}),df3.rename(columns={14:'Empresa', 15:'Ticker', 16:'Cotação', 17:'EV/EBIT', 18:'M.EBIT', 19:'Vol.(Mi)'})
df1,df2,df3=filter(df1,'Empresa'),filter(df2,'Empresa'),filter(df3,'Empresa')

df_new=pd.DataFrame({'Empresa':df[0], 'Ticker':df[1], 'Cotação':round((df[2]+df[9]+df[16])/3,2), 'EV/EBIT':round((df[3]+df[10]+df[17])/3,2), 'M.EBIT':round((df[4]+df[11]+df[18])/3,2), 'Vol.(Mi)':round((df[5]+df[12]+df[19])/3,2)})

df_new=filter(df_new,'Empresa')

#### OUTPUT Files ####
csv_save(df1,'main_test')
df1.to_csv("deepvalue_statusinv.csv",index=False)
shutil.move('deepvalue_statusinv.csv', 'csv/dv_statusinv.csv')
df2.to_csv("deepvalue_fundamentus.csv",index=False)
shutil.move('deepvalue_fundamentus.csv', 'csv/dv_fundamentus.csv')
df3.to_csv("deepvalue_investsite.csv",index=False)
shutil.move('deepvalue_investsite.csv', 'csv/dv_investsite.csv')
df_new.to_csv("deepvalue_filtered.csv",index=False)
shutil.move('deepvalue_filtered.csv', 'csv/dv_filtered.csv')
#### OUTPUT SCREEN ####
bar = pd.DataFrame({'| | | ':40*['| | | ']})
print('\n    statusinvest.com.br                          | | |   fundamentus.com.br                          | | |    investsite.com.br                          | | |   Em comun nos 3 sites')
print('-------------------------------------------------| | |-----------------------------------------------| | |-----------------------------------------------| | |------------------------------------')
print(pd.concat([df1, bar, df2, bar, df3, bar, df_new], axis=1).head(20))
print('-------------------------------------------------| | |-----------------------------------------------| | |-----------------------------------------------| | |------------------------------------')
print(pd.concat([df1, ' '+bar, df2, bar, df3, bar, df_new], axis=1)[20:40])
