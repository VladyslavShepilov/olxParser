from sqlalchemy import create_engine, Column, Integer, BigInteger, String, Text, DateTime, Enum
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class OlxItem(Base):
    __tablename__ = 'olx_items'

    id = Column(BigInteger, primary_key=True, unique=True)
    views = Column(Integer)
    title = Column(String(255))
    price = Column(String(255))
    published_at = Column(DateTime, nullable=True)
    description = Column(Text, nullable=True)
    images = Column(Text, nullable=True)
    tags = Column(Text, nullable=True)
    lang = Column(Enum('uk', 'ru', name='lang_enum'), default='uk')

    def __repr__(self):
        return f"<OlxItem(id={self.id}, title={self.title})>"
