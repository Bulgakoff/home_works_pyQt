import ipaddress
import subprocess

"""2. Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона.
 Меняться должен только последний октет каждого адреса.
  По результатам проверки должно выводиться соответствующее сообщение."""
# Создание объекта, описывающего сеть - функция ip_network()
subnet = ipaddress.ip_network("80.0.1.0/28")


# Просмотр всех хостов для объекта-сети
# print("hosts", list(subnet.hosts()), len(list(subnet.hosts())))
def host_ping(ip_address):
    with subprocess.Popen(["ping", "-c1", str(ip_address)]) as result:
        if result:
            print(ip_address, "Узел недоступен")
        else:
            print(ip_address, "Узел доступен")


def host_range_ping(ip_addresses):
    for ip in ip_addresses:
        host_ping(ip)


ip_addres = list(subnet.hosts())

host_range_ping(ip_addres)
