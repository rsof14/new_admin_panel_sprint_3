from elasticsearch import Elasticsearch
from conf import settings
from elastic_index import el_index
from elasticsearch.helpers import bulk, BulkIndexError
from backoff import backoff
from elasticsearch import ConnectionError, TransportError, NotFoundError, ConnectionTimeout, RequestError


class ElasticLoader:
    def __init__(self):
        self.connection = None

    @backoff(exceptions=(ConnectionTimeout, ConnectionError, NotFoundError, TransportError))
    def connect_elastic(self):
        self.connection = Elasticsearch(hosts=f"http://{settings.ES_HOST}:{settings.ES_PORT}")

    @backoff(exceptions=(RequestError,))
    def load_index(self):
        if not self.connection.indices.exists(index="movies"):
            self.connection.indices.create(index="movies", body=el_index.EL_INDEX)

    @backoff(exceptions=(BulkIndexError,))
    def load_data(self, movies_data):
        movies = []
        for movie in movies_data:
            movies.append({"_index": "movies", "_id": movie['id'], "_source": movie})
        bulk(self.connection, movies)
