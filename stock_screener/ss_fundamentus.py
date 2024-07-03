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

stocks = tickers('tickers.dat')
miss, names, tickers, price, evebit, m_ebit, volume = ([] for i in range(7))
for i in range(len(stocks)):
    print('Scraping', stocks[i],'from fundamentus.com.br:', i+1, 'out of', len(stocks))
    tables = page_tables(stocks[i])
    if tables==None:
        print('ERR 404: STOCK NOT FOUND')
        print('\n############################################################\n')
        names.append('NOT FOUND')
        tickers.append(stocks[i])
        price.append(float('nan'))
        evebit.append(float('nan'))
        m_ebit.append(float('nan'))
        volume.append(float('nan'))
        miss.append(stocks[i])
    else:
        try:
            names.append(tables[0][1][2].replace(' ON','').replace(' PNA','').replace(' PNB','').replace(' PN','').replace(' N1','').replace(' UNT','').replace(' N2','').replace(' NM',''))
            print('Empresa:',tables[0][1][2].replace(' ON','').replace(' PNA','').replace(' PNB','').replace(' PN','').replace(' N1','').replace(' UNT','').replace(' N2','').replace(' NM',''))
            tickers.append(stocks[i])
            price.append(float(tables[0][3][0])/100)
            print('Cotação --->',float(tables[0][3][0])/100)
            try:
                evebit.append(float(tables[2][3][10].replace('.',''))/100)
            except ValueError:
                evebit.append(float('nan'))
            print('EV/EBIT  --->',tables[2][3][10])
            try:
                m_ebit.append(float(tables[2][5][4].replace(',','.').replace('%','')))
            except ValueError:
                m_ebit.append(float('nan'))
            print('M. EBIT  --->',tables[2][5][4].replace(',','.').replace('%',''))
            volume.append(float(tables[0][3][4].replace('.','')))
            print('Vol Méd  --->', float(tables[0][3][4].replace('.','')))
            print('\n############################################################\n')
        except:
            print('ERR 404: STOCK NOT FOUND')
            print('\n############################################################\n')
            names.append('NOT FOUND')
            tickers.append(stocks[i])
            price.append(float('nan'))
            evebit.append(float('nan'))
            m_ebit.append(float('nan'))
            volume.append(float('nan'))
            miss.append(stocks[i])
# build a dataframe with data from all stocks
print("ERROR: page not found",miss)
rows = {'Empresa':names, 'Ticker':tickers, 'Cotação':price, 'EV/EBIT':evebit, 'M.EBIT':m_ebit, 'Volume Médio':volume}
df = pd.DataFrame(rows)
# Print first 50 data frame lines
print(df.head(50))
# Write the data to an output csv file
df.to_csv("fundaments.csv",index=False)
shutil.copy('fundaments.csv', 'csv/fundaments.csv')
# Write a backup csv file with price date
date = str(datetime.datetime.now().date()-datetime.timedelta(days=2))
print('data base:', date)
shutil.move('fundaments.csv', 'csv/history/fundamentus/fundaments-' + date + ".csv")
