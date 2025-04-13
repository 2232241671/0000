# import os
# import time
# from pathlib import Path
# from loguru import logger
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
#
#
# class LogFileHandler(FileSystemEventHandler):
#     def __init__(self, callback):
#         self.callback = callback
#
#     def on_modified(self, event):
#         if not event.is_directory:
#             self.callback(event.src_path)
#
#
# class LogCollector:
#     def __init__(self, log_dir, parser):
#         self.log_dir = Path(log_dir)
#         self.parser = parser
#         self.observer = Observer()
#         self.file_positions = {}
#
#     def start(self):
#         """启动日志收集"""
#         if not self.log_dir.exists():
#             self.log_dir.mkdir(parents=True)
#
#         event_handler = LogFileHandler(self.process_log)
#         self.observer.schedule(event_handler, self.log_dir, recursive=True)
#         self.observer.start()
#
#         try:
#             while True:
#                 time.sleep(1)
#         except KeyboardInterrupt:
#             self.observer.stop()
#         self.observer.join()
#
#     def process_log(self, file_path):
#         """处理日志文件变化"""
#         current_position = self.file_positions.get(file_path, 0)
#
#         try:
#             with open(file_path, 'r') as f:
#                 f.seek(current_position)
#                 for line in f:
#                     parsed = self.parser.parse(line.strip())
#                     if parsed:
#                         self.store_log(parsed)
#                 self.file_positions[file_path] = f.tell()
#         except Exception as e:
#             logger.error(f"Error processing {file_path}: {str(e)}")
#
#     def store_log(self, log_data):
#         """存储日志数据"""
#         # 先简单打印，后续替换为实际存储
#         logger.info(f"New log: {log_data}")

import os
import time
from pathlib import Path
from loguru import logger
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class LogFileHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback

    def on_modified(self, event):
        if not event.is_directory and not event.src_path.endswith('~'):
            self.callback(event.src_path)


class LogCollector:
    def __init__(self, log_dir, parser_class):
        self.log_dir = Path(log_dir)
        self.parser = parser_class()  # 实例化解析器
        self.observer = Observer()
        self.file_positions = {}

    def start(self):
        """启动日志收集"""
        print(f"[日志收集器] 开始监控目录: {self.log_dir}")
        print(f"[日志收集器] 当前工作目录: {os.getcwd()}")
        if not self.log_dir.exists():
            self.log_dir.mkdir(parents=True)

        event_handler = LogFileHandler(self.process_log)
        self.observer.schedule(event_handler, self.log_dir, recursive=True)
        self.observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

    # def process_log(self, file_path):
    #     """处理日志文件变化"""
    #     if file_path.endswith('~'):  # 忽略临时文件
    #         return
    #
    #     current_position = self.file_positions.get(file_path, 0)
    #
    #     try:
    #         with open(file_path, 'r', encoding='utf-8') as f:
    #             f.seek(current_position)
    #             for line in f:
    #                 line = line.strip()
    #                 if line:  # 忽略空行
    #                     parsed = self.parser.parse(line)  # 使用实例方法
    #                     if parsed:
    #                         self.store_log(parsed)
    #             self.file_positions[file_path] = f.tell()
    #     except Exception as e:
    #         logger.error(f"Error processing {file_path}: {str(e)}")


    #日志批量处理
    def process_log(self, file_path):
        BATCH_SIZE = 100  # 每100条处理一次
        buffer = []

        with open(file_path) as f:
            for line in f:
                parsed = self.parser.parse(line)
                if parsed:
                    buffer.append(parsed)
                    if len(buffer) >= BATCH_SIZE:
                        async_analyze_logs.delay(buffer.copy())
                        buffer.clear()


    def store_log(self, log_data):
        """存储日志数据"""
        logger.info(f"New log: {log_data}")
        # 这里可以添加存储到Elasticsearch的逻辑
        # 例如：
        # from app.models import WebLog
        # WebLog(**log_data).save()