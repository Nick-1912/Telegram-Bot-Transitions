from states import Ordering
import pytest

class Tests:
    pass

def send_message_result(text, _):
    print(text)


def test_init():
    order = Ordering(send_message_result, 0)
    assert order.state == 'start'
    order.start()


def test_dialog_1():
    order = Ordering(send_message_result, 0)
    assert order.state == 'start'
    order.start()

    assert order.state == 'pizza_size'
    order.get_message('Большую')
    assert order.state == 'pay_type'
    order.get_message('Картой')
    assert order.state == 'confirm'
    order.get_message('да')
    assert order.state == 'end'



def test_dialog_2():
    order = Ordering(send_message_result, 0)
    assert order.state == 'start'
    order.start()

    assert order.state == 'pizza_size'
    order.get_message('маленькую')
    assert order.state == 'pay_type'
    order.get_message('наличкой')
    assert order.state == 'confirm'
    order.get_message('да')
    assert order.state == 'end'

def test_dialog_3():
    order = Ordering(send_message_result, 0)
    assert order.state == 'start'
    order.start()

    assert order.state == 'pizza_size'
    order.get_message('hi')
    assert order.state == 'pizza_size'
    order.get_message('hi')
    assert order.state == 'pizza_size'
    order.get_message('Большую')
    assert order.state == 'pay_type'
    order.get_message('Картой')
    assert order.state == 'confirm'
    order.get_message('да')
    assert order.state == 'end'

def test_dialog_4():
    order = Ordering(send_message_result, 0)
    assert order.state == 'start'
    order.start()

    assert order.state == 'pizza_size'
    order.get_message('Большую')
    assert order.state == 'pay_type'
    order.get_message('Точно не картой')
    assert order.state == 'pay_type'
    order.get_message('картой')
    assert order.state == 'confirm'
    order.get_message('да')
    assert order.state == 'end'