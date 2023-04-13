import psycopg2
from psycopg2.extras import DictCursor
from psycopg2 import DatabaseError, OperationalError, ProgrammingError, DataError
from query import PG_EXACT_QUERY
from backoff import backoff
from conf import settings
import config


class PostgresExtractor:

    def __init__(self):
        self.connection = None
        self.cursor = None

    @backoff(exceptions=(OperationalError,))
    def connect_to_pgdb(self):
        dsl = {'dbname': config.DB_NAME, 'user': config.DB_USER,
               'password': config.DB_PASSWORD, 'host': config.DB_HOST,
               'port': config.DB_PORT}
        self.connection = psycopg2.connect(**dsl, cursor_factory=DictCursor)
        self.cursor = self.connection.cursor()

    @backoff(exceptions=(DataError, DatabaseError, ProgrammingError))
    def extract_filmworks(self, since):
        query = PG_EXACT_QUERY
        self.cursor.execute(query, (since, since, since))
        while True:
            rows = self.cursor.fetchmany(settings.ROWS_AMOUNT)
            if rows:
                yield rows
            else:
                break
