import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from joblib import dump, load
import os

class MLAnomalyDetector:
    def __init__(self, model_path='ml_models'):
        self.model_path = os.path.join(model_path, 'iforest.joblib')
        self.scaler = StandardScaler()
        os.makedirs(model_path, exist_ok=True)
        self.model = self._load_or_init_model()

    def _load_or_init_model(self):
        if os.path.exists(self.model_path):
            return load(self.model_path)
        return IsolationForest(n_estimators=100, contamination=0.01)

    def extract_features(self, logs):
        """从日志中提取特征矩阵"""
        features = []
        for log in logs:
            features.append([
                len(log['request']),                # 请求长度
                len(log.get('url_path', '')),       # URL路径长度
                len(log.get('url_query', {})),      # 查询参数数量
                int(log['status']) // 100,         # 状态码首位
                log['body_bytes_sent'] / 1024      # 响应大小(KB)
            ])
        return self.scaler.fit_transform(features)

    def train(self, normal_logs):
        """训练模型"""
        X = self.extract_features(normal_logs)
        self.model.fit(X)
        dump(self.model, self.model_path)

    def predict(self, logs):
        """检测异常日志"""
        X = self.extract_features(logs)
        preds = self.model.predict(X)
        return [log for log, pred in zip(logs, preds) if pred == -1]