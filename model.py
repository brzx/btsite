
from sqlalchemy import (
    Column, Integer, Sequence, String, DateTime, 
)
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Entity(Base):
    __tablename__ = 'entity'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    name = Column(String(50))
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return "<Entity('%d', '%s')>" % (self.id, self.name)

class AssetType(Base):
    __tablename__ = 'assettype'
    id = Column(Integer, autoincrement=True, primary_key=True)
    assetname = Column(String(200), nullable=False)
    detailtype = Column(String(200), nullable=False)
    isdeleted = Column(String(2), default='0')
    create_dt = Column(DateTime(), default=datetime.now)
    update_dt = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    def __repr__(self):
        return "<AssetType('%s', '%s')>" % (self.assetname, self.detailtype)