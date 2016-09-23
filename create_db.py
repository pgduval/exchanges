from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, ForeignKeyConstraint, PrimaryKeyConstraint, Float

from setup import DB_PATH

Base = declarative_base()


class DBOrderPull(Base):

    __tablename__ = 'orderpull'

    book_id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    ticker = Column(String, nullable=False)
    provider = Column(String, nullable=False)


class DBOrderBook(Base):

    __tablename__ = 'orderbook'

    id = Column(Integer, autoincrement=True, primary_key=True)
    book_id = Column(Integer, ForeignKey('orderpull.book_id'))
    price = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)
    side = Column(String, nullable=False)


class DBPrice(Base):

    __tablename__ = 'price'

    price_id = Column(Integer, autoincrement=True, primary_key=True)
    ticker = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    last = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    bid = Column(Float, nullable=False)
    ask = Column(Float, nullable=False)


class DBTransactPull(Base):

    __tablename__ = 'transactpull'

    transact_id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    ticker = Column(String, nullable=False)
    provider = Column(String, nullable=False)


class DBTransaction(Base):

    __tablename__ = 'transaction'

    id = Column(Integer, autoincrement=True, primary_key=True)
    transact_id = Column(Integer, ForeignKey('transactpull.transact_id'))
    trade_date = Column(DateTime, nullable=False)
    tid = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)
    side = Column(String, nullable=False)


if __name__ == '__main__':
    engine = create_engine(DB_PATH, echo=True)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)

    session = Session()
