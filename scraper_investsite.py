#!/usr/bin/env python
# coding: utf-8

from scraper_tools import parse_sitemap, scrape_stock_data, save_to_csv

sitemap_url = "https://www.investsite.com.br/sitemap.xml"
base_url = "https://www.investsite.com.br/principais_indicadores.php?cod_negociacao="

# Fetch all stocks pages from sitemap
tickers_urls = parse_sitemap(sitemap_url, base_url)

# Scrape stocks data
all_stocks_data = scrape_stock_data(tickers_urls,"=")

# Convert to DataFrame and save to CSV
save_to_csv(all_stocks_data,'investsite')