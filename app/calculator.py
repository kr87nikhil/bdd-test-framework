class Calculator:
    """Calculator for basic operations"""
    ADDITION_SYMBOL = '+'
    SUBTRACTION_SYMBOL = '-'
    MULTIPLICATION_SYMBOL = '*'
    DIVISION_SYMBOL = '/'
    SPACE_CHARACTER = ' '
    NEW_LINE_CHARACTER = '\n'
    operation_history = []

    @classmethod
    def add(cls, first_num, second_num):
        """Add 2 numbers"""
        cls.save_operation(first_num, second_num, cls.ADDITION_SYMBOL)
        return first_num + second_num

    @classmethod
    def subtract(cls, first_num, second_num):
        """Subtract first argument from second argument"""
        cls.save_operation(first_num, second_num, cls.SUBTRACTION_SYMBOL)
        return first_num - second_num

    @classmethod
    def multiply(cls, first_num, second_num):
        """Multiply 2 numbers"""
        cls.save_operation(first_num, second_num, cls.MULTIPLICATION_SYMBOL)
        return first_num * second_num

    @classmethod
    def division(cls, first_num, second_num):
        """Divide first argument by second argument"""
        cls.save_operation(first_num, second_num, cls.DIVISION_SYMBOL)
        return first_num / second_num

    @classmethod
    def save_operation(cls, first_num, second_num, operation_symbol):
        """Save operation history"""
        cls.operation_history.append(str(first_num) + cls.SPACE_CHARACTER + operation_symbol +
                                     cls.SPACE_CHARACTER + str(second_num))

    @classmethod
    def show_history(cls):
        """Show history for all operations"""
        for operation in cls.operation_history:
            print(operation, end=', ')
