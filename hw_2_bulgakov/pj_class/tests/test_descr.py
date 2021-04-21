import pytest
from pj_class.server import ServerProp


class ServerrSocket:
    port = ServerProp(default=7777)


def test_init():
    sut = ServerrSocket()
    assert sut.port == 7777


def test_set():
    sut = ServerrSocket()
    sut.port = 1234
    assert sut.port == 1234


# def test_set_1_raises_error():
#     sut = ServerrSocket()
#     with pytest.raises(ValueError):
#         sut.port = 0
#
#
# def test_set_1_raises_66666():
#     sut = ServerrSocket()
#     with pytest.raises(ValueError):
#         sut.port = 77777
data_set = [(0, ValueError), (825855, ValueError),
            ("qwe", TypeError), (10.5, TypeError),
            (object(), TypeError)]


@pytest.mark.parametrize("value,exp_val", data_set)
def test_set_invalid_raises_value_error(value, exp_val):
    sut = ServerrSocket()
    with pytest.raises(exp_val):
        sut.port = value


def test_multi_use_stores_different_values():
    class Sut:
        port1 = ServerProp(8888)
        port2 = ServerProp(8888)

    sut = Sut()
    sut.port1 = 100
    sut.port2 = 200
    assert sut.port1 == 100
    assert sut.port2 == 200


def test_multi_instance_store_different_values():
    sut1 = ServerrSocket()
    sut2 = ServerrSocket()

    sut1.port = 100
    sut2.port = 200

    assert sut1.port == 100
    assert sut2.port == 200


# @pytest.mark.parametrize("param", ["qwe", 10.5, object(),5555])
# def test_set_wrong_type_raises_type_error(param):
#     sut = ServerrSocket()
#     with pytest.raises(TypeError):
#         sut.port = param
@pytest.mark.parametrize("value,exp_val",
                         data_set)
def test_invalid_raises_default_error(value, exp_val):
    with pytest.raises(exp_val):
        class Sut:
            port = ServerProp(default=value)
