from tabulate import tabulate

from business_object.User_object.utilisateur import Utilisateur
from utils.log_decorator import log
from utils.securite import hash_password


class UtilisateurService:
    """Classe contenant les méthodes de service des Utilisateurs"""

    @log
    def creer(self, id_user, nom_user, mail_user, mdp) -> Utilisateur:
        """Création d'un utilisateur"""

        nouvel_utilisateur = Utilisateur(
            id_user=id_user,
            nom_user=nom_user,
            mail_user=mail_user,
            mdp=hash_password(mdp, nom_user),
        )

        return nouvel_utilisateur if UtilisateurDao().creer(nouvel_utilisateur) else None

    @log
    def trouver_par_id(self, id_user) -> Utilisateur:
        """Trouver un utilisateur à partir de son id"""
        return UtilisateurDao().trouver_par_id(id_user)

    @log
    def modifier(self, utilisateur) -> Utilisateur:
        """Modification d'un utilisateur"""

        utilisateur.mdp = hash_password(utilisateur.mdp, utilisateur.nom_user)
        return utilisateur if UtilisateurDao().modifier(utilisateur) else None

    @log
    def supprimer(self, utilisateur) -> bool:
        """Supprimer le compte d'un utilisateur"""
        return UtilisateurDao().supprimer(utilisateur)

    @log
    def afficher_tous(self) -> str:
        """Afficher tous les utilisateurs
        Sortie : Une chaine de caractères mise sous forme de tableau
        """
        entetes = ["nom", "mail"]

        utilisateurs = UtilisateurDao().lister_tous()

        for j in utilisateurs:
            if j.nom_user == "admin":
                utilisateurs.remove(j)

        utilisateurs_as_list = [j.as_list() for j in utilisateurs]

        str_utilisateurs = "-" * 100
        str_utilisateurs += "\nListe des utilisateurs \n"
        str_utilisateurs += "-" * 100
        str_utilisateurs += "\n"
        str_utilisateurs += tabulate(
            tabular_data=utilisateurs_as_list,
            headers=entetes,
            tablefmt="psql",
            floatfmt=".2f",
        )
        str_utilisateurs += "\n"

        return str_utilisateurs

    @log
    def se_connecter(self, nom_user, mdp) -> Utilisateur:
        """Se connecter à partir de nom_user et mdp"""
        return UtilisateurDao().se_connecter(nom_user, hash_password(mdp, nom_user))

    @log
    def nom_user_deja_utilise(self, nom_user) -> bool:
        """Vérifie si le nom_user est déjà utilisé
        Retourne True si le nom_user existe déjà en BDD"""
        utilisateurs = UtilisateurDao().lister_tous()
        return nom_user in [j.nom_user for j in utilisateurs]
