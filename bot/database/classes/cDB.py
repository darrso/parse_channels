from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///database/parser.db", echo=True)
base = declarative_base()


class Posts(base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    public = Column(String)
    post_id = Column(Integer, unique=True)


class Users(base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    user_name = Column(String)

    on_off = Column(String)
    parse_channels = Column(String)

# СОЗДАНИЕ БАЗЫ ПО СХЕМЕ
# base.metadata.create_all(engine)
