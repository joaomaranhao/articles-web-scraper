from data_scraper import DataScraper

if __name__ == "__main__":
    scraper = DataScraper(webdriver_manager=True, headless=False)
    print(scraper._download_path)
    scraper.quit()