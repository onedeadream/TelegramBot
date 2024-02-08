from aiogram.fsm.state import StatesGroup, State
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP
import sqlalchemy.orm as orm
from config import URL_DATABASE

Base = orm.declarative_base()
engine = create_engine(URL_DATABASE)
connection = engine.connect()


class Events(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    event_name = Column(String)
    event_time = Column(TIMESTAMP)


class DialogStates(StatesGroup):
    name_event = State()
    time_event = State()
    edit_event = State()


Base.metadata.create_all(engine)
Session = orm.sessionmaker(bind=engine)
session = Session()



