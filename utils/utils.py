# from pydantic import BaseModel
# from datetime import date
from sqlalchemy import Column, Integer, Date, String, MetaData, Table
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select, create_engine

from config import settings
import pandas as pd
from enum import Enum


class Weekday(Enum):
    Monday = 0
    Tuesday = 1
    Wednesday = 2
    Thursday = 3
    Friday = 4
    Saturday = 5
    Sunday = 6


metadata_object = MetaData()

times_table = Table(
    "times",
    metadata_object,
    Column("id", Integer, primary_key=True),
    Column("date", Date),
    Column("time", Integer),
    Column("weekday", String),
    Column("productivity", String)
)


class Base(DeclarativeBase):
    pass


class Day(Base):
    __tablename__ = "times"

    id = Column(Integer, primary_key=True, nullable=False)
    date = Column(Date, unique=True)
    time = Column(Integer)
    weekday = Column(String(10))
    productivity = Column(String(5))


def get_productivity_value(time: int):
    result = "Low"

    if (time > 150 and time <= 300):
        result = "Norm"
    elif (time > 300):
        result = "High"

    return result


def get_df_from_table_from_db():
    """Convert table from database to pandas.dataframe"""
    """The database and table are specified in the .env file"""
    engine = create_engine(
        url=settings.get_db_url_psycopg,
        echo=True
    )

    result_df = pd.DataFrame()

    with engine.connect() as conn:
        result_df = pd.read_sql_query(select(times_table),
                                      con=conn)

        result_df.set_index("id", inplace=True)
        result_df["date"] = pd.to_datetime(result_df["date"])

    return result_df
