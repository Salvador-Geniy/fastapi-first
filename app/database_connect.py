""" This module for connecting to database with QSL-queries in code, without ORM"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor

from dotenv import load_dotenv

load_dotenv()


class ConnectData:
    db_host: str = os.getenv('DB_HOST')
    db_name: str = os.getenv('DB_NAME')
    db_port: str = os.getenv('DB_PORT')
    db_user: str = os.getenv('DB_USER')
    db_pass: str = os.getenv('DB_PASS')


def connect_to_database():
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(host=ConnectData.db_host,
                                database=ConnectData.db_name,
                                user=ConnectData.db_user,
                                password=ConnectData.db_pass,
                                port=ConnectData.db_port,
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was successful!')
    except Exception as error:
        print('Connection to database failed!', error)

    return cursor, conn
