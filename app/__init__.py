# from flask import Flask
# from .config import Config
# from .extensions import db, init_es  # 修改这里，导入init_es而不是es
#
# def create_app(config_class=Config):
#
#     app = Flask(__name__)
#     app.config.from_object(config_class)
#
#     # 初始化扩展
#     db.init_app(app)
#     init_es(app)  # 初始化Elasticsearch
#
#     # 添加测试路由（必须在app创建后）
#     # @app.route('/test')
#     # def test():
#     #     import threading
#     #     return {
#     #         "status": "running",
#     #         "threads": [t.name for t in threading.enumerate()],
#     #         "log_dir": app.config['LOG_DIR']
#     #     }
#     @app.route('/test')
#     def test():
#         from flask import jsonify  # 或者在这里单独导入
#         import threading
#         return jsonify({
#             "status": "running",
#             "components": {
#                 "flask": True,
#                 "log_collector": threading.current_thread().name == "LogCollector",
#                 "elasticsearch": "http://localhost:9200"
#             }
#         })
#
#
#
#
#
#
#     # 注册蓝图
#     from app.routes import bp
#     app.register_blueprint(bp)
#
# #     # 创建数据库表
# #     with app.app_context():
# #         db.create_all()
# #
# #     return app
# #
# #
# # # 1. 创建Flask实例
# # # 2. 加载配置
# # 3. 初始化扩展
# # 4. 添加路由
# # 5. 注册蓝图
# # 6. 返回app实例

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.extensions import db, cache, celery
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 初始化扩展
    db.init_app(app)
    cache.init_app(app)
    celery.conf.update(app.config)

    # 注册蓝图
    from app.api.log_api import bp as log_bp
    from app.api.visualization import bp as vis_bp
    app.register_blueprint(log_bp, url_prefix='/api/logs')
    app.register_blueprint(vis_bp, url_prefix='/api/vis')

    # 创建数据库表
    with app.app_context():
        db.create_all()

    return app