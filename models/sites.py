from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

Base = declarative_base()


class Sites(Base):
    __tablename__ = 'sites'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, name=None, url=None):
        self.name = name
        self.url = url

    def __repr__(self):
        return '<Sites %r>' % self.name
