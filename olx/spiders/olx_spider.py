import scrapy
from scrapy.exceptions import CloseSpider

from olx.selectors import OLXSelectors


class OlxSpider(scrapy.Spider):
    name = "olx_spider"

    base_url = "https://www.olx.ua/uk/list/?page="
    page_limit = 5

    def start_requests(self):
        for page in range(1, self.page_limit + 1):
            url = self.base_url + str(page)
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for card in response.css(OLXSelectors.CARD):
            book_link = card.css(OLXSelectors.LINK).get()

            if book_link:
                yield response.follow(book_link, callback=self.parse_item)

    def parse_item(self, response):
        page_name = response.url
        self.logger.info(f"Processing page: {page_name}")

        item = {
            "olx_id": response.xpath(OLXSelectors.ID_X).get(),
            "views": response.xpath(OLXSelectors.VIEWS_X).get(),
            "title": response.css(OLXSelectors.TITLE).get(),
            "price": response.css(OLXSelectors.PRICE).get(),
            "published_at": response.css(OLXSelectors.PUBLISHED_AT).get(),
            "description": response.css(OLXSelectors.DESCRIPTION).get(),
            "images": response.css(OLXSelectors.IMG_SRC).getall(),
            "tags": response.css(OLXSelectors.TAGS).getall(),
        }
        self.logger.info(f"Item is {item}")

        yield item
