import sys
import time

from icecream import ic
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    exists,
    and_,
    DateTime,
    event,
    Table,
    select,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import Engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """implements the operation of a foreign key"""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


node_to_node = Table(
    "node_to_node",
    Base.metadata,
    Column("left_node_id", Integer, ForeignKey("client_parent.id"), primary_key=True),
    Column("right_node_id", Integer, ForeignKey("client_parent.id"), primary_key=True),
)


class Client(Base):
    """User Table"""

    __tablename__ = "client_parent"

    id = Column(Integer, primary_key=True)
    login = Column(String(20), unique=True)
    password = Column(String(100))
    children = relationship("ClientHistory", back_populates="parent")

    right_nodes = relationship(
        "Client",
        secondary=node_to_node,
        primaryjoin=id == node_to_node.c.left_node_id,
        secondaryjoin=id == node_to_node.c.right_node_id,
    )

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def __repr__(self):
        return (
            f"Client (login = {self.login}),"
            f" Client (password = {self.password}),"
            f" right_nodes === > {self.right_nodes}"
        )


class ClientHistory(Base):
    """Table with connection history users"""

    __tablename__ = "history_user_child"

    id = Column(Integer, primary_key=True)
    ip_address = Column(String(4 + 4 + 4 + 3), unique=True)
    connect_time = Column(Integer)
    parent_id = Column(Integer, ForeignKey("client_parent.id"))
    parent = relationship("Client", back_populates="children")

    def __init__(self, ip_address, parent_id, connect_time):
        self.ip_address = ip_address
        self.parent_id = parent_id
        self.connect_time = connect_time

    def __repr__(self):
        return (
            f"<ClientHistory(_ip_address = '{self.ip_address}'),"
            f" (_connect_time = {self.connect_time})"
        )


if __name__ == "__main__":
    engine = create_engine("sqlite:///anketa_3.db")
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # ==================================
    u1, u2, u3, u4, ch5, ch6 = (
        Client("fooq2", "PaSsWord"),
        Client(login="foo112", password="PaSsWord1"),
        Client("foo222", "PaSsWord2"),
        Client("foo332", "PaSsWord3"),
        ClientHistory(
            ip_address="198.1.25.112112", parent_id=1, connect_time=time.ctime()
        ),
        ClientHistory("198.1.25.1e1312", 3, time.ctime()),
    )
    u1.right_nodes = [u2, u4, u3]
    u4.right_nodes = [u1]
    #: u4.right_nodes.append(u4)
    session.add_all([u1, u2, u3, u4, ch5, ch6])

    q_user = session.query(ClientHistory).filter_by(parent_id=1).first()
    print()
    ic("Simple query:", q_user)
    session.commit()
