from Configuration import Configuration
from MethodResult import MethodResult
from Statistics import Statistics
from PerformanceResult import PerformanceResult


class RunResult:

    def __init__(self, timestamp: int, config: Configuration, result: MethodResult, statistics: Statistics,
                 analysis: PerformanceResult):
        self.timestamp = timestamp
        self.config = config
        self.result = result
        self.statistics = statistics
        self.analysis = analysis
