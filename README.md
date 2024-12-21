# Brazilian Stock Market Data Scraper

This repository contains Python scripts designed to scrape and aggregate financial data for all stocks listed on the Brazilian stock exchange (B3) from four reliable platforms: **Status Invest**, **InvestSite**, **Investidor10**, and **Fundamentus**. These scripts use web scraping techniques to collect key stock indicators and export them to structured CSV files for analysis.

## Features
- **Multi-Source Data Aggregation**: Consolidates financial and operational metrics from multiple trusted sources.
- **Automated Sitemap Parsing**: Dynamically identifies stock-specific pages from each platform’s sitemap.
- **Customizable and Scalable**: Easily extendable to include additional platforms or tailor data points to your needs.
- **CSV Export**: Outputs data in clean, date-stamped CSV files for easy integration with analytics tools.

## Repository Structure
### Shared Utilities
- **`scraper_tools.py`**
  - Provides core functions for:
    - Fetching HTML content using `requests`.
    - Parsing stock data using `BeautifulSoup`.
    - Saving results to CSV files with accurate date-stamping.
  - Handles platform-specific scraping logic using modular parsing functions.

### Platform-Specific Scrapers
1. **`scraper_statusinvst.py`**
   - Scrapes data from [Status Invest](https://statusinvest.com.br).
   - Parses the sitemap to identify stock pages and extracts detailed financial data.

2. **`scraper_investsite.py`**
   - Scrapes key metrics from [InvestSite](https://www.investsite.com.br).
   - Uses the sitemap to dynamically discover stock-specific pages.

3. **`scraper_investidor10.py`**
   - Collects data from [Investidor10](https://investidor10.com.br).
   - Maps stock tickers from Status Invest to their respective pages on Investidor10.

4. **`scraper_fundamentus.py`**
   - Scrapes key metrics from [Fundamentus](https://fundamentus.com.br)
   - Uses the sitemap to dynamically discover stock-specific pages.

## How to Use
1. Clone the repository.
2. Install required libraries (requests, BeautifulSoup, pandas).
3. Run the individual scripts to fetch data from the respective platforms.
4. Find the generated CSV files with aggregated stock information in the current working directory.

Note: This project adheres to the respective websites' terms of service and is intended for educational purposes. Always ensure compliance with local laws and ethical web scraping practices.
