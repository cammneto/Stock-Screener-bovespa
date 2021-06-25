from lxml import html
import pandas as pd
import requests
import datetime
import shutil
import numpy as np

# Read file with stocks tickers
def tickers(InputFile):
    infile = open(InputFile, "r")
    tickers = [line.split() for line in infile]
    ticker = []
    for i in tickers:
        ticker.append(i[0])
    return ticker

# Build the row with values for each stock
def indicadores(ticker):
    # Define url to read
    url   = requests.get('https://statusinvest.com.br/acoes/'+ticker)
    # Strips html content
    tree   = html.fromstring(url.content)
    # company name
    name = tree.xpath('//small/text()')[0]
    if name =='RESUMO DO DIA':
        print('Empresa: NOT FOUND')
        print('Ativo:',ticker)
        miss.append(ticker)
        print('\n############################################################\n')
        name = 'NOT FOUND'
        price, evebit, m_ebit, volume, sit = 5*[float('nan')]
        return name, ticker, price, evebit, m_ebit, volume, sit
    else:
        print('Empresa: ',name)
        print('Ativo:',ticker)
        # Stock price
        price_values = tree.xpath('//strong[@class="value"]/text()')
        # html line with values for selected stock
        indicadores_financeiros = tree.xpath('//strong[@class="value d-block lh-4 fs-4 fw-700"]/text()')
        # Financial situation
        sit = tree.xpath('//strong[@class="main-badge mt-1 fs-2 p-1 red accent-4"]/text()')
        # Format prices to float
        price = float(price_values[0].replace(',','.'))
        print('Cotação  --->',price)
        # Format EV/EBIT
        evebit  = indicadores_financeiros[5].replace(',','.')
        print('EV/EBIT  --->',evebit)
        # Format EBIT Margin
        m_ebit = indicadores_financeiros[22].replace('.','').replace(',','.').replace('%','')
        print('M. EBIT  --->',m_ebit)
        # Format daily volume
        if len(ticker)==6:
            volume = float(price_values[6].replace('.','').replace(',','.'))
        else:
            volume = float(price_values[7].replace('.','').replace(',','.'))
        print('Vol Méd  --->', volume)
        print('Situação --->',sit)
        print('\n############################################################\n')
        return name, ticker, price, evebit, m_ebit, volume, sit

stocks = tickers('tickers.dat')
j=0
miss,row,names,tickers,price,evebit,m_ebit,volume,sit=([] for i in range(9))
for i in stocks:
    j+=1
    print('Scraping', j, 'out of', len(stocks),'from: statusinvest.com.br')
    row.append(indicadores(i))
# Build a Dataframe with all stocks data
header = ['Empresa', 'Ticker', 'Cotação', 'EV/EBIT', 'M.EBIT','Volume Médio', 'Situação']
df=pd.DataFrame(row,columns=header)
# Print first 50 data frame lines
print(df.head(50))
# Write the data to an output csv file
df.to_csv("statsinvst.csv",index=False)
shutil.move('statsinvst.csv', 'csv/statsinvst.csv')
# Write a backup csv file with price date
date = str(datetime.datetime.now().date()-datetime.timedelta(days=1))
print('data base:', date)
df.to_csv('statsinvst-' + date + ".csv",index=False)
shutil.move('statsinvst-' + date + ".csv", 'csv/history/statsinvst-' + date + ".csv")
