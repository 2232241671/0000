# import threading
# from app import create_app
# from app.services.log_collector import LogCollector
# from app.services.log_parser import LogParser
# from app.services.log_analyzer import LogAnalyzer
# app = create_app()
#
# def start_collector():
#     from app.services import LogParser, LogAnalyzer
#     from app.models import WebLog
#
#     parser = LogParser()
#     analyzer = LogAnalyzer()
#
#     def process_logs(log_lines):
#         # 解析日志
#         parsed_logs = []
#         for line in log_lines:
#             parsed = parser.parse_common(line)
#             if parsed:
#                 parsed_logs.append(parsed)
#
#         # 分析日志
#         result = analyzer.process(parsed_logs)
#
#         # 存储到ES
#         for log in result['logs']:
#             WebLog(**log).save()
#
#         # 处理告警（可发送邮件或存储）
#         for alert in result['alerts']:
#             print(f"[ALERT] {alert['message']}")
#
#     collector = LogCollector(app.config['LOG_DIR'], process_logs)
#     collector.start()
#
#
# if __name__ == '__main__':
#     # 在单独线程中启动日志收集器
#     collector_thread = threading.Thread(target=start_collector)
#     collector_thread.daemon = True
#     collector_thread.start()
#
#     # 启动Flask应用
#     app.run(host='0.0.0.0', port=5000, debug=True)


import threading
from app import create_app
from app.services.log_collector import LogCollector
from app.services.log_parser import LogParser
from app.services.log_analyzer import LogAnalyzer
from app.models import WebLog
#下面为测试
import sys
import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
print("="*50)
print("系统启动调试信息")
print("="*50)
#上面为测试
app = create_app()

def start_collector():
    # 初始化各组件
    parser = LogParser()  # 使用修正后的LogParser类
    analyzer = LogAnalyzer()  # 确保log_analyzer.py也已同步修正

    def process_logs(log_lines):
        """处理日志的完整流水线"""
        # 1. 解析日志
        parsed_logs = []
        for line in log_lines:
            parsed = parser.parse(line)  # 使用实例方法parse()
            if parsed:
                parsed_logs.append(parsed)

        # 2. 分析日志
        result = analyzer.process(parsed_logs)

        # 3. 存储到ES
        for log in result['logs']:
            try:
                WebLog(**log).save()
            except Exception as e:
                print(f"存储日志到ES失败: {str(e)}")

        # 4. 处理告警
        for alert in result['alerts']:
            print(f"[ALERT] {alert['message']}")

    # 启动日志收集器（传入LogParser类和回调函数）
    collector = LogCollector(
        log_dir=app.config['LOG_DIR'],
        parser_class=LogParser  # 关键修改：传入类而非实例
    )
    collector.start()

if __name__ == '__main__':
    # 在单独线程中启动日志收集器
    print("[主线程] 正在启动日志收集线程...")
    collector_thread = threading.Thread(
        target=start_collector,
        daemon=True  # 设置为守护线程
    )
    collector_thread.start()
    print(f"[主线程] 线程状态: {collector_thread.is_alive()}")
    # 启动Flask应用（关闭自动reloader避免线程重复启动）
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False  # 禁用自动重载
    )