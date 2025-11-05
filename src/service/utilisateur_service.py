from tabulate import tabulate
from business_object.user_object.utilisateur import Utilisateur
from dao.utilisateur_dao import UtilisateurDAO
from utils.log_decorator import log
from utils.securite import hash_password


class UtilisateurService:
    """Classe contenant les méthodes de service des Utilisateurs"""

    @log
    def creer(self, nom_user, mail_user, mdp) -> Utilisateur:
        """Création d'un utilisateur"""
        # Générer automatiquement l'ID
        utilisateurs = UtilisateurDAO().lister_tous()
        if utilisateurs:
            nouvel_id = max([u.id_user for u in utilisateurs]) + 1
        else:
            nouvel_id = 1
        
        nouvel_utilisateur = Utilisateur(
            id_user=nouvel_id,
            nom_user=nom_user,
            mail_user=mail_user,
            mdp=hash_password(mdp, nom_user),
        )
        return nouvel_utilisateur if UtilisateurDAO().creer(nouvel_utilisateur) else None

    @log
    def trouver_par_id(self, id_user) -> Utilisateur:
        """Trouver un utilisateur à partir de son id"""
        return UtilisateurDAO().trouver_par_id(id_user)

    @log
    def modifier(self, utilisateur) -> Utilisateur:
        """Modification d'un utilisateur"""
        utilisateur.mdp = hash_password(utilisateur.mdp, utilisateur.nom_user)
        return utilisateur if UtilisateurDAO().modifier(utilisateur) else None

    @log
    def supprimer(self, utilisateur) -> bool:
        """Supprimer le compte d'un utilisateur"""
        return UtilisateurDAO().supprimer(utilisateur)

    @log
    def afficher_tous(self) -> str:
        """Afficher tous les utilisateurs
        Sortie : Une chaine de caractères mise sous forme de tableau
        """
        entetes = ["nom", "mail"]
        utilisateurs = UtilisateurDAO().lister_tous()
        
        # ✅ Filtrer sans modifier la liste pendant l'itération
        utilisateurs = [u for u in utilisateurs if u.nom_user != "admin"]
        
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
        return UtilisateurDAO().se_connecter(nom_user, hash_password(mdp, nom_user))

    @log
    def nom_user_deja_utilise(self, nom_user) -> bool:
        """Vérifie si le nom_user est déjà utilisé
        Retourne True si le nom_user existe déjà en BDD"""
        utilisateurs = UtilisateurDAO().lister_tous()
        return nom_user in [j.nom_user for j in utilisateurs]
    
    @log
    def mail_deja_utilise(self, mail_user) -> bool:
        """Vérifie si le mail est déjà utilisé
        Retourne True si le mail existe déjà en BDD"""
        utilisateurs = UtilisateurDAO().lister_tous()
        return mail_user in [j.mail_user for j in utilisateurs]