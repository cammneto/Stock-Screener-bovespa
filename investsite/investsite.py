import pandas as pd
import requests
import datetime
import shutil

# Read Stocks file for searching
def ticker(InputFile):
    infile = open(InputFile, "r")
    tickers = [line.split() for line in infile]
    ticker = []
    for i in tickers:
        ticker.append(i[0])
    return ticker

# Scrap data from url
def page_tables(ticker):
    url = 'https://www.investsite.com.br/principais_indicadores.php?cod_negociacao='+ticker
    page = requests.get(url)
    # Get all the tables from the html content
    for p in page:
     try:
         tables = pd.read_html(page.content)
         return tables
     except ValueError:
         pass

# call stocks tickers from the file
stocks=ticker('tickers.dat')
names,tickers,price,evebit,m_ebit,volume,sit=[],[],[],[],[],[],[]
for i in range(len(stocks)):
    print('Scraping',i+1, 'out of', len(stocks),'from: investsite.com.br')
    tables = page_tables(stocks[i])
    if tables==None:
        print(tables)
        print('Ativo:',stocks[i])
        print('ERR 404: STOCK NOT FOUND')
        print('\n############################################################\n')
        pass
    else:
        # Separate tables from the page
        db = [tables[1][0],tables[1][1]]   # Dados Básicos
        pr = [tables[2][0],tables[2][1]]   # Precos Relativos
        dre= [tables[3][0],tables[3][1]]   # DRE 12 meses
        vol= [tables[5][0],tables[5][1]]   # Volume Diário (média 90 dias)
        outros=[tables[6][0],tables[6][1]] # Outros Indicadores
        namesi = db[1][0]
        names.append(namesi)
        print('Empresa: ',namesi)
        tickers.append(stocks[i])
        print('Ativo:',stocks[i])
        pricei = float(db[1][9].replace(',','.').replace('R$ ',''))
        price.append(pricei)
        print('Cotação  --->',pricei)
        try:
            evebiti = float(pr[1][9])/100
            evebit.append(evebiti)
            print('EV/EBIT  --->',evebiti)
        except ValueError:
            evebit.append(float('nan'))
            print('EV/EBIT --->', pr[1][9])
        print('M.EBIT --->',outros[1][6])
        m_ebit.append(outros[1][6])
        voli = float(vol[1][12].replace('R$ ','').replace(',','').replace(' B','0000000').replace(' M','0000').replace(' mil','0'))
        volume.append(voli)
        print('Vol Med  --->', voli)
        sit.append(db[1][3])
        print('Situação --->',db[1][3])
        print('\n############################################################\n')
# build a dataframe with data from all stocks
rows = {'Empresa':names, 'Ticker':tickers, 'Cotação':price, 'EV/EBIT':evebit, 'M.EBIT':m_ebit, 'Volume Médio':volume, 'Situação Judicial':sit}
df = pd.DataFrame(rows)
# Print first 50 data frame lines
print(df.head(50))
# Write the data to an output csv file
df.to_csv("investsite.csv",index=False)
# Write a backup csv file with today date
today = str(datetime.datetime.now().date())
df.to_csv('investsite-' + today + ".csv",index=False)
shutil.move('investsite-' + today + ".csv", '../history/investsite-' + today + ".csv")
