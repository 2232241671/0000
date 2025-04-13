# from flask_caching import Cache
# from flask_sqlalchemy import SQLAlchemy
# from celery import Celery
# from elasticsearch_dsl import connections
#
# # 初始化各扩展
# db = SQLAlchemy()
# cache = Cache()  # 新增缓存支持
# celery = Celery(__name__, broker='redis://localhost:6379/0')
# es = connections.create_connection(hosts=['http://localhost:9200'])
#
# def init_extensions(app):
#     """初始化所有扩展"""
#     db.init_app(app)
#     cache.init_app(app, config={'CACHE_TYPE': 'SimpleCache'})  # 简单内存缓存
#     celery.conf.update(app.config)

from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from celery import Celery
from elasticsearch_dsl import connections
import os

# 初始化基础扩展
db = SQLAlchemy()
cache = Cache()
celery = Celery(__name__)

# 弹性初始化Elasticsearch
try:
    es = connections.create_connection(
        hosts=os.getenv('ES_HOSTS', ['http://localhost:9200']),
        timeout=20
    )
except Exception:
    es = None  # 开发时允许ES不可用
    print("⚠️ Elasticsearch连接失败，部分功能受限")


def init_extensions(app):
    """按需初始化扩展"""
    # 必须初始化的组件
    db.init_app(app)
    cache.init_app(app)

    # 条件初始化
    if app.config.get('USE_CELERY'):
        celery.conf.update(app.config)

    # 开发时模拟组件
    if app.debug and os.getenv('USE_MOCK'):
        from .mocks import MockES
        global es
        es = MockES()  # 使用模拟对象