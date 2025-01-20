from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time


class OlxDownloaderMiddleware:
    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("start-maximized")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def process_request(self, request, spider):
        spider.logger.info(f"Loading content of the: {request.url}")
        self.driver.get(request.url)

        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        page_source = self.driver.page_source
        return HtmlResponse(url=request.url, body=page_source, encoding="utf-8", request=request)

    def __del__(self):
        self.driver.quit()

    def spider_opened(self, spider):
        spider.logger.info("Spider opened with Selenium Middleware")
