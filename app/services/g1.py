from data_scraper import DataScraper, instantiate_driver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By

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
            description_element = article.find_element(
                By.CLASS_NAME, "feed-post-body-resumo"
            )

            article_url = article.find_element(By.TAG_NAME, "a").get_attribute("href")
            article_title = sanitize_paragraph(title_element.text)
            article_description = description_element.text

            article_dict = {
                "article_url": article_url,
                "article_title": article_title,
                "article_description": article_description,
                "image_url": "",
            }
            article_list.append(article_dict)

        for article in article_list:
            scraper.driver.get(article["article_url"])
            videos_ids = []

            try:
                image_element = scraper.driver.find_element(By.TAG_NAME, "amp-img")

                if image_element:
                    image_url = image_element.get_attribute("src")
                    article["image_url"] = image_url
            except NoSuchElementException:
                pass

            try:
                video_elements = scraper.driver.find_elements(
                    By.CLASS_NAME, "block-youtube"
                )
                for video_element in video_elements:
                    iframe = video_element.find_element(By.TAG_NAME, "iframe")
                    video_url = iframe.get_attribute("src")
                    if video_url:
                        video_id = video_url.split("/")[4].split("?")[0]
                        videos_ids.append(video_id)
                article["videos_ids"] = videos_ids
            except NoSuchElementException:
                pass

            full_article = scraper.driver.find_element(By.TAG_NAME, "article")
            full_article_text = full_article.text
            main_image_description, sanitized_article = sanitize_article(
                full_article_text
            )
            article["main_image_description"] = main_image_description

            article["full_article_text"] = sanitized_article

        scraper.quit()
        return article_list
    except Exception as e:
        print(e)
        return []


def sanitize_article(full_article_text: str) -> tuple:
    """Function to sanitize article

    Args:
        full_article_text (str): Full article text

    Returns:
        tuple: Tuple with main image description and sanitized article
    """
    split_article = full_article_text.split("\n")
    for index, paragraph in enumerate(split_article):
        split_article[index] = sanitize_paragraph(paragraph)
    main_image_description = split_article[0]
    sanitized_article = "\n".join(split_article[1:])
    return main_image_description, sanitized_article


def sanitize_paragraph(paragraph: str) -> str:
    """Function to sanitize paragraph

    Args:
        paragraph (str): Paragraph

    Returns:
        str: Sanitized paragraph
    """
    if "Leia mais" in paragraph:
        paragraph = paragraph.replace("Leia mais", "")
    if "leia mais" in paragraph:
        paragraph = paragraph.replace("leia mais", "")
    if "Leia também" in paragraph:
        paragraph = paragraph.replace("Leia também", "")
    if "leia também" in paragraph:
        paragraph = paragraph.replace("leia também", "")
    if "; veja destaques" in paragraph:
        paragraph = paragraph.replace("; veja destaques", "")
    if ". ." in paragraph:
        paragraph = paragraph.replace(". .", ".")
    if "em entrevista ao g1" in paragraph:
        paragraph = paragraph.replace("em entrevista ao g1", "")
    if ", ." in paragraph:
        paragraph = paragraph.replace(", .", ".")
    return paragraph
