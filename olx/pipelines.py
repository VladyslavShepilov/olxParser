from loguru import logger
from pydantic import ValidationError
from scrapy.exceptions import DropItem

from config.database import get_session
from models.olx_item import OlxItem
from olx.items import ItemValidator


class OlxDatabasePipeline:
    def __init__(self):
        self.session = get_session()
        self.logger = logger
        self.batch_size = 10

    def process_item(self, item, spider):
        self.logger.warning(f"Processing item: {item['olx_id']}")
        existing_item = (
            self.session.query(OlxItem).filter(OlxItem.olx_id == item["olx_id"]).first()
        )

        if not existing_item:
            new_item = OlxItem(**item)
            self.session.add(new_item)

        if len(self.session.new) >= self.batch_size:
            self.session.commit()
            self.logger.warning(f"Committing batch of {self.batch_size} items.")

        return item

    def close_spider(self, spider):
        if self.session.new:
            self.session.commit()
        self.session.close()

        def close_spider(self, spider):
            self.logger.warning("Closing the spider and closing the database session.")
            self.session.close()


class OlxItemValidationPipeline:
    def process_item(self, item, spider):
        try:
            validated_item = ItemValidator(**item)
            logger.warning(f"Validated item: {validated_item}")
            return validated_item.model_dump()
        except ValidationError as e:
            logger.error(f"Validation error for item {item.get('olx_id')}: {e}")
            raise DropItem(f"Invalid item: {e}") from e
