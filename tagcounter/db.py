import logging
import sqlalchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class DbRecSiteTagCounts(Base):
    __tablename__ = 'site_tag_counts'
    site_url = Column(String(), primary_key=True)  # name of site as id
    tag_counts_json = Column(String())

    def __repr__(self):
        return 'site_url=' + self.site_url + '   tag_counts_json=' + self.tag_counts_json


def init_db_session(file_db_sqlite):
    """Init DB session: connect to local sqlite DB and create tables if not existing"""
    db_engine = create_engine('sqlite:///' + file_db_sqlite)
    if not db_engine.has_table('site_tag_counts'):
        Base.metadata.create_all(db_engine)
    Base.metadata.bind = db_engine
    DBSession = sessionmaker(bind=db_engine)
    db_session = DBSession()
    return(db_session)


def write_to_db(url, tags_count_json, db_session):
    """keep in db (if not empty result)"""
    if (tags_count_json and tags_count_json != '{}'):
        db_session.query(DbRecSiteTagCounts).filter(DbRecSiteTagCounts.site_url == url).delete()
        db_session.commit()
        db_session.add(DbRecSiteTagCounts(site_url=url, tag_counts_json=tags_count_json))
        db_session.commit()


def view_from_db(url, db_session):
    tags_count_json = None
    try:
        db_recs = db_session.query(DbRecSiteTagCounts).filter(DbRecSiteTagCounts.site_url == url).all()
        if db_recs:
            tags_count_json = db_recs[-1].tag_counts_json
        else:
            logging.warning("No record found in data base for: " + url)
    except:
        logging.error("Unable to read from data base any record for: " + url)
    return tags_count_json



