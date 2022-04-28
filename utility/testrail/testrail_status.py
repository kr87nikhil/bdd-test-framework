from enum import Enum, unique


@unique
class TestRailStatus(int, Enum):
    Blocked = 2
    Failed = 5
    Passed = 1
    Retest = 4
