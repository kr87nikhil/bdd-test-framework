from parse import compile


class StepTable:
    """Step table parser utility class"""
    KEY_TEXT = 'key'
    EMPTY_TEXT = ''
    VALUE_TEXT = 'value'
    NESTED_KEY_TEXT = 'nested_key'
    EMPTY_DOUBLE_QUOTES = '""'
    NEW_LINE_CHARACTER = '\n'
    LESS_THAN_CHARACTER = '<'
    GREATER_THAN_CHARACTER = '>'
    key_value_schema = compile('|{key:^w}|{value:^}|')
    nested_key_value_schema = compile('|{key:^w}|{nested_key:^}|{value:^}|')

    @staticmethod
    def parse_step_table(step_table: str):
        """Parse static step table

        Note:
            Empty key is not accepted, will raise Exception
            Key value mapping with empty value will be ignored
        """
        table_dict = {}
        for line in step_table.split(StepTable.NEW_LINE_CHARACTER):
            if line == StepTable.EMPTY_TEXT:
                break
            result = StepTable.key_value_schema.parse(line)
            if result is None:
                raise Exception('Step Error: Unable to parse step table')
            else:
                if result.named[StepTable.VALUE_TEXT].strip() == StepTable.EMPTY_TEXT:
                    continue
                table_dict.update({
                    result.named.get(StepTable.KEY_TEXT): result.named.get(StepTable.VALUE_TEXT)
                })
        return table_dict

    @staticmethod
    def parse_nested_key_step_table(step_table: str):
        """Parse static nested step table

        Note:
            Empty key is not accepted, will raise Exception
            If empty value, simple or nested key value be ignored
        """
        table_dict = {}
        for line in step_table.split(StepTable.NEW_LINE_CHARACTER):
            result = StepTable.nested_key_value_schema.parse(line)
            if result is None:
                raise Exception('Step Error: Unable to parse nested step table')
            else:
                if result.named[StepTable.VALUE_TEXT].strip() == StepTable.EMPTY_TEXT:
                    continue
                elif result.named[StepTable.NESTED_KEY_TEXT].strip() == StepTable.EMPTY_TEXT:
                    table_dict.update({
                        result.named.get(StepTable.KEY_TEXT): result.named.get(StepTable.VALUE_TEXT)
                    })
                else:
                    table_dict.update({
                        result.named.get(StepTable.KEY_TEXT):
                            {result.named.get(StepTable.NESTED_KEY_TEXT): result.named.get(StepTable.VALUE_TEXT)}
                    })
        return table_dict

    @staticmethod
    def parse_step_table_example_value(request, table_dict):
        """Parse step table example value"""
        return {key: StepTable.get_value(request, value) for key, value in table_dict.items()}

    @staticmethod
    def get_value(request, argument):
        """Get fixture value from BDD examples"""
        if argument[0] == StepTable.LESS_THAN_CHARACTER and argument[-1] == StepTable.GREATER_THAN_CHARACTER:
            value = request.getfixturevalue(argument[1:-1])
            return None if value == StepTable.EMPTY_TEXT else value
        return None if argument == StepTable.EMPTY_DOUBLE_QUOTES else argument
