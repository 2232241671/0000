from .rule_engine import RuleEngine
from .log_cleaner import LogCleaner
from .ml_analyzer import MLAnomalyDetector

# class LogAnalyzer:
#     def __init__(self):
#         self.cleaner = LogCleaner()
#         self.rule_engine = RuleEngine()
#
#     def process(self, raw_logs):
#         """处理日志流水线"""
#         # 1. 清洗日志
#         cleaned_logs = []
#         for log in raw_logs:
#             cleaned = self.cleaner.clean(log)
#             if cleaned:
#                 cleaned_logs.append(cleaned)
#
#         # 2. 执行分析
#         analysis_results = self.rule_engine.analyze(cleaned_logs)
#
#         return {
#             'logs': cleaned_logs,
#             'alerts': analysis_results
#
#         }

class LogAnalyzer:
    def __init__(self):
        self.ml_detector = MLAnomalyDetector()
        self.cleaner = LogCleaner()
        self.rule_engine = RuleEngine()

    def process(self, raw_logs):
        """处理日志流水线"""
        # 1. 清洗日志
        cleaned_logs = []
        for log in raw_logs:
            cleaned = self.cleaner.clean(log)
            if cleaned:
                cleaned_logs.append(cleaned)

        # 2. 执行分析
        #analysis_results = self.rule_engine.analyze(cleaned_logs)
        ml_anomalies = self.ml_detector.predict(cleaned_logs)
        for anomaly in ml_anomalies:
            results['alerts'].append({
                'type': 'ml_anomaly',
                'level': 'high',
                'message': f"ML检测到异常行为: {anomaly['request'][:50]}..."
            })
        return results

        # return {
        #     'logs': cleaned_logs,
        #     'alerts': analysis_results
        #
        # }
