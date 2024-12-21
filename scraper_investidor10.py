#!/usr/bin/env python
# coding: utf-8

from scraper_tools import parse_sitemap, scrape_stock_data, save_to_csv

sitemap_url = 'https://statusinvest.com.br/sitemaps/sitemap-acao.xml'
base_url = "https://statusinvest.com.br/acoes/"
url_to_scrape = 'https://investidor10.com.br/acoes/'

# Fetch all stocks pages from sitemap
tickers = [url for url in parse_sitemap(sitemap_url, base_url) if "page" not in url]
tickers_urls = [url_to_scrape+ticker.split('acoes/')[-1] for ticker in tickers_urls]

# Scrape stocks data
all_stocks_data = scrape_stock_data(tickers_urls,"/")

# Convert to DataFrame and save to CSV
save_to_csv(all_stocks_data, 'investidor10')