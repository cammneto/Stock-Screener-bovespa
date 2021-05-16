import pandas as pd
import requests
import datetime

# Import stocks for searching
def ticker(InputFile):
    infile = open(InputFile, "r")
    tickers = [line.split() for line in infile]
    ticker = []
    for i in tickers:
        ticker.append(i[0])
    return ticker

# Scrap data from url
def frame(i,ticker):
    print('Scraping data for', ticker, 'from investsite.com.br','\n')
    url = 'https://www.investsite.com.br/principais_indicadores.php?cod_negociacao='+ticker
    html = requests.get(url).content
    # Get all the tables from the html content
    tables = pd.read_html(html)
    # Separate tables from html
    db = [tables[1][0],tables[1][1]]   # Dados Básicos
    pr = [tables[2][0],tables[2][1]]   # Precos Relativos
    dre= [tables[3][0],tables[3][1]]   # DRE 12 meses
    vol= [tables[5][0],tables[5][1]]   # Volume Diário (média 90 dias)
    outros=[tables[6][0],tables[6][1]] # Outros Indicadores
    # Arrange desired values in a list
    linha=[db[1][0],db[1][6],db[1][9],pr[1][9],outros[1][6],vol[1][12],db[1][3]]
    print(ticker,'DONE')
    print('##########################################################')
    return linha

# call stocks tickers from the file
tickers=ticker('tickers.dat')
rows=[]
number = len(tickers)

for i in range(number):
    print('Searching for stock', i, 'out of', number, 'Stocks','\n')
    ticker=tickers[i]
    rows.append(frame(i,ticker))

# Create a header for the data frame
header = ['Empresa', 'Ticker', 'Cotação', 'EV/EBIT', 'Margem EBIT', 'Volume Diário', 'Situação']
# build a dataframe with data from all stocks
df=pd.DataFrame(rows, columns=header)
# Print first 60 data frame lines
print(df.head(60))
# Write the data to an output csv file
df.to_csv("output.csv",index=False)
# Write a backup csv file with today date
today = str(datetime.datetime.now().date())
df.to_csv('output-' + today + ".csv",index=False)
