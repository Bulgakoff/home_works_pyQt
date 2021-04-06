import sys
import time

from icecream import ic
from sqlalchemy import Column, ForeignKey, Integer, String, \
    exists, and_, DateTime, event, Table
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

# association_table = Table('association', Base.metadata,
#     Column('host_id', Integer, ForeignKey('client_parent.id')),
#     Column('user_id', Integer, ForeignKey('client_parent.id'))
# )

class Client(Base):
    __tablename__ = 'client_parent'

    id = Column(Integer, primary_key=True)
    login = Column(String(20), unique=True)
    password = Column(String(100))

    children = relationship("ClientHistory", back_populates="parent")
    # host_user = relationship("Client")


    def __init__(self, login, password):
        self.login = login
        self.password = password

    def __repr__(self):
        return f"Client (login = {self.login})," \
               f" Client (password = {self.password})"


class ClientHistory(Base):
    __tablename__ = 'history_user_child'

    id = Column(Integer, primary_key=True)
    ip_address = Column(String(4 + 4 + 4 + 3), unique=True)
    connect_time = Column(Integer)
    parent_id = Column(Integer, ForeignKey('client_parent.id'))
    parent = relationship("Client", back_populates="children")

    def __init__(self, ip_address, parent_id, connect_time):
        self.ip_address = ip_address
        self.parent_id = parent_id
        self.connect_time = connect_time

    def __repr__(self):
        return f"<ClientHistory(_ip_address = '{self.ip_address}')," \
               f" (_connect_time = {self.connect_time})"


if __name__ == '__main__':
    engine = create_engine('sqlite:///anketa_2.db')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    parent_user = Client('fooq2', 'PaSsWord')
    ic("Classic Mapping. parent_user: ", parent_user)

    child_table = ClientHistory('198.1.25.1112', 1, time.ctime())
    ic("Classic Mapping. child_user: ", child_table)

    session.add(parent_user)
    session.add(child_table)
    session.add_all(
        [
            Client('foo112', 'PaSsWord1'),
            Client('foo222', 'PaSsWord2'),
            Client('foo332', 'PaSsWord3'),
            ClientHistory('198.1.25.112112', 1, time.ctime()),
            ClientHistory('198.1.25.112222', 2, time.ctime()),
        ]
    )

    q_user = session.query(Client).filter_by(login="foo") \
        .first()
    ic("Simple query:", q_user)
    session.commit()
