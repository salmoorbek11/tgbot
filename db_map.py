from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class MediaIds(Base):
    __tablename__ = 'MediaIds'
    id = Column(Integer, primary_key=True)
    id_user = Column(Integer)
    file_id = Column(String(255))
    file_name = Column(String(255))
    file_type = Column(String(255))