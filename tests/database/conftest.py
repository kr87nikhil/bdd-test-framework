def pytest_addoption(parser):
    """Define pytest command line parameters"""
    parser.addoption("--relational_db", action="store", default='MySQL', help='Target database')
