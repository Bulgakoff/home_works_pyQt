from serializer import Serializer
from DataCl import *
from m_chat.disconnector import Disconnector


class MessageProcessor:
    def __init__(self,
                 serializer=Serializer()
                 ):
        self._serializer = serializer

    def on_auth_response(self, msg_data_class):
        """вызывать сериалайзер для превращения сообщения в байты,
         а потом передавать эти байты в  SendBuffer """
        if msg_data_class.response != "200":
            pass
            # self._disconnector.disconnect()
        else:
            presence = Presence('Bob', '"Yep, I am here!"')
            data = self._serializer.serialize(presence)
            self._send_buffer.send(data)

    def on_auth(self, msg_data_class):
        if msg_data_class.action != "authenticate":
            response_err = ResponceError('402', 'epic fail')
            # формируем другой дата класс для ответа в сериализатор
            data = self._serializer.serialize(response_err)
            self._send_buffer.send(data)
        else:
            responce_ok = Responce('200', 'okok')
            data = self._serializer.serialize(responce_ok)
            self._send_buffer.send(data)
            # как выглядит добавление в список клиентов?

    def on_probe(self, msg_data_class):
        # добавляем в список клиентов ?????
        if msg_data_class.action == "probe!!!":
            response_err = AnwQuit('quit')
            data = self.serialize(response_err)
            time.sleep(10)
            self.send(data)
        else:
            pass
