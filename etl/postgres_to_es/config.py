import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

POSTGRES_DB = os.environ.get('POSTGRES_DB')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
