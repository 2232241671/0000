from app.extensions import db

class LogSource(db.Model):
    """日志源配置"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    type = db.Column(db.String(20), nullable=False)  # nginx, apache, iis
    path = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class RawLog(db.Model):
    """原始日志存储（仅用于小规模测试）"""
    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.Integer, db.ForeignKey('log_source.id'))
    raw_text = db.Column(db.Text, nullable=False)
    parsed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

#
class LogEntry(db.Model):
    __tablename__ = 'log_entries'

    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(45), nullable=False, index=True)
    request_url = db.Column(db.Text, nullable=False)
    status_code = db.Column(db.Integer, nullable=False)
    user_agent = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, nullable=False, index=True)
    is_processed = db.Column(db.Boolean, default=False)

    __table_args__ = (
        db.Index('idx_ip_timestamp', 'ip', 'timestamp'),
    )


class LogAnalysisResult(db.Model):
    __tablename__ = 'log_analysis_results'

    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(45), nullable=False, index=True)
    request_url = db.Column(db.Text, nullable=False)
    status_code = db.Column(db.Integer)
    anomaly_score = db.Column(db.Float)
    detection_method = db.Column(db.String(20))  # 'rule' or 'ml'
    timestamp = db.Column(db.DateTime, nullable=False, index=True)
    details = db.Column(db.JSON)

    __table_args__ = (
        db.Index('idx_method_timestamp', 'detection_method', 'timestamp'),
    )

from elasticsearch_dsl import Document, Date, Keyword, Text, Integer
from elasticsearch_dsl import connections
def get_es():
    return connections.get_connection()
class WebLog(Document):
    timestamp = Date()
    remote_addr = Keyword()
    request = Text(fields={'keyword': Keyword()})
    status = Integer()
    body_bytes_sent = Integer()
    http_referer = Text()
    http_user_agent = Text()

    class Index:
        name = 'web_logs'

    @classmethod
    def init_index(cls):
        """初始化索引"""
        if not cls._index.exists():
            cls.init()