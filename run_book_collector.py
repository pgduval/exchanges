from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from setup import DB_PATH
from collectors import QuadrigaxCollector, CoinsquareCollector

# Get a 
engine = create_engine(DB_PATH)
DBSession = sessionmaker(bind=engine)
session = DBSession()

quad = QuadrigaxCollector()
qb = quad.get_book()
qb.store(session=session)
# qp = quad.get_price()
# qp.store(session=session)
# qt = quad.get_transaction()
# qt.store(session=session)

coin = CoinsquareCollector()
cb, ct = coin.get_book()
cb.store(session=session)
# ct.store(session=session)
# cp = coin.get_price()
# cp.store(session=session)
