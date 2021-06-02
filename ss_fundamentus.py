from lxml import html
import pandas as pd
import requests
import datetime
import shutil

# Read file with stocks tickers
def tickers(InputFile):
    infile = open(InputFile, "r")
    tickers = [line.split() for line in infile]
    ticker = []
    for i in tickers:
        ticker.append(i[0])
    return ticker

def page_tables(ticker):
    header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36","X-Requested-With": "XMLHttpRequest"}
    url  = 'https://fundamentus.com.br/detalhes.php?papel='+ticker
    page = requests.get(url, headers=header)
    # Get all the tables from the html content
    for p in page:
     try:
         tables = pd.read_html(page.content)
         return tables
     except ValueError:
         pass


def situacao(ticker):
    url = 'https://www.investsite.com.br/principais_indicadores.php?cod_negociacao='+ticker
    page = requests.get(url)
    # Get all the tables from the html content
    for p in page:
     try:
         tables = pd.read_html(page.content)
         db = [tables[1][0],tables[1][1]]
         print('Situação --->',db[1][3])
         situacao = db[1][3]
         return situacao
     except ValueError:
         pass

stocks = tickers('tickers.dat')
names,tickers,price,evebit,m_ebit,volume,sit=[],[],[],[],[],[],[]
for i in range(len(stocks)):
    tables = page_tables(stocks[i])
    print('Scraping',i+1, 'out of', len(stocks),'from: fundamentus.com.br')
    if tables==None:
        print('Ativo:',stocks[i])
        print('ERR 404: STOCK NOT FOUND')
        print('\n############################################################\n')
        pass
    else:
        names.append(tables[0][1][2].replace(' ON','').replace(' PNA','').replace(' PNB','').replace(' PN','').replace(' N1','').replace(' UNT','').replace(' N2','').replace(' NM',''))
        print('Empresa:',tables[0][1][2].replace(' ON','').replace(' PNA','').replace(' PNB','').replace(' PN','').replace(' N1','').replace(' UNT','').replace(' N2','').replace(' NM',''))
        tickers.append(stocks[i])
        print('Ativo:',stocks[i])
        price.append(float(tables[0][3][0])/100)
        print('Cotação --->',float(tables[0][3][0])/100)
        try:
            evebit.append(float(tables[2][3][10].replace('.',''))/100)
            print('EV/EBIT  --->',float(tables[2][3][10].replace('.',''))/100)
        except ValueError:
            evebit.append(float('nan'))
            print('EV/EBIT  --->',tables[2][3][10])
        try:
            m_ebit.append(float(tables[2][5][4].replace(',','.').replace('%','')))
            print('M. EBIT  --->',tables[2][5][4].replace(',','.').replace('%',''))
        except ValueError:
            m_ebit.append(float('nan'))
            print('M. EBIT  --->',tables[2][5][4].replace(',','.').replace('%',''))
        volume.append(float(tables[0][3][4].replace('.','')))
        print('Vol Méd  --->', float(tables[0][3][4].replace('.','')))
        sit.append(situacao(stocks[i]))
        print('\n############################################################\n')
# build a dataframe with data from all stocks
rows = {'Empresa':names, 'Ticker':tickers, 'Cotação':price, 'EV/EBIT':evebit, 'M.EBIT':m_ebit, 'Volume Médio':volume, 'Situação':sit}
df = pd.DataFrame(rows)
# Print first 50 data frame lines
print(df.head(50))
# Write the data to an output csv file
df.to_csv("fundamentus.csv",index=False)
shutil.move('fundamentus.csv', 'csv/fundamentus.csv')
# Write a backup csv file with today date
date = str(datetime.datetime.now().date())-datetime.timedelta(days=1)
df.to_csv('fundamentus-' + date + ".csv",index=False)
shutil.move('fundamentus-' + date + ".csv", 'csv/history/fundamentus-' + date + ".csv")
