import os
import dotenv

import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from utils.singleton import Singleton
from dao.db_connection import DBConnection

class ResetDatabase(metaclass=Singleton):
    """
    Réinitialisation de la base de données
    """

    def lancer(self):
        print("Ré-initialisation de la base de données")
        pop_data_path = "data/pop_db.sql"

        dotenv.load_dotenv()

        schema = os.environ["POSTGRES_SCHEMA"]

        create_schema = f"DROP SCHEMA IF EXISTS {schema} CASCADE; CREATE SCHEMA {schema};"

        init_db = open("data/init_db.sql", encoding="utf-8")
        init_db_as_string = init_db.read()
        init_db.close()

        pop_db = open(pop_data_path, encoding="utf-8")
        pop_db_as_string = pop_db.read()
        pop_db.close()


        # Chargement des fichiers

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    print("📝 Création du schema")
                    cursor.execute(create_schema)
                    print("📝 Exécution de init_db.sql...")
                    cursor.execute(init_db_as_string)
                    # print("📝 Exécution de pop_db.sql...")
                    # cursor.execute(pop_db_as_string)

                connection.commit()
                print("✅ Base de données réinitialisée avec succès!")

        except Exception as e:
            print(f"❌ Erreur lors de la réinitialisation: {e}")
            raise

        print("Ré-initialisation de la base de données - Terminée")
        return True


if __name__ == "__main__":
    ResetDatabase().lancer()
