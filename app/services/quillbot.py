import time
from data_scraper import DataScraper
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException

DEFAULT_URL = "https://quillbot.com/"

def rewrite_paragraph(paragraph: str) -> str:
    """Function to rewrite paragraphs using Quillbot

    Args:
        paragraphs (list): List of paragraphs to be rewritten

    Returns:
        list: List of rewritten paragraphs
    """
    scraper = DataScraper(webdriver_manager=True, headless=False)
    try:
        scraper.driver.get(DEFAULT_URL)
    except WebDriverException:
        scraper.quit()
        print("Error getting URL. Check if the URL is correct.")
        return []
    try:
        rewrited_paragraphs = []
        #Select language
        language_value = "Portuguese"
        language_dropdown = scraper.driver.find_element(By.CLASS_NAME, "css-rplln7")
        language_dropdown.click()
        time.sleep(.5)
        language_button = language_dropdown.find_element(By.XPATH, f"//*[text()='{language_value}']")
        time.sleep(.5)
        language_button.click()
        time.sleep(.5)

        #Paste paragraph
        text_area = scraper.driver.find_element(By.ID, "paraphraser-input-box")
        time.sleep(.5)
        text_area.clear()
        time.sleep(.5)
        text_area.send_keys(paragraph)
        time.sleep(.5)

        #Click rewrite button
        button_aria_label = "Paraphrase (Ctrl + Enter)"
        rewrite_button = scraper.driver.find_element(By.XPATH, f"//*[@aria-label='{button_aria_label}']")
        time.sleep(.5)
        rewrite_button.click()
        time.sleep(4)

        #Get result
        reslut_area = scraper.driver.find_element(By.ID, "paraphraser-output-box")
        rewrited_element = reslut_area.find_element(By.TAG_NAME, "span")
        rewrited_paragraph = rewrited_element.text
        return rewrited_paragraph

    except NoSuchElementException:
        pass
    finally:
        scraper.quit()
    return ""
