import regex
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator, PasswordValidator
from prompt_toolkit.validation import ValidationError, Validator

from service.utilisateur_service import UtilisateurService
from view.vue_abstraite import VueAbstraite


class InscriptionVue(VueAbstraite):
    def choisir_menu(self):
        # Demande à l'utilisateur de saisir nom, mot de passe...
        nom = inquirer.text(message="Entrez votre nom : ").execute()

        if UtilisateurService().nom_user_deja_utilise(nom):
            from view.accueil.accueil_vue import AccueilVue

            return AccueilVue(f"Le nom {nom} est déjà utilisé.")

        mdp = inquirer.secret(
            message="Entrez votre mot de passe : ",
            validate=PasswordValidator(
                length=12,
                cap=True,
                number=True,
                message="Au moins 12 caractères, incluant une majuscule et un chiffre",
            ),
        ).execute()

        mail = inquirer.text(message="Entrez votre mail : ", validate=MailValidator()).execute()

        # Appel du service pour créer l'utilisateur
        utilisateur = UtilisateurService().creer(nom, mail, mdp)

        # Si l'utilisateur a été créé
        if utilisateur:
            message = (
                f"Votre compte {utilisateur.nom} a été créé. Vous pouvez maintenant vous connecter."
            )
        else:
            message = "Erreur de connexion (nom ou mot de passe invalide)"

        from view.accueil.accueil_vue import AccueilVue

        return AccueilVue(message)


class MailValidator(Validator):
    """la classe MailValidator verifie si la chaine de caractères
    que l'on entre correspond au format de l'email"""

    def validate(self, document) -> None:
        ok = regex.match(r"^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$", document.text)
        if not ok:
            raise ValidationError(
                message="Please enter a valid mail", cursor_position=len(document.text)
            )
