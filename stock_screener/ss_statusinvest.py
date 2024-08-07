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
    url = 'https://statusinvest.com.br/acoes/'+ticker
    header={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0', 'Referer':url}
    req   = requests.get(url,headers=header)
    # Strips html content
    tree   = html.fromstring(req.content)
    # company name
    name = tree.xpath('//small/text()')[2]
    if name =='RESUMO DO DIA':
        print('Empresa: NOT FOUND')
        print('Ativo:',ticker)
        miss.append(ticker)
        print('\n############################################################\n')
        name = 'NOT FOUND'
        price, evebit, m_ebit, volume, sit = 5*[float('nan')]
        return name, ticker, price, evebit, m_ebit, volume, sit
    else:
        if len(name)>20:
            print('Empresa: ',name[:20])
        else:
            print('Empresa: ',name)
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
            try:
                volume = float(price_values[6].replace('.','').replace(',','.'))
            except ValueError:
                volume = float("nan")
        else:
            try:
                volume = float(price_values[7].replace('.','').replace(',','.'))
            except ValueError:
                volume = float("nan")
        print('Vol Méd  --->', volume)
        print('Situação --->',sit)
        print('\n############################################################\n')
        return name, ticker, price, evebit, m_ebit, volume, sit

stocks = tickers('tickers.dat')
j=0
row, miss = [],[]
for i in stocks:
    j+=1
    print('Scraping', i,'from statusinvest.com.br:', j, 'out of', len(stocks))
    row.append(indicadores(i))
# Build a Dataframe with all stocks data
print("ERROR: page not found",miss)
header = ['Empresa', 'Ticker', 'Cotação', 'EV/EBIT', 'M.EBIT', 'Volume Médio', 'Situação']
df=pd.DataFrame(row,columns=header)
# Print first 50 data frame lines
print(df.head(50))
# Write the data to an output csv file
df.to_csv("statsinvst.csv",index=False)
shutil.copy('statsinvst.csv', 'csv/statsinvst.csv')
# Write a backup csv file with price date
date = str(datetime.datetime.now().date()-datetime.timedelta(days=2))
print('data base:', date)
shutil.move('statsinvst.csv', 'csv/history/statusinvest/statsinvst-' + date + ".csv")
