import sys
from icecream import ic
from sqlalchemy import Column, ForeignKey, Integer, String, \
    exists, and_, DateTime, event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import Engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import time

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# создание экземпляра declarative_base
Base = declarative_base()

# здесь добавим классы
# мы создаем класс Book наследуя его из класса Base.
class Client(Base):
    __tablename__ = 'client'

    client_id = Column(Integer, primary_key=True)
    login = Column(String(20), unique=True)
    password = Column(String(100))

    cli_history = relationship("ClientHistory", back_populates="client_id")

    def __repr__(self):
        return f"<Client(id = '{self.id}')," \
               f" (login = {self.login})," \
               f" (password = {self.password})"


class ClientStorage:
    def __init__(self, session):
        self._session = session

    def client_add(self, login, password):
        try:
            with self._session.begin():
                self._session.add(Client(login=login, password=password))
        except IntegrityError as e:
            raise ValueError('Логин должен быть уникальным') from e

    def client_exists(self, login, password):
        stmt = exists().where(and_(Client.login == login, Client.password == password))
        return self._session.query(Client).filter(stmt).first() != None

    def find(self, client_id):
        """Возвращается  Датакласс с id, login, password"""
        pass


class ClientHistory(Base):
    __tablename__ = 'client_history'

    ClientHistoryId = Column(Integer, primary_key=True)
    ip_address = Column(String(4 + 4 + 4 + 3), unique=True)
    connect_time = Column(Integer)
    # connect_time = Column(DateTime)

    client_id = Column(Integer, ForeignKey('client.client_id'))
    client = relationship("Client", back_populates="cli_history")



class ClientHistoryStorage:
    def __init__(self, session):
        self._session = session

    def add_record(self, client_id, address, tm):
        with self._session.begin():
            self._session.add(ClientHistory(ClientId=client_id,
                                            ip_address=address,
                                            connect_time=tm))


if __name__ == '__main__':
    engine = create_engine('sqlite:///qwe_sqlite1.db')
    Base.metadata.create_all(engine)  # создает все
    # таблицы что обнаружил
    Session = sessionmaker(bind=engine)
    session = Session()

    parent_user = ClientStorage(session)
    parent_user.client_add('foo', 'PaSsWord')
    exists = parent_user.client_exists('foo', 'PaSsWord')

    ic(exists)
    session.commit()

    # with Session() as session:
        # client_storage = ClientStorage(session)
        # client_storage.client_add('foo', 'PaSsWord')
        # exists = client_storage.client_exists('foo', 'PaSsWord')

        # ic(exists)

        # client_history_storage = ClientHistoryStorage(session)
        # client_history_storage.add_record(1,'198.1.25.111',time.ctime())
