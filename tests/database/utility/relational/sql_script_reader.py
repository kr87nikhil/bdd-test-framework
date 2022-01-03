from os.path import join
from pathlib import Path

class SqlScriptReader:
    """SQL file related service"""

    def __init__(self, file_name = 'initialize_mysql.sql'):
        """Read sql file from resources folder"""
        base_path = Path(__file__).parent.parent
        with open(join(base_path, 'resources', file_name)) as sql_file:
            self.sql_queries = sql_file.read().split(';')[:4]
    
    def __iter__(self):
        """Iterator object and is implicitly called at the start of loops"""
        return self

    def __next__(self):
        """Execute SQL scripts sequentially"""
        for script in self.sql_queries:
            return script.strip()
        raise StopIteration
