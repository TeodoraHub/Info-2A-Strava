import os

import dotenv
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

from utils.singleton import Singleton

load_dotenv(dotenv_path="P:/Projet info 2A/Info-2A-Strava/.env")


class DBConnection(metaclass=Singleton):
    """
    Technical class to open only one connection to the DB.
    """

    def __init__(self):
        dotenv.load_dotenv(override=True)
        # Open the connection.
        self.__connection = psycopg2.connect(
            host=os.environ["POSTGRES_HOST"],
            port=os.environ["POSTGRES_PORT"],
            database=os.environ["POSTGRES_DATABASE"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            cursor_factory=RealDictCursor,
        )

    @property
    def connection(self):
        """
        return the opened connection.

        :return: the opened connection.
        """
        return self.__connection        """
        return self.__connection