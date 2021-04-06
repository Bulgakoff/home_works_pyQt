import sys
import time

from icecream import ic
from sqlalchemy import Column, ForeignKey, Integer, String, \
    exists, and_, DateTime, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import Engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class Client(Base):
    __tablename__ = 'client_parent'

    id = Column(Integer, primary_key=True)
    login = Column(String(20), unique=True)
    password = Column(String(100))

    children = relationship("ClientHistory", back_populates="parent")

    def __init__(self, login, password):
        self._login = login
        self._password = password

    def __repr__(self):
        return f"Client (login = {self._login})," \
               f" Client (password = {self._password})"


class ClientHistory(Base):
    __tablename__ = 'history_user_child'

    id = Column(Integer, primary_key=True)
    ip_address = Column(String(4 + 4 + 4 + 3), unique=True)
    connect_time = Column(Integer)
    parent_id = Column(Integer, ForeignKey('client_parent.id'))
    parent = relationship("Client", back_populates="children")

    def __init__(self, ip_address, parent_id, connect_time):
        self._ip_address = ip_address
        self._parent_id = parent_id
        self._connect_time = connect_time

    def __repr__(self):
        return f"<ClientHistory(_ip_address = '{self._ip_address}')," \
               f" (_connect_time = {self._connect_time})"


if __name__ == '__main__':
    engine = create_engine('sqlite:///anketa_2.db')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    parent_user = Client('foo', 'PaSsWord')
    ic("Classic Mapping. parent_user: ", parent_user)

    child_table = ClientHistory(1, '198.1.25.111', time.ctime())
    ic("Classic Mapping. child_user: ", child_table)

    session.add(parent_user)
    session.add(child_table)
    session.add_all(
        [
            Client('foo1', 'PaSsWord1'),
            Client('foo2', 'PaSsWord2'),
            Client('foo3', 'PaSsWord3'),
            ClientHistory(1, '198.1.25.1121', time.ctime()),
            ClientHistory(3, '198.1.25.1122', time.ctime()),
        ]
    )

    q_user = session.query(Client).filter_by(login="foo") \
        .first()
    ic("Simple query:", q_user)
    session.commit()
