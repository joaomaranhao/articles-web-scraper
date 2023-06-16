from data_scraper import DataScraper
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException

DEFAULT_URL = "https://g1.globo.com/pop-arte/games/"

def get_g1_articles(url: str = DEFAULT_URL) -> list:
    """Function to get articles from G1

    Args:
        url (str, optional): URL to scrape. Defaults to DEFAULT_URL.

    Returns:
        list: List of articles
    """
    try:
        scraper = DataScraper(webdriver_manager=True, headless=False)
        try:
            scraper.driver.get(url)
        except WebDriverException:
            scraper.quit()
            print("Error getting URL. Check if the URL is correct.")
            return []
        article_list = []
        articles = scraper.driver.find_elements(By.CLASS_NAME, "feed-post-body")
        for article in articles:
            title_element = article.find_element(By.CLASS_NAME, "gui-color-hover")
            description_element = article.find_element(By.CLASS_NAME, "feed-post-body-resumo")

            article_url = article.find_element(By.TAG_NAME, "a").get_attribute("href")
            article_title = title_element.text
            article_description = description_element.text

            article_dict = {
                "article_url": article_url,
                "article_title": article_title,
                "article_description": article_description,
            }
            article_list.append(article_dict)

        for article in article_list:
            scraper.driver.get(article["article_url"])
            video_urls = []

            try:
                image_element = scraper.driver.find_element(By.TAG_NAME, "amp-img")

                if image_element:
                    image_url = image_element.get_attribute("src")
                    article["image_url"] = image_url
            except NoSuchElementException:
                pass

            try:
                video_elements = scraper.driver.find_elements(By.CLASS_NAME, "block-youtube")
                for video_element in video_elements:
                    iframe = video_element.find_element(By.TAG_NAME, "iframe")
                    video_url = iframe.get_attribute("src")
                    video_urls.append(video_url)
                article["video_urls"] = video_urls
            except NoSuchElementException:
                pass

            full_article = scraper.driver.find_element(By.TAG_NAME, "article")
            full_article_text = full_article.text

            article["full_article_text"] = full_article_text
        
        scraper.quit()
        return article_list
    except Exception as e:
        print(e)
        scraper.quit()
        return []