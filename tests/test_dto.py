from datetime import datetime

from src.dto import Payment, Operation

def test_init_payment_from_str():
    payment = Payment.init_from_str('Visa Classic 6831982476737658')
    assert payment.name == 'Visa Classic'
    assert payment.number == '6831982476737658'


def test_safe_payment_for_amount():
    payment = Payment(name='Счет', number='64686473678894779589')
    assert payment.safe() == 'Счет **9589'


def test_safe_payment_for_card_number():
    payment = Payment(name='MasterCard', number='7158300734726758')
    assert payment.safe() == 'MasterCard 7158 30** **** 6758'


def test_split_card_number_by_blocks():
    card_number = '7158300734726758'
    result = Payment.split_card_number_by_blocks(card_number)
    assert result == '7158 3007 3472 6758'


def test_init_operation_from_dict(operation_data_without_from):
    op = Operation.init_from_dict(operation_data_without_from)

    assert op.id == 41428829
    assert op.state == 'EXECUTED'
    assert op.date == datetime(2019, 7, 3, 18, 35, 29, 512364)
    assert op.amount.value == 8221.37
    assert op.amount.currency_name == 'USD'
    assert op.amount.currency_code == 'USD'
    assert op.description == 'Открытие вклада'
    assert op.payment_to.name == 'Счет'
    assert op.payment_to.number == '35383033474447895560'
    assert op.payment_from is None



def test_safe_operation_with_from(operation_data_with_from):
    operation = Operation.init_from_dict(operation_data_with_from)
    expected_result = (
        '03.07.2019 Перевод организации\n'
        'MasterCard 7158 30** **** 6758 -> Счет **5560\n'
        '8221.37 USD'
    )

    assert operation.safe() == expected_result


def test_safe_operation_without_from(operation_data_without_from):
    operation = Operation.init_from_dict(operation_data_without_from)
    expected_result = (
        '03.07.2019 Открытие вклада\n'
        'Счет **5560\n'
        '8221.37 USD'
    )

    assert operation.safe() == expected_result


