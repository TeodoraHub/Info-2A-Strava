import os

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

        # Dossier courant = dossier du script utils/
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Aller dans ../data (si data est à la racine du projet)
        data_dir = os.path.join(base_dir, "..", "..", "data")

        init_db_path = os.path.join(data_dir, "init_db.sql")
        pop_db_path = os.path.join(data_dir, "pop_db.sql")

        # Chargement des fichiers
        with open(init_db_path, encoding="utf-8") as init_db:
            init_db_as_string = init_db.read()

        with open(pop_db_path, encoding="utf-8") as pop_db:
            pop_db_as_string = pop_db.read()

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    print("📝 Exécution de init_db.sql...")
                    cursor.execute(init_db_as_string)

                    print("📝 Exécution de pop_db.sql...")
                    cursor.execute(pop_db_as_string)

                connection.commit()
                print("✅ Base de données réinitialisée avec succès!")   

        except Exception as e:
            print(f"❌ Erreur lors de la réinitialisation: {e}")
            raise

        print("Ré-initialisation de la base de données - Terminée")
        return True


if __name__ == "__main__":
    ResetDatabase().lancer()
