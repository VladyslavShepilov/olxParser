from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class OlxDownloaderMiddleware:
    def __init__(self):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("start-maximized")
        options.add_argument("--disable-gpu") 

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


    def process_request(self, request, spider):
        # Scroll and wait only 'list' pages
        if not request.url.startswith("https://www.olx.ua/uk/list/?page="):
            return None

        spider.logger.info(f"Loading content of: {request.url}")
        self.driver.get(request.url)

        self.scroll_to_bottom()

        page_source = self.driver.page_source

        return HtmlResponse(url=request.url, body=page_source, encoding="utf-8", request=request)

    def scroll_to_bottom(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit()

    def spider_opened(self, spider):
        spider.logger.info("Spider opened with Selenium Middleware")
