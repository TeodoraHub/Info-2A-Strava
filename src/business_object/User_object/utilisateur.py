class Utilisateur:
    """
    Classe représentant un Utilisateur

    Attributs
    ----------
    id_user : int
        identifiant
    nom_user : str
        nom de l'utilisateur
    mail_user : str
        adresse mail de l'utilisateur
    mdp : str
        le mot de passe du joueur
    """

    def __init__(self, id_user, nom_user, mail_user, mdp):
        """Constructeur"""
        self.id_user = id_user
        self.nom_user = nom_user
        self.mail_user = mail_user
        self.mdp = mdp
