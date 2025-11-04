from view.vue_abstraite import VueAbstraite
from view.session import Session
from service.utilisateur_service import UtilisateurService
from InquirerPy import inquirer

class ProfilUtilisateurVue(VueAbstraite):
    """Vue pour afficher le profil de l'utilisateur connecté."""

    def afficher(self):
        """Affiche les informations du profil de l'utilisateur connecté."""
        utilisateur = Session().utilisateur
        if not utilisateur:
            print("Aucun utilisateur connecté.")
            return

        # Afficher les informations de base
        print("\n" + "=" * 50)
        print(f"Profil de {utilisateur.nom_user}")
        print("=" * 50)
        print(f"ID: {utilisateur.id_user}")
        print(f"Email: {utilisateur.mail_user}")

        # Afficher les activités de l'utilisateur
        if utilisateur.activites:
            print("\nActivités récentes:")
            for activite in utilisateur.activites:
                print(f"- {activite.titre} ({activite.type_activite})")
        else:
            print("\nAucune activité enregistrée.")

        # Afficher les statistiques
        stats = utilisateur.obtenir_statistiques()
        print("\nStatistiques:")
        print(f"- Nombre d'activités: {stats['nombre_activites']}")
        print(f"- Kilomètres parcourus: {stats['kilometres']}")
        print(f"- Heures d'activité: {stats['heures']}")

        # Demander à l'utilisateur ce qu'il veut faire ensuite
        choix = inquirer.select(
            message="Que voulez-vous faire ?",
            choices=[
                "Retourner au menu principal",
                "Se déconnecter",
            ],
        ).execute()

        if choix == "Retourner au menu principal":
            from view.menu_utilisateur_vue import MenuUtilisateurVue
            return MenuUtilisateurVue()
        elif choix == "Se déconnecter":
            Session().deconnexion()
            from view.accueil.accueil_vue import AccueilVue
            return AccueilVue()
