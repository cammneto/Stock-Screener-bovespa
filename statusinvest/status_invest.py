import pandas as pd
from lxml import html
import requests as req
import datetime

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
    url   = req.get('https://statusinvest.com.br/acoes/'+ticker)
    # Strips html content
    tree   = html.fromstring(url.content)
    # Get the company name
    name = tree.xpath('//small/text()')[0]
    # Stock price
    price_values = tree.xpath('//strong[@class="value"]/text()')
    # html line with values for selected stock
    indicadores_financeiros = tree.xpath('//strong[@class="value d-block lh-4 fs-4 fw-700"]/text()')
    # Financial situation
    situacao = tree.xpath('//strong[@class="main-badge mt-1 fs-2 p-1 red accent-4"]/text()')
    # Format prices to float
    price = float(price_values[0].replace(',','.'))
    # Format EV/EBIT
    value_ebit  = indicadores_financeiros[5].replace(',','.')
    # Format EBIT Margin
    margem_ebit = indicadores_financeiros[22].replace(',','.').replace('%','')
    # Format daily volume
    volume = float(price_values[7].replace('.','').replace(',','.'))
    # Build the row with values to be appended
    row = [name, ticker, price, value_ebit, margem_ebit, volume, situacao]
    return row

# Calling function to read the file
stocks = tickers('tickers.dat')#[:10]
# Header for the data frame
header = ['Empresa', 'Ticker', 'Cotação', 'EV/EBIT', 'Margem EBIT', 'Volume Diário', 'Situação']
row=[]
j=0
# Appends the rows after call the function to build it
for i in stocks:
    j+=1
    print('Procurando Ativo', j, i, 'no site statusinvest.com.br')
    print('Total de ações', len(stocks))
    row.append(indicadores(i))
    print('DONE', i)
    print('#####################################################################')
# Dataframe with data for all stocks
df=pd.DataFrame(row, columns=header)
print(df)
# Save data to a csv file
df.to_csv("output.csv",index=False)
# Sava a backup with current data
today = str(datetime.datetime.now().date())
df.to_csv('output-' + today + ".csv",index=False)
