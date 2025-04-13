import re
from datetime import datetime, timedelta


class LogCleaner:
    @staticmethod
    def clean(log_entry):
        """执行数据清洗"""
        if not log_entry:
            return None

        # 1. 过滤健康检查等无效请求
        if LogCleaner._is_health_check(log_entry):
            return None

        # 2. 标准化字段
        log_entry = LogCleaner._standardize_fields(log_entry)

        # 3. 补充缺失字段
        log_entry = LogCleaner._fill_missing_fields(log_entry)

        return log_entry

    @staticmethod
    def _is_health_check(log_entry):
        """判断是否是健康检查请求"""
        health_paths = ['/health', '/status']
        user_agents = ['kube-probe', 'ELB-HealthChecker']

        path = log_entry.get('url_path', '')
        ua = log_entry.get('http_user_agent', '').lower()

        return (any(hp in path for hp in health_paths) or
                any(hu in ua for hu in user_agents))

    @staticmethod
    def _standardize_fields(log_entry):
        """字段标准化"""
        # IP地址标准化
        if 'remote_addr' in log_entry:
            log_entry['remote_addr'] = log_entry['remote_addr'].split(':')[0]

        # 时间标准化
        if 'time_local' in log_entry:
            try:
                log_entry['timestamp'] = datetime.strptime(
                    log_entry['time_local'],
                    '%d/%b/%Y:%H:%M:%S %z'
                ).isoformat()
            except:
                log_entry['timestamp'] = datetime.now().isoformat()

        return log_entry