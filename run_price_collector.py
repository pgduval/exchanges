from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from setup import DB_PATH
from collectors import QuadrigaxCollector, CoinsquareCollector

engine = create_engine(DB_PATH)
DBSession = sessionmaker(bind=engine)
session = DBSession()

quad = QuadrigaxCollector()
qp = quad.get_price()
qp.store(session=session)

coin = CoinsquareCollector()
cp = coin.get_price()
cp.store(session=session)
