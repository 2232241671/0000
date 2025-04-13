import os
from pathlib import Path


class Config:
    # 基础配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-123')
    LOG_DIR = Path('logs').absolute()

    # 数据库配置 (SQLite)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(Path(__file__).parent / 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 缓存配置 (内存缓存)
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300  # 5分钟

    # Elasticsearch (本地单节点)
    ELASTICSEARCH_HOSTS = ['http://localhost:9200']
    ELASTICSEARCH_SETTINGS = {
        'refresh_interval': '60s',  # 降低写入压力
        'number_of_replicas': 0  # 单节点无需副本
    }

    # Celery配置 (本地Redis)
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'

    # 功能开关 (按需启用)
    ENABLE_ML = True  # 机器学习分析
    USE_CELERY = False  # 开发时可先关闭Celery


class DevelopmentConfig(Config):
    DEBUG = True
    ELASTICSEARCH_SETTINGS = {
        'refresh_interval': '30s',
        'number_of_shards': 1  # 开发环境减少分片
    }


class ProductionConfig(Config):
    USE_CELERY = True