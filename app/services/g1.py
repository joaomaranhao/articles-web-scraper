import os
from data_scraper import DataScraper
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from services.quillbot import rewrite_paragraph

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
            article_title = sanitize_paragraph(title_element.text)
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

def create_article_html(article_dict: dict) -> str:
    """Function to create HTML from article dict

    Args:
        article_dict (dict): Article

    Returns:
        str: HTML
    """
    videos_used_counter = 0
    paragraph_list = article_dict["full_article_text"].split("\n")
    title = rewrite_paragraph(article_dict['article_title'])
    html = f"<h1>{title}</h1>\n\n"
    description = rewrite_paragraph(article_dict['article_description'])
    html += f"<h3>{description}</h3>\n\n"
    html += f'<img src="{article_dict["image_url"]}" alt="{article_dict["main_image_description"]}">\n\n'
    for paragraph in paragraph_list:
        if article_dict["videos_ids"]:
            if paragraph.startswith("'") and paragraph.endswith("'"):
                html += f"<h2>{paragraph[1:-1]}</h2>\n\n"
                html += f'<iframe class="centered-iframe" width="560" height="315" src="https://www.youtube.com/embed/{article_dict["videos_ids"][videos_used_counter]}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>\n\n'
                videos_used_counter += 1
            else:
                paragraph = rewrite_paragraph(paragraph)
                html += f"<p>{paragraph}</p>\n\n"
        else:
            paragraph = rewrite_paragraph(paragraph)
            html += f"<p>{paragraph}</p>\n\n"
    return html

def save_html_to_file(html_text: str) -> str:    
    """Function to save HTML to file and return file name

    Args:
        html_text (str): HTML text
    """
    file_name = html_text.split("\n")[0].split("<h1>")[1].replace(" ", "_").replace(",", "").replace(":", "").replace("'", "").lower().split("</h1>")[0]
    with open(f"./tmp/{file_name}.html", "w") as file:
        file.write(html_text)
    return file_name

def delete_html_file(file_name: str) -> None:
    """Function to delete HTML file

    Args:
        file_name (str): File name
    """
    os.remove(f"./tmp/{file_name}.html")