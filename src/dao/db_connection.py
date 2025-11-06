import os
from pathlib import Path
import dotenv
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from utils.singleton import Singleton

# Charger le .env depuis la racine du projet
dotenv_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=dotenv_path, override=True)

# load_dotenv(dotenv_path="P:/Projet info 2A/Info-2A-Strava/.env")


class DBConnection(metaclass=Singleton):
    """
    Connexion unique à la base de données PostgreSQL
    """

    def __init__(self):
        dotenv.load_dotenv(override=True)
        # Récupérer le schéma
        schema = os.environ.get("POSTGRES_SCHEMA", "public")
        # Connexion avec options pour définir le search_path
        self.__connection = psycopg2.connect(
            host=os.environ["POSTGRES_HOST"],
            port=os.environ["POSTGRES_PORT"],
            database=os.environ["POSTGRES_DATABASE"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            cursor_factory=RealDictCursor,
            options=f"-c search_path={schema}"
        )

        # Create SQLAlchemy engine for ORM operations
        db_url = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DATABASE']}"
        self.__engine = create_engine(db_url)

        # Create a scoped session factory
        session_factory = sessionmaker(bind=self.__engine)
        self.__Session = scoped_session(session_factory)

    @property
    def connection(self):
        """
        return the opened connection.

        :return: the opened connection.
        """
        return self.__connection

    @property
    def engine(self):
        """
        return the SQLAlchemy engine.

        :return: the SQLAlchemy engine.
        """
        return self.__engine

    @property
    def session(self):
        """
        return a SQLAlchemy session.

        :return: the SQLAlchemy session.
        """
        return self.__Session()

    def close_session(self):
        """ Ferme la session SQLAlchemy """

        self.__Session.remove()

    def __del__(self):
        """Nettoyage à la destruction de l'objet"""
        if hasattr(self, '_DBConnection__connection'):
            self.__connection.close()
        if hasattr(self, '_DBConnection__Session'):
            self.__Session.remove()
