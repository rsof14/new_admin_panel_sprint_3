import os
import datetime
from contextlib import contextmanager, closing
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor, execute_values
from psycopg2 import DatabaseError, OperationalError, ProgrammingError, DataError
import uuid
from etl.movies_admin.config import settings
from query import PG_EXACT_QUERY
from backoff import backoff


class PostgresExtractor:

    def __init__(self):
        self.connection = None
        self.cursor = None

    @backoff(exceptions=(OperationalError,))
    def connect_to_pgdb(self):
        dsl = {'dbname': os.environ.get('DB_NAME'), 'user': os.environ.get('DB_USER'),
               'password': os.environ.get('DB_PASSWORD'), 'host': os.environ.get('DB_HOST'),
               'port': os.environ.get('DB_PORT')}
        self.connection = psycopg2.connect(**dsl, cursor_factory=DictCursor)
        self.cursor = self.connection.cursor()

    @backoff(exceptions=(DataError, DatabaseError, ProgrammingError))
    def extract_filmworks(self, since):
        rows_amount = 50
        query = PG_EXACT_QUERY
        self.cursor.execute(query, (since, since, since))
        while True:
            rows = self.cursor.fetchmany(rows_amount)
            if rows:
                # for row in rows:
                #     yield dict(row)
                yield rows
            else:
                break

if __name__ == '__main__':
    pg = PostgresExtractor()
    pg.connect_to_pgdb()
    for i in pg.extract_filmworks(datetime.datetime(2009, 10, 5, 18, 00)):
        print(i)

