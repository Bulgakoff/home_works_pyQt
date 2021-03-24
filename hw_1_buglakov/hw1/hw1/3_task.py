import ipaddress
import subprocess
from pprint import pprint

from tabulate import tabulate

"""3. Написать функцию host_range_ping_tab(), возможности которой основаны на функции из примера 2.
 Но в данном случае результат должен быть итоговым по всем ip-адресам, представленным в табличном формате
  (использовать модуль tabulate). Таблица должна состоять из двух колонок и выглядеть примерно так:
Reachable
10.0.0.1
10.0.0.2
Unreachable
10.0.0.3
10.0.0.4
"""


def create_lst_ip(num):
    ip_address = []
    for n in range(num):
        # ip = f'192.168.0.{n}/24'
        ip = format(ipaddress.ip_address(f"192.168.1.{n}"))  # так не получается
        ip_address.append(ip)
    return ip_address


print(create_lst_ip(5))


def host_ping(ip_address):
    return subprocess.call(["ping", "/n", "1", ip_address],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL) == 0


ip = format(ipaddress.ip_address("192.168.1.1"))
print(host_ping('google.com'))


def host_range_ping(ip_addresses):
    result = {}
    for ip in ip_addresses:
        result[ip] = host_ping(ip)
    return result

# Табличное представление списка словарей
dict_ip = host_range_ping(create_lst_ip(7))
print(tabulate([dict_ip], headers="keys", tablefmt="grid"))
