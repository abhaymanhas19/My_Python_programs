from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import declarative_base

base = declarative_base()


engine = create_engine("sqlite:///test.sqlite")
conn = engine.connect()



class User(base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True)
    name = Column(String)

base.metadata.create_all(engine)
