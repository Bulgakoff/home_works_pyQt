import ipaddress
import subprocess

"""1. Написать ф-ию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов.
 Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или ip-адресом.
  В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения 
(«Узел доступен», «Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с помощью функции ip_address()."""


def host_ping(ip_address):
    return subprocess.call(["ping", "/n", "1", ip_address],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL) == 0


ip = format(ipaddress.ip_address("192.168.1.1"))
print(host_ping('google.com'))