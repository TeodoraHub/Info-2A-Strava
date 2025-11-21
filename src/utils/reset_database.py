import os
import logging
import dotenv
import sys

# Nécessaire pour les chemins absolus (suppose que vous remontez de src/utils/ à la racine)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
sys.path.append(os.path.join(project_root, "src")) 

from utils.singleton import Singleton
from dao.db_connection import DBConnection
# from service.joueur_service import JoueurService # Commenté car non défini dans l'input

# Définition des chemins absolus
DATA_DIR = os.path.join(project_root, "data")
INIT_DB_PATH = os.path.join(DATA_DIR, "init_db.sql")
POP_DB_PATH = os.path.join(DATA_DIR, "pop_db.sql")
POP_DB_TEST_PATH = os.path.join(DATA_DIR, "pop_db_test.sql")


class ResetDatabase(metaclass=Singleton):
    
    def lancer(self, test_dao=False):
        dotenv.load_dotenv()
        if test_dao:
            schema = "projet_test_dao"
            pop_data_path = POP_DB_TEST_PATH
        else:
            schema = os.environ.get("POSTGRES_SCHEMA", "public")
            pop_data_path = POP_DB_PATH

        create_schema = f"DROP SCHEMA IF EXISTS {schema} CASCADE; CREATE SCHEMA {schema};"

        try:
            with open(INIT_DB_PATH, encoding="utf-8") as init_db:
                init_db_as_string = init_db.read()
            with open(pop_data_path, encoding="utf-8") as pop_db:
                pop_db_as_string = pop_db.read()
        except FileNotFoundError as e:
            logging.error(f"Fichier SQL introuvable: {e}")
            raise

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    print(f"📝 Réinitialisation du schéma : {schema}")
                    cursor.execute(create_schema)
                    # Force le search_path pour toutes les requêtes suivantes
                    cursor.execute(f"SET search_path TO {schema};")
                    cursor.execute(init_db_as_string)
                    cursor.execute(pop_db_as_string)
                    connection.commit()
        except Exception as e:
            logging.error(e)
            raise
        return True




if __name__ == "__main__":
    ResetDatabase().lancer()
