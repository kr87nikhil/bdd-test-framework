from pytest_bdd import when, then, scenarios
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
def result_should_be(actual_result, expected_result):
    assert float(expected_result) == actual_result, 'Calculator operation result should match'
