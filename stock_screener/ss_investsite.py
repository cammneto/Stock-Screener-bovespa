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
    header={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0', 'Referer':url}
    page = requests.get(url,headers=header)
    # Get all the tables from the html content
    for p in page:
     try:
         tables = pd.read_html(page.content)
         return tables
     except ValueError:
         pass

# call stocks tickers from the file
stocks=ticker('tickers.dat')
miss, names, tickers, price, evebit, m_ebit, volume, sit = ([] for i in range(8))
for i in range(len(stocks)):
    print('Scraping', stocks[i],'from investsite.com.br:', i+1, 'out of', len(stocks))
    tables = page_tables(stocks[i])
    if tables==None:
        print(tables)
        print('Ativo:',stocks[i])
        print('ERR 404: STOCK NOT FOUND')
        print('\n############################################################\n')
        names.append('NOT FOUND')
        tickers.append(stocks[i])
        price.append(float('nan'))
        evebit.append(float('nan'))
        m_ebit.append(float('nan'))
        volume.append(float('nan'))
        sit.append(float('nan'))
        miss.append(stocks[i])
    else:
        # Separate tables from the page
        db = [tables[1][0],tables[1][1]]   # Dados Básicos
        pr = [tables[2][0],tables[2][1]]   # Precos Relativos
        dre= [tables[3][0],tables[3][1]]   # DRE 12 meses
        vol= [tables[5][0],tables[5][1]]   # Volume Diário (média 90 dias)
        outros=[tables[6][0],tables[6][1]] # Outros Indicadores
        namesi = db[1][0]
        names.append(namesi)
        tickers.append(stocks[i])
        pricei = float(db[1][9].replace(',','.').replace('R$ ',''))
        price.append(pricei)
        print('Empresa: ',namesi)
        print('Ativo:',stocks[i])
        print('Cotação  --->',pricei)
        try:
            evebiti = float(pr[1][9])/100
            evebit.append(evebiti)
            print('EV/EBIT  --->',pr[1][9])
        except ValueError:
            evebit.append(float('nan'))
            print('EV/EBIT --->', pr[1][9])
        try:
            mebiti=outros[1][6].replace('.','').replace(',','.').replace('%','')
            m_ebit.append(mebiti)
            print('M.EBIT   --->',mebiti)
        except AttributeError:
            mebiti=float(outros[1][6])
            m_ebit.append(mebiti)
            print('M.EBIT   --->',mebiti)
        voli = float(vol[1][12].replace('R$ ','').replace(',','').replace(' B','0000000').replace(' M','0000').replace(' mil','0'))
        volume.append(voli)
        sit.append(db[1][3])
        print('Vol Med  --->', voli)
        print('Situação --->',db[1][3])
        print('\n############################################################\n')
# build a dataframe with data from all stocks
rows = {'Empresa':names, 'Ticker':tickers, 'Cotação':price, 'EV/EBIT':evebit, 'M.EBIT':m_ebit, 'Volume Médio':volume, 'Situação':sit}
df = pd.DataFrame(rows)
# Print first 50 data frame lines
print("ERROR: page not found",miss)
print(df.head(50))
# Write the data to an output csv file
df.to_csv('investsite.csv',index=False) #writes to file
shutil.copy('investsite.csv', 'csv/investsite.csv') #make a copy in the specified location
# Write a backup csv file with date
date = str(datetime.datetime.now().date()-datetime.timedelta(days=1)) #date defined for today -1
print('data base:', date)
shutil.move('investsite.csv', 'csv/history/investsite/investsite-' + date + '.csv') #move original file to history path with date in name
