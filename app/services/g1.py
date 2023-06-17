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
            videos_ids = []

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
                    video_id = video_url.split("/")[4].split("?")[0]
                    videos_ids.append(video_id)
                article["videos_ids"] = videos_ids
            except NoSuchElementException:
                pass

            full_article = scraper.driver.find_element(By.TAG_NAME, "article")
            full_article_text = full_article.text
            main_image_description, sanitized_article = sanitize_article(full_article_text)
            article["main_image_description"] = main_image_description

            article["full_article_text"] = sanitized_article
        
        scraper.quit()
        return article_list
    except Exception as e:
        print(e)
        scraper.quit()
        return []
    
def sanitize_article(full_article_text: str) -> tuple:
    """Function to sanitize article

    Args:
        full_article_text (str): Full article text

    Returns:
        tuple: Tuple with main image description and sanitized article
    """
    split_article = full_article_text.split("\n")
    main_image_description = split_article[0]
    sanitized_article = "\n".join(split_article[1:])
    return main_image_description, sanitized_article

def create_markdown(article_dict: dict) -> str:
    """Function to create markdown from article dict

    Args:
        article_dict (dict): Article

    Returns:
        str: Markdown
    """
    videos_used_counter = 0
    paragraph_list = article_dict["full_article_text"].split("\n")
    markdown = f"# {article_dict['article_title']}\n\n"
    markdown += f"## {article_dict['article_description']}\n\n"
    markdown += f"![{article_dict['main_image_description']}]({article_dict['image_url']})\n\n"
    for paragraph in paragraph_list:
        if article_dict["videos_ids"]:
            if paragraph.startswith("'") and paragraph.endswith("'"):
                markdown += f"### {paragraph[1:-1]}\n\n"
                markdown += f"[![](https://img.youtube.com/vi/{article_dict['videos_ids'][videos_used_counter]}/0.jpg)](https://www.youtube.com/watch?v={article_dict['videos_ids'][videos_used_counter]})\n\n"
                videos_used_counter += 1
            else:
                markdown += f"{paragraph}\n\n"
        else:
            markdown += f"{paragraph}\n\n"
    return markdown

