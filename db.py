from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


PG_DSN = 'postgresql+asyncpg://'

engine = create_async_engine(PG_DSN)

Base = declarative_base()


class People(Base):

    __tablename__ = 'character'

    id = Column(Integer, primary_key=True, autoincrement=True)
    birth_year = Column(String(30))
    eye_color = Column(String(30))
    films = Column(String(500))
    gender = Column(String(30))
    hair_color = Column(String(30))
    height = Column(String(30))
    homeworld = Column(String(30))
    mass = Column(String(30))
    name = Column(String(30))
    skin_color = Column(String(30))
    species = Column(String(500))
    starships = Column(String(500))
    vehicles = Column(String(500))

Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
