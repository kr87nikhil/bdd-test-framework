from os.path import join
from pathlib import Path

class SqlScriptReader:
    """SQL file related service"""

    def __init__(self, file_name = 'initialize_mysql.sql'):
        """Read sql file from resources folder"""
        self.index = -1
        base_path = Path(__file__).parent.parent
        with open(join(base_path, 'resources', file_name)) as sql_file:
            self.sql_queries = sql_file.read().split(';')[:4]
    
    def __iter__(self):
        """Iterator object and is implicitly called at the start of loops"""
        return self

    def __next__(self):
        """Get next SQL script"""
        self.index += 1
        if self.index == len(self.sql_queries):
            raise StopIteration
        else:
            return self.sql_queries[self.index].strip() + ';'
