#!/usr/bin/env python

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from setup import DB_PATH
from collectors import QuadrigaxCollector, CoinsquareCollector

engine = create_engine(DB_PATH)
DBSession = sessionmaker(bind=engine)
session = DBSession()

try:
    quad = QuadrigaxCollector()
    qt = quad.get_transaction()
    qt.store(session=session)
except:
    pass

try:
    coin = CoinsquareCollector()
    cb, ct = coin.get_book()
    ct.store(session=session)
except:
    pass
