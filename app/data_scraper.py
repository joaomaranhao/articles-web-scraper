from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options


class DataScraper:
    """Class to scrape data from the web

    Attributes:
        _download_path (str): Path to download files
        options (selenium.webdriver.chrome.options.Options): Options to configure Chrome
    """
    def __init__(self, headless: bool = True) -> None:
        """Constructor

        Args:
            headless (bool, optional): Run Chrome in headless mode. Defaults to True.
        """

        self._download_path = "/tmp"

        # SELENIUM
        self.options = Options()
        self.options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": self._download_path,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True,
                "plugins.always_open_pdf_externally": True,
            },
        )
        if headless:
            self.options.add_argument("--headless")
            
        self.driver = WebDriver(
            options=self.options,
        )

    def quit(self):
        self.driver.quit()



