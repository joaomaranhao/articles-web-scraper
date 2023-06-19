from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class DataScraper:
    """Class to scrape data from the web

    Attributes:
        _download_path (str): Path to download files
        options (selenium.webdriver.chrome.options.Options): Options to configure Chrome
        driver (selenium.webdriver.chrome.webdriver.WebDriver): Chrome webdriver
    """

    def __init__(self, webdriver_manager: bool = False, headless: bool = True) -> None:
        """Constructor

        Args:
            webdriver_manager (bool, optional): Use webdriver_manager to download ChromeDriver. Defaults to False.
            headless (bool, optional): Run Chrome in headless mode. Defaults to True.
        """

        self._download_path = "/tmp"

        # SELENIUM
        self.options = Options()
        self.options.binary_location = "/opt/chrome/chrome"
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
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--disable-dev-tools")
        self.options.add_argument("--no-zygote")
        self.options.add_argument("--single-process")
        self.options.add_argument("window-size=2560x1440")
        self.options.add_argument("--user-data-dir=/tmp/chrome-user-data")
        self.options.add_argument("--remote-debugging-port=9222")
        self.options.add_argument("--headless")

        if webdriver_manager:
            self.driver = webdriver.Chrome(
                service=Service(
                    executable_path=ChromeDriverManager().install(),
                    log_path="/tmp/chromedriver.log",
                ),
            )

        else:
            self.driver = webdriver.Chrome(
                service=Service(
                    executable_path="/opt/chromedriver/chromedriver",
                    log_path="/tmp/chromedriver.log",
                ),
                options=self.options,
            )

    def quit(self):
        self.driver.quit()


def instantiate_driver() -> DataScraper:
    """Function to instantiate driver

    Returns:
        DataScraper: DataScraper object
    """
    scraper = DataScraper(webdriver_manager=True, headless=False)
    return scraper
