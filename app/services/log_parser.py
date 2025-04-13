# import re
# from datetime import datetime
# class LogParser:
#     @staticmethod
#     def parse_nginx(log_line):
#         """解析Nginx日志格式"""
#         pattern = (
#             r'(?P<remote_addr>\S+)\s-\s(?P<remote_user>\S+)\s+\[(?P<time_local>.*?)\]\s+'
#             r'"(?P<request>.*?)"\s+(?P<status>\d+)\s+(?P<body_bytes_sent>\d+)\s+'
#             r'"(?P<http_referer>.*?)"\s+"(?P<http_user_agent>.*?)"'
#         )
#         match = re.match(pattern, log_line)
#         if not match:
#             return None
#         log_data = match.groupdict()
#         # 转换时间格式
#         try:
#             log_data['timestamp'] = datetime.strptime(
#                 log_data['time_local'], '%d/%b/%Y:%H:%M:%S %z'
#             ).isoformat()
#         except:
#             log_data['timestamp'] = datetime.now().isoformat()
#
#         return log_data
#     @classmethod
#     def parse(cls, log_line):
#         """自动识别并解析日志"""
#         # 这里可以添加其他日志格式的识别
#         return cls.parse_nginx(log_line)


import re
from datetime import datetime
from urllib.parse import urlparse, parse_qs


class LogParser:
    def parse(self, log_line):
        """主解析方法"""
        return self.parse_nginx(log_line)

    @staticmethod
    def parse_nginx(log_line):
        """解析Nginx日志格式"""
        pattern = (
            r'(?P<remote_addr>\S+)\s-\s(?P<remote_user>\S+)\s+\[(?P<time_local>.*?)\]\s+'
            r'"(?P<request>.*?)"\s+(?P<status>\d+)\s+(?P<body_bytes_sent>\d+)\s+'
            r'"(?P<http_referer>.*?)"\s+"(?P<http_user_agent>.*?)"'
        )
        match = re.match(pattern, log_line)
        if not match:
            return None

        log_data = match.groupdict()

        # 转换时间格式
        try:
            log_data['timestamp'] = datetime.strptime(
                log_data['time_local'],
                '%d/%b/%Y:%H:%M:%S %z'
            ).isoformat()
        except:
            log_data['timestamp'] = datetime.now().isoformat()

        # URL解析
        try:
            request_parts = log_data['request'].split()
            if len(request_parts) > 1:
                url_info = urlparse(request_parts[1])
                log_data['url_path'] = url_info.path
                log_data['url_query'] = parse_qs(url_info.query)
        except:
            log_data['url_path'] = None
            log_data['url_query'] = None

        return log_data