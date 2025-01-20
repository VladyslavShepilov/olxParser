import scrapy
from olx.selectors import OLXSelectors
from olx.items import OlxItem

class OlxSpider(scrapy.Spider):
    name = "olx_spider"

    base_url = "https://www.olx.ua/uk/list/?page=" 
    page_limit = 1

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
        page_name = response.url.split("/")[-1]
        print(f"Current page: {page_name}")
        
        item = {
            "id": response.css(OLXSelectors.ID).get(),
            "views": response.css(OLXSelectors.VIEWS).get(),
            "title": response.css(OLXSelectors.TITLE).get(),
            "price": response.css(OLXSelectors.PRICE).get(),
            "published_at": response.css(OLXSelectors.PUBLISHED_AT).get(),
            "description": response.css(OLXSelectors.DESCRIPTION).get(),
            "images": response.css(OLXSelectors.IMG_SRC).getall(),
            "tags": response.css(OLXSelectors.TAGS).getall(),
        }

        try:
            listing_item = OlxItem(**item)
        except ValueError as e:
            self.logger.error(f"Failed to process item due to validation error: {e}")
            return

        yield listing_item
