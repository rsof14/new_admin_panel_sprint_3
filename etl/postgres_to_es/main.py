import datetime

from pgdb_exactor import PostgresExtractor
from pgdb_transformer import ElasticTransformer
from elastic_loader import ElasticLoader
from state import State, JsonFileStorage


class MainETL:
    def __init__(self):
        self.state = State(JsonFileStorage('fixme'))
        self.extractor = PostgresExtractor()
        self.transformer = ElasticTransformer()
        self.data_loader = ElasticLoader()

    def load_data(self):
        last_modified = datetime.datetime.min
        for rows in self.extractor.extract_filmworks(last_modified):
            transformed_data = self.transformer.transform_data(rows)


{'id': 'ffc3df9f-a17e-4bae-b0b6-c9c4da290fdd', 'title': 'MegaMan Star Force', 'description': '', 'rating': 7.1,
 'type': 'movie', 'created': datetime.datetime(2021, 6, 16, 20, 14, 9, 259084, tzinfo=datetime.timezone.utc),
 'modified': datetime.datetime(2021, 6, 16, 20, 14, 9, 259100, tzinfo=datetime.timezone.utc), 'persons': [
    {'person_id': 'b7aa38da-b725-4eac-8608-c4fe7636060b', 'person_name': 'Michael P. Greco', 'person_role': 'actor'}],
 'genres': ['Animation']}
