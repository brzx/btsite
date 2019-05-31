
from sqlalchemy import (
    Column, Integer, Sequence, String, DateTime, 
    Float, DECIMAL, ForeignKey, 
)
from sqlalchemy.orm import relationship
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

    children = relationship('Asset')

    def __repr__(self):
        return "<AssetType('%s', '%s')>" % (self.assetname, self.detailtype)

class Asset(Base):
    __tablename__ = 'asset'
    id = Column(Integer, autoincrement=True, primary_key=True)
    asiden = Column(String(200), nullable=False)
    asorgan = Column(String(200), nullable=False)
    bill_dt = Column(String(50))
    repayment_dt = Column(String(50))
    credit_limit = Column(String(50))
    year_rate = Column(String(50))
    comment = Column(String(200))
    isdeleted = Column(String(2), default='0')
    create_dt = Column(DateTime(), default=datetime.now)
    update_dt = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    assettype_id = Column(Integer, ForeignKey('assettype.id'))

    children = relationship('AssetRecord')

    def __repr__(self):
        return "<Asset('%s', '%s')>" % (self.asiden, self.asorgan)

class AssetRecord(Base):
    __tablename__ = 'assetrecord'
    id = Column(Integer, autoincrement=True, primary_key=True)
    amount = Column(Float, nullable=False)
    comment = Column(String(200))
    isdeleted = Column(String(2), default='0')
    create_dt = Column(DateTime(), default=datetime.now)
    update_dt = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    asset_id = Column(Integer, ForeignKey('asset.id'))

    def __repr__(self):
        return "<AssetRecord('%s', '%s')>" % (self.asiden, self.asorgan)
