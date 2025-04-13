#供开发使用
class MockES:
    """模拟Elasticsearch的迷你实现"""

    def search(self, *args, **kwargs):
        return {'hits': {'hits': []}}

    def __getattr__(self, name):
        return lambda *args, **kwargs: None