import sys

# Import des composants nécessaires au démarrage de l'application
try:
    # La vue de départ de l'application
    from view.accueil.accueil_vue import AccueilVue
    # Outils pour l'initialisation et la gestion de session
    from utils.reset_database import ResetDatabase
    from utils.session import Session
except ImportError as e:
    print(f"Erreur d'importation au démarrage : {e}")
    print("Vérifiez que vos chemins d'accès (view/ et utils/) sont corrects.")
    sys.exit(1)


def main():
    """
    Fonction principale de l'application en ligne de commande (CLI).
    Elle gère le cycle de vie de l'application et la transition entre les vues.
    """

    print("--- Démarrage de l'application Striv CLI ---")

    # ===============================================
    # 1. Initialisation de la base de données (Optionnel)
    # Décommenter si vous souhaitez réinitialiser la BDD à chaque lancement
    #try:
    #    ResetDatabase().lancer()
    #    print("Base de données réinitialisée avec succès.")
    #except Exception as e:
    # Ceci est courant si la BDD n'est pas encore configurée ou si le reset_database n'existe pas encore
    #     print(f"Attention: Impossible de réinitialiser la base de données. Continuer sans reset: {e}")
    # ===============================================

    # 2. Initialisation et nettoyage de la session utilisateur
    Session().reset()

    # 3. Démarrage de la boucle principale avec la Vue d'Accueil
    current_view = AccueilVue("Bienvenue sur Striv. Veuillez vous connecter ou vous inscrire.")

    # Boucle principale : l'application tourne tant que 'current_view' n'est pas None (l'utilisateur a choisi 'Quitter')
    while current_view:

        try:
            # La vue actuelle demande le choix de l'utilisateur et retourne la vue suivante
            next_view = current_view.choisir_menu()

            # Mise à jour de la vue actuelle pour la prochaine itération
            current_view = next_view

        except EOFError:
            # Gestion de Ctrl+D ou si l'utilisateur annule InquirerPy (force la sortie)
            print("\nOpération annulée par l'utilisateur (EOF).")
            break
        except KeyboardInterrupt:
            # Gestion de Ctrl+C (force la sortie)
            print("\nApplication interrompue par l'utilisateur (Ctrl+C).")
            break
        except Exception as e:
            # Gestion des erreurs inattendues non gérées dans les vues
            print("\n--- ERREUR CRITIQUE ---")
            print(f"Une erreur inattendue s'est produite : {e}")
            break

    # 4. Fin de l'application
    print("\n--- Fin de l'application Striv. Au revoir ! ---")


if __name__ == "__main__":
    main()
