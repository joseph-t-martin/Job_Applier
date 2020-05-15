from models.sites import Sites
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.sql import func
Base = declarative_base()


class Jobs(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    site_id = Column(Integer, ForeignKey(Sites.id))
    job_title = Column(String)
    url = Column(String)
    submitted = Column(Boolean)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __init__(self, job_title=None, url=None):
        self.job_title = job_title
        self.url = url

    def __repr__(self):
        return '<Jobs %r>' % self.job_title
