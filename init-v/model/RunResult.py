
class RunResult:

    def __init__(self, timestamp: int, config: Configuration, result: MethodResult, statistics: Statistics,
                 analysis: PerformanceResult):
        self.timestamp = timestamp
        self.config = config
        self.result = result
        self.statistics = statistics
        self.analysis = analysis