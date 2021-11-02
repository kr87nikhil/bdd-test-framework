import pytest
from pytest_bdd import when, then, parsers, scenarios
from app.calculator import Calculator

name_operation_mapping = {
    'ADDITION': Calculator.add,
    'DIVISION': Calculator.division,
    'SUBTRACTION': Calculator.subtract,
    'MULTIPLICATION': Calculator.multiply
}
scenarios('calculator.feature')


@when(
    "<first_number> is operated with <operation> by <second_number>",
    target_fixture='actual_result'
)
def is_operated_with_by(first_number, operation, second_number):
    calculator_operation = name_operation_mapping.get(operation)
    return calculator_operation(float(first_number), float(second_number))


@then("result should be <expected_result>")
def result_should_be(expected_result, actual_result):
    assert float(expected_result) == actual_result, 'Calculator operation result should match'


@when(
    parsers.parse("{number:d} is divided by zero")
)
def is_divided_by_zero(number):
    pass


@then("divide by zero exception should be raised")
def divide_by_zero_exception_should_be_raised(number):
    with pytest.raises(ZeroDivisionError) as exp:
        name_operation_mapping.get('DIVISION')(number, 0)
    assert str(exp.value) == 'Division by Zero is attempted', 'Zero division error should be raised'
