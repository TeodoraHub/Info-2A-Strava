from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from view.session import Session

from service.utilisateur_service import UtilisateurService


class ConnexionVue(VueAbstraite):
    """Vue de Connexion (saisie de nom et mdp)"""

    def choisir_menu(self):
        # Demande à l'utilisateur de saisir nom et mot de passe
        nom = inquirer.text(message="Entrez votre nom : ").execute()
        mdp = inquirer.secret(message="Entrez votre mot de passe :").execute()

        # Appel du service pour trouver l'utilisateur
        utilisateur = UtilisateurService().se_connecter(nom, mdp)

        # Si l'utilisateur a été trouvé à partir des ses identifiants de connexion
        if utilisateur:
            message = f"Vous êtes connecté sous le nom {utilisateur.nom}"
            Session().connexion(utilisateur)

            from view.menu_utilisateur_vue import MenuJoueurVue

            return MenuJoueurVue(message)

        message = "Erreur de connexion (nom ou mot de passe invalide)"
        from view.accueil.accueil_vue import AccueilVue

        return AccueilVue(message)
