#!/usr/bin/env python

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from setup import DB_PATH
from collectors import QuadrigaxCollector, CoinsquareCollector, TaurusCollector

# Get a session
engine = create_engine(DB_PATH)
DBSession = sessionmaker(bind=engine)
session = DBSession()

try:
    quad = QuadrigaxCollector()
    qb = quad.get_book()
    qb.store(session=session)
except:
    pass

try:
    taurus = TaurusCollector()
    tb = taurus.get_book()
    tb.store(session=session)
except:
    pass

try:
    coin = CoinsquareCollector()
    cb, ct = coin.get_book()
    cb.store(session=session)
except:
    pass
