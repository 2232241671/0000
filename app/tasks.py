# from celery import Celery
# from .extensions import celery_app
# from celery import Celery
# from app.extensions import db
# from app.models import LogEntry
# from app.services.ml_analyzer import MLService
# import pandas as pd
# from datetime import datetime, timedelta
#
# celery = Celery(__name__)
# ml_service = MLService()
#
# @celery_app.task
# def async_analyze_logs(logs):
#     from .services import LogAnalyzer
#     return LogAnalyzer().process(logs)
#
#
# @celery.task
# def daily_ml_analysis():
#     """每日机器学习分析任务"""
#     yesterday = datetime.now() - timedelta(days=1)
#     logs = LogEntry.query.filter(
#         LogEntry.timestamp >= yesterday
#     ).all()
#
#     log_data = pd.DataFrame([{
#         'id': log.id,
#         'timestamp': log.timestamp,
#         'ip_address': log.ip_address,
#         'status_code': log.status_code,
#         'response_size': log.response_size,
#         'request_path': log.request_path
#     } for log in logs])
#
#     # 执行异常检测
#     anomalies = ml_service.detect_anomalies(log_data)
#
#     # 执行聚类分析
#     clusters = ml_service.cluster_logs(log_data)
#
#     return {
#         'anomaly_count': len(anomalies),
#         'cluster_info': clusters
#     }

from celery import Celery
from .extensions import celery_app

@celery_app.task
def async_analyze_logs(logs):
    from .services import LogAnalyzer
    return LogAnalyzer().process(logs)