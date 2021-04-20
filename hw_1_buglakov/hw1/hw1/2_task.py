import ipaddress
import subprocess
from pprint import pprint

"""2. Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона.
 Меняться должен только последний октет каждого адреса.
  По результатам проверки должно выводиться соответствующее сообщение."""


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
    pprint(result)


host_range_ping(create_lst_ip(7))
