import pytest
from pj_class.server import ServerProp, Server

def test_init():
    name = 'port'
    type_name = int
    # default = 1111

    sut = ServerProp(name, type_name,"1111")
    assert sut.default == '1111'


def test_default():
    name = 'port'
    type_name = int
    sut = Server()
    sut2 = ServerProp(name, type_name)
    # assert sut2.name == sut.port
    assert sut2.default == 7777
    # assert sut2.type == sut.port

def test_type():
    name = 'port'
    type_name = int
    sut = Server()
    sut2 = ServerProp(name, type_name, "1111")
    # assert sut2.name == sut.port
    # assert sut2.default == sut.port
    assert sut2.type == int

def test_name():
    name = 'port'
    type_name = int
    sut = Server()
    sut2 = ServerProp(name, type_name, "1111")
    # assert sut2.name == sut.port
    # assert sut2.default == sut.port
    assert sut2.name == '_port'

def test_get_get():
    qwe = object()
    name = 'port'
    type_name = int
    sut4 = Server()
    sut3 = ServerProp(name, type_name)
    assert sut3.__get__(sut4,qwe) == 7777

def test_set():
    qwe = object()
    name = 'port'
    type_name = str
    sut5 = Server()
    sut6 = ServerProp(name, type_name,10000)
    assert sut6.__set__(sut5,10000) == 7777