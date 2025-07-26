import requests
from bs4 import BeautifulSoup
import pandas as pd
from statistics import mode
from datetime import datetime,date, timedelta

def fetch_html(url):
    """Fetch the HTML content of a given URL."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0', 'Referer': url}
    return requests.get(url, headers=headers).text

def parse_sitemap(sitemap_url, base_url):
    """Parse the sitemap and return a list of stock URLs."""
    sitemap_content = BeautifulSoup(fetch_html(sitemap_url), "xml").text.split("\n")
    pages_toscrape = sorted([line for line in sitemap_content if base_url in line and len(base_url) < len(line) < len(base_url)+9])
    print(f"Number of urls to scrape: {len(pages_toscrape)}\n")
    return pages_toscrape

def get_tickers_urls(base_url):
    tickers_url = []
    for row in BeautifulSoup(fetch_html(base_url), 'html.parser').find_all('td'):
        for item in row.find_all('a'):
            tickers_url.append(base_url+item.get_text())
    return tickers_url

def parse_stock_data(soup,site):
    """Parse stock data from the BeautifulSoup object and return a dictionary."""
    stock_data = {}

    if 'investsite' in site:
        for title,value in zip(soup.find_all('td',class_='esquerda'),soup.find_all('td',class_='direita')):
            stock_data[title.get_text().strip()] = value.get_text().strip()
    elif 'fundamentus' in site:
        for label,data in zip(soup.find_all('td', class_='label'),soup.find_all('td', class_='data')):
            title = label.find('span', class_='txt')
            value = data.find('span', class_=['txt','oscil'])
            if title and value:
                stock_data[title.get_text().strip()] = value.get_text().strip()
    elif 'status' in site:
        for info,indicator in zip(soup.find_all('div', class_='info'),soup.find_all('div', class_='item')):
            title = info.find(['h3', 'span'], class_=['title', 'd-none', 'd-inline-block', 'sub-value']) or indicator.find('h3', class_='title')
            value = info.find('strong', class_='value') or indicator.find('strong', class_='value')
            if title and value and "\n" not in title.get_text() and value.get_text() != "\xa0":
                stock_data[title.get_text().strip()] = value.get_text().strip()
    elif 'investidor10' in site:
        for title,value in zip(soup.find_all('div',class_='_card-header'),soup.find_all('div',class_='_card-body')):
            stock_data[title.get_text().strip()] = value.get_text().strip()
        for cell in soup.find_all('div',class_='cell'):
            title = cell.find(['span'], class_=['d-flex', 'title'])
            value = cell.find(['div', 'span'], class_='value')
            if title and value:
                if 'DIVIDEND YIELD - ' in title.get_text().strip():
                    stock_data[title.get_text().strip().split('-')[0]] = value.get_text().strip().split('\n')[-1]
                else:
                    stock_data[title.get_text().strip()] = value.get_text().strip().split('\n')[-1]
        # Extract the price date
        for item in soup.find_all('div', class_='_card cotacao'):
            stock_data['Data da Cotação'] = item.find('i', class_='far')['data-content'].split()[-1]
    else:
        raise Exception('Site unknown!!!')
        
    return stock_data

def scrape_stock_data(tickers_urls,split_parameter):
    """Scrape stock data from a list of URLs."""
    all_stocks_data = []
    
    for n, url in enumerate(tickers_urls):  # Limit to n stocks for testing: tickers_urls[:n]
        print(f"Scraping {url.split(split_parameter)[-1]} data ({n+1} of {len(tickers_urls)})\n page: {url}")
        soup = BeautifulSoup(fetch_html(url), 'html.parser')
        stock_data = {"Ticker": url.split(split_parameter)[-1]}  # Add ticker symbol to the stock data
        stock_data.update(parse_stock_data(soup,url))  # Merge parsed data
        all_stocks_data.append(stock_data)  # Append to the list

    return all_stocks_data

def save_to_csv(data_list, database_name):
    """
    Save scraped data to a CSV file with price date in the filename.
    """
    df = pd.DataFrame(data_list)
    if 'Data da Cotação' in df.columns: 
        price_date = mode(df['Data da Cotação']) # get the most common date as the most recent price date
        YMD_date = datetime.strptime(price_date,'%d/%m/%Y').strftime('%Y-%m-%d') # format date to be Y-m-d
        file_name = YMD_date+'_'+database_name+'.csv'
    elif 'Data últ cot' in df.columns:
        price_date = mode(df['Data últ cot']) # get the most recent date as the most common date
        YMD_date = datetime.strptime(price_date,'%d/%m/%Y').strftime('%Y-%m-%d') # format date to be Y-m-d
        file_name = YMD_date+'_'+database_name+'.csv'
    else:
        weekday = date.today().weekday()
        print(f'weekday {weekday+1}')
        if weekday == 5:
            print("today is saturday")
            today = str(date.today() - timedelta(days=1))
        elif weekday == 6:
            print("today is sunday")
            today = str(date.today() - timedelta(days=2))
        else:
            today = str(date.today())
        print('database date {today}')
        file_name = today+'_'+database_name+'.csv' # Writes today date in filename in case price date is not present in the dataframe
    df.to_csv(file_name, index=False)
    print(f"\nData saved to ---> {file_name}\n")