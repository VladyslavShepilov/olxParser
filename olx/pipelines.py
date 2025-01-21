# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from config.database import get_session
from olx.items import OlxItem

class DatabasePipeline:
    def __init__(self):
        self.session = get_session()

    def process_item(self, item, spider):
        existing_item = self.session.query(OlxItem).filter(OlxItem.url == item['olx_od']).first()
        
        if not existing_item:
            # Add new item if no duplicates
            new_item = OlxItem(**item)
            self.session.add(new_item)
            self.session.commit()
        return item

    def close_spider(self, spider):
        self.session.close()
