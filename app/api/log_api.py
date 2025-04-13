#from flask_restful import Resource
# from app.models import LogSource
# from app.extensions import db
# from ..services.analyzer import LogAnalyzer
#
#
# class LogSourceAPI(Resource):
#     def get(self):
#         """获取所有日志源配置"""
#         sources = LogSource.query.all()
#         return {
#             'data': [{
#                 'id': s.id,
#                 'name': s.name,
#                 'type': s.type,
#                 'path': s.path,
#                 'status': s.status
#             } for s in sources]
#         }
#
#     def post(self):
#         """添加新的日志源"""
#         # 实现添加逻辑
#         pass
from flask_restful import Resource
from ..services.log_analyzer import LogAnalyzer
from flask import Blueprint, jsonify, request
from app.extensions import cache
from app.models import LogEntry


bp = Blueprint('log_api', __name__)

@bp.route('/logs')
@cache.cached(timeout=60, query_string=True)  # 缓存60秒
def get_logs():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)

    logs = LogEntry.query.order_by(
        LogEntry.timestamp.desc()
    ).paginate(page=page, per_page=per_page)

    return jsonify({
        'items': [log.to_dict() for log in logs.items],
        'total': logs.total,
        'pages': logs.pages
    })


class LogSourceAPI(Resource):
    def get(self):
        """获取所有日志源配置"""
        sources = LogSource.query.all()
        return {
            'data': [{
                'id': s.id,
                'name': s.name,
                'type': s.type,
                'path': s.path,
                'status': s.status
            } for s in sources]
        }

    def post(self):
        """添加新的日志源"""
        # 实现添加逻辑
        pass
#TIAN JIA

class RecentLogsAPI(Resource):
    def get(self):
        """获取最近日志"""
        search = Search(index='web_logs').sort('-timestamp')[:100]
        results = search.execute()

        return {
            'total': len(results),
            'items': [hit.to_dict() for hit in results]
        }


class LogStatsAPI(Resource):
    def get(self):
        """获取日志统计"""
        from elasticsearch_dsl import A

        # 状态码聚合
        agg = A('terms', field='status', size=10)
        search = WebLog.search().extra(size=0)
        search.aggs.bucket('status_codes', agg)

        response = search.execute()
        return {
            'status_codes': {bucket.key: bucket.doc_count
                             for bucket in response.aggregations.status_codes.buckets}
        }


class AlertsAPI(Resource):
    def get(self):
        """获取安全告警"""
        # 这里可以从数据库或ES获取存储的告警
        return [
            {'type': 'sqli', 'message': 'Possible SQLi detected', 'level': 'high'},
            {'type': 'xss', 'message': 'Possible XSS detected', 'level': 'high'}
        ]