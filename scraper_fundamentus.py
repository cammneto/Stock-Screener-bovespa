#!/usr/bin/env python
# coding: utf-8

from scraper_tools import get_tickers_url, scrape_stock_data, save_to_csv

# Fetch all stocks pages from sitemap
tickers_urls = get_tickers_urls('https://www.fundamentus.com.br/detalhes.php?papel=')

# Scrape stocks data
all_stocks_data = scrape_stock_data(tickers_urls,"=")

# Convert to DataFrame and save to CSV
save_to_csv(all_stocks_data,'fundamentus')