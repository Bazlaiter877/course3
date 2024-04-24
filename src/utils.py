import json

from src.dto import Operation


def get_operations(filename):
    operations = []
    with open(filename, encoding='utf-8') as f:
        for data in json.load(f):
            if data:
                op = Operation.init_from_dict(data)
                operations.append(op)

    return operations


def filter_operation_by_state(*operations, state):
    filter_operation = []
    for op in operations:
        if op.state == state:
            filter_operation.append(op)
    return filter_operation


def sort_operation_by_date(*operations: Operation):
    return sorted(operations, key=lambda op: op.date, reverse=True)
