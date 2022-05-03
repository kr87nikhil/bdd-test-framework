from enum import Enum, unique


@unique
class TestRailCaseTypes(Enum):
    AUTOMATED = 3
    FUNCTIONAL = 6
    PERFORMANCE = 8
    REGRESSION = 9
    SMOKE_AND_SANITY = 11
