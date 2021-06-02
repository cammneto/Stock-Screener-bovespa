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

# Build the row with values for each stock
def indicadores(ticker):
    # Define url to read
    url   = requests.get('https://statusinvest.com.br/acoes/'+ticker)
    # Strips html content
    tree   = html.fromstring(url.content)
    # company name
    name = tree.xpath('//small/text()')[0]
    print('Empresa: ',name)
    print('Ativo:',ticker)
    # Stock price
    price_values = tree.xpath('//strong[@class="value"]/text()')
    # html line with values for selected stock
    indicadores_financeiros = tree.xpath('//strong[@class="value d-block lh-4 fs-4 fw-700"]/text()')
    # Financial situation
    situacao = tree.xpath('//strong[@class="main-badge mt-1 fs-2 p-1 red accent-4"]/text()')
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
    if ticker=='ALUP11' or ticker=='SAPR11' or ticker=='TAEE11':
        volume = float(price_values[6].replace('.','').replace(',','.'))
    else:
        volume = float(price_values[7].replace('.','').replace(',','.'))
    print('Vol Méd  --->', volume)
    print('Situação --->',situacao)
    print('\n############################################################\n')
    return name, ticker, price, evebit, m_ebit, volume, situacao

stocks = tickers('tickers.dat')
j=0
names,tickers,price,evebit,m_ebit,volume,sit=[],[],[],[],[],[],[]
for i in stocks:
    j+=1
    print('Scraping', j, 'out of', len(stocks),'from: statusinvest.com.br')
    row = indicadores(i)
    names.append(row[0])
    tickers.append(row[1])
    price.append(row[2])
    evebit.append(row[3])
    m_ebit.append(row[4])
    volume.append(row[5])
    sit.append(row[6])
# Build a Dataframe with all stocks data
rows = {'Empresa':names, 'Ticker':tickers, 'Cotação':price, 'EV/EBIT':evebit, 'M.EBIT':m_ebit, 'Volume Médio':volume, 'Situação':sit}
df=pd.DataFrame(rows)#, columns=header)
# Print first 50 data frame lines
print(df.head(50))
# Write the data to an output csv file
df.to_csv("statusinvest.csv",index=False)
shutil.move('statusinvest.csv', 'csv/statusinvest.csv')
# Write a backup csv file with today date
date = str(datetime.datetime.now().date())-datetime.timedelta(days=1)
print('data base date:', date)
df.to_csv('statusinvest-' + date + ".csv",index=False)
shutil.move('statusinvest-' + date + ".csv", 'csv/history/statusinvest-' + date + ".csv")
