from flask import Blueprint, redirect
from flask_restful import Api
from app.api.log_api import LogSourceAPI

from app.api.log_api import RecentLogsAPI, LogStatsAPI, AlertsAPI

bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(bp)

api.add_resource(LogSourceAPI, '/log-sources')
api.add_resource(RecentLogsAPI, '/logs/recent')
api.add_resource(LogStatsAPI, '/logs/stats')
api.add_resource(AlertsAPI, '/alerts')
# @bp.route('/')
# def home():
#     return """
#     <h1>WEB日志安全分析系统</h1>
#     <ul>
#         <li><a href="/api/alerts">安全告警</a></li>
#         <li><a href="/logs/recent">最近日志</a></li>
#     </ul>
#     """
@bp.route('/')
def index():
    return redirect('/test')  # 重定向到测试页