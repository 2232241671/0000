from flask_restful import Resource
from ..models import WebLog
from elasticsearch_dsl import A


class AttackMapAPI(Resource):
    def get(self):
        agg = A('terms', field='geoip.country', size=100)
        search = WebLog.search().extra(size=0)
        search.aggs.bucket('attack_countries', agg)
        results = search.execute()

        return {
            'points': [
                {
                    'name': bucket.key,
                    'value': [bucket.key, 0, bucket.doc_count]  # [国家, 经度, 纬度, 数量]
                }
                for bucket in results.aggregations.attack_countries.buckets
            ]
        }