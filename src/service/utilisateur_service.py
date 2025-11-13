from tabulate import tabulate

from business_object.user_object.utilisateur import Utilisateur
from dao.utilisateur_dao import UtilisateurDAO
from utils.log_decorator import log
from utils.securite import hash_password
from utils.singleton import Singleton


class UtilisateurService(metaclass=Singleton):
    """Expose les operations de plus haut niveau sur les utilisateurs."""

    def __init__(self):
        self.utilisateur_dao = UtilisateurDAO()

    @log
    def creer(self, nom_user, mail_user, mdp) -> dict | None:
        """Cree un utilisateur (id genere en base)."""
        nouvel_utilisateur = Utilisateur(
            id_user=None,
            nom_user=nom_user,
            mail_user=mail_user,
            mdp=hash_password(mdp, nom_user),
        )

        if self.utilisateur_dao.creer(nouvel_utilisateur):
            return {
                "id_user": nouvel_utilisateur.id_user,
                "nom_user": nouvel_utilisateur.nom_user,
                "mail_user": nouvel_utilisateur.mail_user,
            }
        return None

    @log
    def trouver_par_id(self, id_user) -> Utilisateur | None:
        """Retourne l'utilisateur correspondant a l'identifiant."""
        return self.utilisateur_dao.trouver_par_id(id_user)

    @log
    def modifier(self, utilisateur) -> Utilisateur | None:
        """Met a jour un utilisateur apres avoir rehash le mot de passe."""
        utilisateur.mdp = hash_password(utilisateur.mdp, utilisateur.nom_user)
        return utilisateur if self.utilisateur_dao.modifier(utilisateur) else None

    @log
    def supprimer(self, utilisateur) -> bool:
        """Supprime un utilisateur."""
        return self.utilisateur_dao.supprimer(utilisateur)

    @log
    def afficher_tous(self) -> str:
        """Retourne une representation tabulaire des utilisateurs."""
        entetes = ["id", "nom", "mail"]
        utilisateurs = [u for u in self.utilisateur_dao.lister_tous() if u.nom_user != "admin"]
        tableau = tabulate(
            tabular_data=[u.as_list() for u in utilisateurs],
            headers=entetes,
            tablefmt="psql",
            floatfmt=".2f",
        )
        return "-" * 100 + "\nListe des utilisateurs \n" + "-" * 100 + "\n" + tableau + "\n"

    @log
    def se_connecter(self, nom_user, mdp) -> Utilisateur | None:
        """Authentifie un utilisateur a partir de son nom/mot de passe."""
        return self.utilisateur_dao.se_connecter(nom_user, hash_password(mdp, nom_user))

    @log
    def nom_user_deja_utilise(self, nom_user) -> bool:
        """Indique si le nom est deja utilise."""
        utilisateurs = self.utilisateur_dao.lister_tous()
        return nom_user in [u.nom_user for u in utilisateurs]

    @log
    def mail_deja_utilise(self, mail_user) -> bool:
        """Indique si le mail est deja utilise."""
        utilisateurs = self.utilisateur_dao.lister_tous()
        return mail_user in [u.mail_user for u in utilisateurs]

    @log
    def lister_tous(self) -> list:
        """Retourne la liste de tous les utilisateurs."""
        return self.utilisateur_dao.lister_tous()
