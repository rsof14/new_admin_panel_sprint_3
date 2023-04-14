import datetime
import time
from pgdb_exactor import PostgresExtractor
from pgdb_transformer import ElasticTransformer
from elastic_loader import ElasticLoader
from state import State, JsonFileStorage
from conf import settings


class MainETL:
    def __init__(self):
        self.state = State(JsonFileStorage(settings.PATH_JSON))
        self.extractor = PostgresExtractor()
        self.transformer = ElasticTransformer()
        self.data_loader = ElasticLoader()
        self.data_loader.connect_elastic()

    def load_data(self):
        self.data_loader.load_index()
        self.extractor.connect_to_pgdb()
        modified = self.state.get_state('modified')
        last_modified = modified if modified is not None else datetime.datetime.min
        for rows in self.extractor.extract_filmworks(last_modified):
            self.state.set_state("modified", datetime.datetime.now())
            transformed_data = self.transformer.transform_data(rows)
            self.data_loader.load_data(transformed_data)


if __name__ == '__main__':
    etl = MainETL()
    while True:
        etl.load_data()
        time.sleep(settings.TIME_SLEEP)
