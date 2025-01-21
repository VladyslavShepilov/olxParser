from config.logging import setup_logging
from config.database import create_tables
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from olx.spiders.olx_spider import OlxSpider

def main():
    setup_logging()
    create_tables()

    process = CrawlerProcess(get_project_settings())
    process.crawl(OlxSpider)

    process.start()

if __name__ == "__main__":
    main()
