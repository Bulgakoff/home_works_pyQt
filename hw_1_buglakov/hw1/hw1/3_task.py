import ipaddress
import subprocess
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

subnet = ipaddress.ip_network("80.0.1.0/28")


def host_ping(ip_address):
    tuples_list_ip = []
    with subprocess.Popen(["ping", "-c1", str(ip_address)]) as result:
        if result:
            tuples_list_ip.append((ip_address, "Узел недоступен"))
        else:
            tuples_list_ip.append((ip_address, "Узел недоступен"))
    return tuples_list_ip


def host_range_ping_tab(ip_addresses):
    tuples_list_last = []
    for ip in ip_addresses:
        tuples_list_last += host_ping(ip)
    return tuples_list_last


ip_addres = list(subnet.hosts())
columns = ["HOST", "status"]
tuples_list = host_range_ping_tab(ip_addres)
table = tabulate(tuples_list, headers=columns)
print(table)
