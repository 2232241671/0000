# from datetime import datetime
# from collections import defaultdict
#
#
# class RuleEngine:
#     def __init__(self):
#         self.rules = [
#             self._detect_sqli,
#             self._detect_xss,
#             self._detect_brute_force,
#             self._detect_scanner
#         ]
#
#     def analyze(self, logs):
#         """执行规则分析"""
#         results = []
#
#         # 实时规则检测
#         for log in logs:
#             for rule in self.rules:
#                 result = rule(log)
#                 if result:
#                     results.append(result)
#
#         # 聚合分析
#         results.extend(self._aggregate_analysis(logs))
#
#         return results
#
#     def _detect_sqli(self, log):
#         """SQL注入检测"""
#         sql_keywords = ['union', 'select', 'insert', 'drop', '--', '/*']
#         request = log.get('request', '').lower()
#
#         if any(kw in request for kw in sql_keywords):
#             return {
#                 'type': 'sqli',
#                 'level': 'high',
#                 'message': f"Possible SQLi detected: {log['request'][:50]}...",
#                 'log_id': log.get('id')
#             }
#         return None
#
#     def _detect_xss(self, log):
#         """XSS攻击检测"""
#         xss_patterns = ['<script>', 'javascript:', 'onerror=']
#         request = log.get('request', '').lower()
#
#         if any(p in request for p in xss_patterns):
#             return {
#                 'type': 'xss',
#                 'level': 'high',
#                 'message': f"Possible XSS detected: {log['request'][:50]}...",
#                 'log_id': log.get('id')
#             }
#         return None
#
#     def _aggregate_analysis(self, logs):
#         """聚合分析（基于时间窗口）"""
#         # 示例：检测高频访问
#         ip_counts = defaultdict(int)
#         for log in logs:
#             ip_counts[log['remote_addr']] += 1
#
#         return [{
#             'type': 'high_frequency',
#             'level': 'medium',
#             'message': f"IP {ip} made {count} requests in short time",
#             'ips': list(ips)
#         } for ip, count in ip_counts.items() if count > 100]


from datetime import datetime
from collections import defaultdict


class RuleEngine:
    def __init__(self):
        self.rules = [
            self.detect_sqli,
            self.detect_xss,
            self.detect_brute_force,
            self.detect_scanner
        ]

    def analyze(self, logs):
        """执行规则分析"""
        results = []

        # 实时规则检测
        for log in logs:
            for rule in self.rules:
                result = rule(log)
                if result:
                    results.append(result)

        # 聚合分析
        results.extend(self.aggregate_analysis(logs))

        return results

    def detect_sqli(self, log):
        """SQL注入检测"""
        sql_keywords = ['union', 'select', 'insert', 'drop', '--', '/*']
        request = log.get('request', '').lower()

        if any(kw in request for kw in sql_keywords):
            return {
                'type': 'sqli',
                'level': 'high',
                'message': f"Possible SQLi detected: {log['request'][:50]}...",
                'log_id': log.get('id')
            }
        return None

    def detect_xss(self, log):
        """XSS攻击检测"""
        xss_patterns = ['<script>', 'javascript:', 'onerror=']
        request = log.get('request', '').lower()

        if any(p in request for p in xss_patterns):
            return {
                'type': 'xss',
                'level': 'high',
                'message': f"Possible XSS detected: {log['request'][:50]}...",
                'log_id': log.get('id')
            }
        return None

    def detect_brute_force(self, log):
        """暴力破解检测"""
        # 这里可以是基于单条日志的暴力破解检测逻辑
        # 更复杂的实现应该在 aggregate_analysis 中
        return None

    def detect_scanner(self, log):
        """扫描器检测"""
        scanner_patterns = ['nmap', 'acunetix', 'nikto']
        ua = log.get('http_user_agent', '').lower()

        if any(p in ua for p in scanner_patterns):
            return {
                'type': 'scanner',
                'level': 'medium',
                'message': f"Possible scanner detected: {ua[:50]}...",
                'log_id': log.get('id')
            }
        return None

    def aggregate_analysis(self, logs):
        """聚合分析（基于时间窗口）"""
        results = []

        # 1. 检测高频访问
        ip_counts = defaultdict(int)
        for log in logs:
            ip_counts[log['remote_addr']] += 1

        for ip, count in ip_counts.items():
            if count > 100:  # 阈值设为100
                results.append({
                    'type': 'high_frequency',
                    'level': 'medium',
                    'message': f"IP {ip} made {count} requests in short time",
                    'ip': ip,
                    'count': count
                })

        return results