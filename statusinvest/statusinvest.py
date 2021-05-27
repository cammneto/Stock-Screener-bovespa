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
    m_ebit = indicadores_financeiros[22].replace(',','.').replace('%','')
    print('M. EBIT  --->',m_ebit)
    # Format daily volume
    volume = float(price_values[7].replace('.','').replace(',','.'))
    print('Vol Med  --->', volume)
    print('Situação --->',situacao)
    print('\n############################################################\n')
    # Build a list with values to be appended
    row = [name, ticker, price, evebit, m_ebit, volume, situacao]
    return row

# Calling function to read the file
stocks = tickers('tickers.dat')#[205:]
# Header for the data frame
header = ['Empresa', 'Ticker', 'Cotação', 'EV/EBIT', 'Margem EBIT', 'Volume Diário', 'Situação']
row=[]
j=0
# Appending data in a list of lists
for i in stocks:
    j+=1
    print('Scraping', j, 'out of', len(stocks),'from: statusinvest.com.br')
    row.append(indicadores(i))
# Build a Dataframe with all stocks data
df=pd.DataFrame(row, columns=header)
# Print first 50 data frame lines
print(df.head(50))
# Save data to a csv file
df.to_csv("statusinvest.csv",index=False)
# Sava a backup with current data
today = str(datetime.datetime.now().date())
df.to_csv('statusinvest-' + today + ".csv",index=False)
shutil.move('statusinvest-' + today + ".csv", '../history/statusinvest-' + today + ".csv")
