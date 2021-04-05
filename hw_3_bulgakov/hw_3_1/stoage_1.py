import sys
# для настройки баз данных
from icecream import ic
from sqlalchemy import Column, ForeignKey, Integer, String, exists, and_, DateTime
# для определения таблицы и модели
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
# для создания отношений между таблицами
from sqlalchemy.orm import relationship, sessionmaker
# для настроек
from sqlalchemy import create_engine

# создание экземпляра declarative_base
Base = declarative_base()
import time

# здесь добавим классы
# мы создаем класс Book наследуя его из класса Base.
class Client(Base):
    __tablename__ = 'Client'

    ClientId = Column(Integer, primary_key=True)
    login = Column(String(20), unique=True)
    password = Column(String(100))

    ClientHistory = relationship("ClientHistory", back_populates="Client")
    # client_history_id = Column(Integer, ForeignKey('client_history.id'))

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
    __tablename__ = 'ClientHistory'

    ClientHistoryId = Column(Integer, primary_key=True)
    ip_address = Column(String(4 + 4 + 4 + 3), unique=True)
    connect_time = Column(String)
    # connect_time = Column(DateTime)

    ClientId = Column(Integer, ForeignKey('Client.ClientId'))
    Client = relationship("Client", back_populates="ClientHistory")



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

    with Session() as session:
        # client_storage = ClientStorage(session)
        # client_storage.client_add('foo', 'PaSsWord')
        # exists = client_storage.client_exists('foo', 'PaSsWord')

        # ic(exists)

        client_history_storage = ClientHistoryStorage(session)
        client_history_storage.add_record(223,'198.1.25.10','2008-11-22')
