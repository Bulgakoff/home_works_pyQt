import ipaddress
import subprocess

"""1. Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов.
 Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или ip-адресом.
  В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения 
(«Узел доступен», «Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с помощью функции ip_address()."""


def create_lst_ip(num):
    ip_address = []
    for n in range(num):
        # ip = f'192.168.0.{n}/24'
        ip = ipaddress.ip_address("192.168.1.0")  # так не получается
        ip_address.append(ip)
    return ip_address


def host_ping(ip_address):
    with subprocess.Popen(["ping", "-c1", str(ip_address)]) as result:
        if result:
            print(ip_address, "Узел недоступен")
        else:
            print(ip_address, "Узел доступен")


def ip_network_check(ip_addr_list):
    for ip_addr in ip_addr_list:
        try:
            ipaddress.ip_network(ip_addr)
            print('Узел недоступен')
        except ValueError:
            print('Узел доступен')


N = 5
create_lst_ip(N)
create_lst_ip(N)
ip = ipaddress.ip_address('192.168.1.0')

host_ping(ip)
ip_network_check(create_lst_ip(N))
