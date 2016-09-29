#!/usr/bin/env python
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from setup import DB_PATH
from collectors import QuadrigaxCollector, CoinsquareCollector, KrakenCollector

engine = create_engine(DB_PATH)
DBSession = sessionmaker(bind=engine)
session = DBSession()

try:
    quad = QuadrigaxCollector()
    qp = quad.get_price()
    qp.store(session=session)
except:
    pass

try:
    coin = CoinsquareCollector()
    cp = coin.get_price()
    cp.store(session=session)
except:
    pass

try:
    kranken = KrakenCollector()
    kp = kranken.get_price()
    kp.store(session=session)
except:
    pass
