from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator
from datetime import datetime

from view.vue_abstraite import VueAbstraite
from service.activity_service import ActivityService
from session import Session


class ModifierActiviteVue(VueAbstraite):
    """Vue pour modifier une activité existante"""

    def __init__(self, activity_id: int, message=""):
        super().__init__(message)
        self.activity_id = activity_id
        self.activity_service = ActivityService()
        self.session = Session()

    def choisir_menu(self):
        """Permet de modifier les informations d'une activité"""
        
        # Récupérer l'utilisateur connecté
        utilisateur = self.session.utilisateur
        if not utilisateur:
            print("Erreur : Aucun utilisateur connecté")
            from view.connexion_vue import ConnexionVue
            return ConnexionVue("Veuillez vous connecter")

        # Récupérer l'activité
        activite = self.activity_service.get_activite_by_id(self.activity_id)
        
        if not activite:
            print(f"❌ Activité {self.activity_id} introuvable.")
            from view.activite.liste_activites_vue import ListeActivitesVue
            return ListeActivitesVue("Activité introuvable")

        # Vérifier que l'utilisateur est bien le propriétaire
        if activite.id_user != utilisateur.id_user:
            print("❌ Vous n'êtes pas autorisé à modifier cette activité.")
            from view.activite.detail_activite_vue import DetailActiviteVue
            return DetailActiviteVue(self.activity_id, "Accès refusé")

        # Afficher les informations actuelles
        self._afficher_infos_actuelles(activite)

        # Demander ce qui doit être modifié
        return self._proposer_modifications(activite)

    def _afficher_infos_actuelles(self, activite):
        """Affiche les informations actuelles de l'activité"""
        print("\n" + "=" * 70)
        print("✏️  MODIFICATION D'ACTIVITÉ")
        print("=" * 70)
        print("\n📋 Informations actuelles:")
        print(f"  • Titre: {activite.titre}")
        print(f"  • Sport: {activite.sport}")
        print(f"  • Date: {activite.date_activite}")
        print(f"  • Lieu: {activite.lieu if activite.lieu else 'Non renseigné'}")
        print(f"  • Distance: {activite.distance:.2f} km" if activite.distance else "  • Distance: N/A")
        
        if activite.duree:
            heures = int(activite.duree // 60)
            minutes = int(activite.duree % 60)
            print(f"  • Durée: {heures}h {minutes}min")
        
        if activite.description:
            print(f"  • Description: {activite.description}")
        
        print("=" * 70 + "\n")

    def _proposer_modifications(self, activite):
        """Propose de modifier les différents champs"""
        
        choix = inquirer.checkbox(
            message="Sélectionnez les champs à modifier (Espace pour sélectionner, Entrée pour valider):",
            choices=[
                {"name": "Titre", "value": "titre"},
                {"name": "Description", "value": "description"},
                {"name": "Lieu", "value": "lieu"},
                {"name": "Date", "value": "date"},
            ],
        ).execute()

        if not choix:
            # Aucune modification sélectionnée
            confirmer = inquirer.confirm(
                message="Aucune modification sélectionnée. Retour aux détails ?",
                default=True
            ).execute()
            
            if confirmer:
                from view.activite.detail_activite_vue import DetailActiviteVue
                return DetailActiviteVue(self.activity_id)
            else:
                return ModifierActiviteVue(self.activity_id)

        # Créer un dictionnaire avec les nouvelles valeurs
        nouvelles_valeurs = {}

        # Demander les nouvelles valeurs pour chaque champ sélectionné
        if "titre" in choix:
            nouvelles_valeurs["titre"] = inquirer.text(
                message="Nouveau titre:",
                default=activite.titre,
                validate=EmptyInputValidator("Le titre ne peut pas être vide")
            ).execute()

        if "description" in choix:
            nouvelles_valeurs["description"] = inquirer.text(
                message="Nouvelle description:",
                default=activite.description if activite.description else ""
            ).execute()

        if "lieu" in choix:
            nouvelles_valeurs["lieu"] = inquirer.text(
                message="Nouveau lieu:",
                default=activite.lieu if activite.lieu else ""
            ).execute()

        if "date" in choix:
            nouvelles_valeurs["date"] = self._demander_nouvelle_date(activite.date_activite)

        # Confirmer les modifications
        return self._confirmer_modifications(activite, nouvelles_valeurs)

    def _demander_nouvelle_date(self, date_actuelle):
        """Demande une nouvelle date avec validation"""
        print(f"\n📅 Date actuelle: {date_actuelle}")
        print("Format attendu: JJ/MM/AAAA (ex: 25/12/2025)")
        
        while True:
            date_str = inquirer.text(
                message="Nouvelle date:",
                default=date_actuelle.strftime("%d/%m/%Y") if hasattr(date_actuelle, 'strftime') else str(date_actuelle)
            ).execute()
            
            try:
                # Essayer de parser la date
                nouvelle_date = datetime.strptime(date_str, "%d/%m/%Y").date()
                return nouvelle_date
            except ValueError:
                print("❌ Format de date invalide. Utilisez JJ/MM/AAAA")
                retry = inquirer.confirm(
                    message="Réessayer ?",
                    default=True
                ).execute()
                if not retry:
                    return date_actuelle

    def _confirmer_modifications(self, activite, nouvelles_valeurs):
        """Affiche un récapitulatif et demande confirmation"""
        
        print("\n" + "=" * 70)
        print("📝 RÉCAPITULATIF DES MODIFICATIONS")
        print("=" * 70)
        
        for champ, nouvelle_valeur in nouvelles_valeurs.items():
            ancienne_valeur = getattr(activite, champ, "N/A")
            print(f"\n{champ.capitalize()}:")
            print(f"  Ancien: {ancienne_valeur}")
            print(f"  Nouveau: {nouvelle_valeur}")
        
        print("=" * 70)
        
        confirmer = inquirer.confirm(
            message="\n✅ Confirmer ces modifications ?",
            default=True
        ).execute()
        
        if not confirmer:
            retry = inquirer.confirm(
                message="Voulez-vous recommencer la modification ?",
                default=False
            ).execute()
            
            if retry:
                return ModifierActiviteVue(self.activity_id)
            else:
                from view.activite.detail_activite_vue import DetailActiviteVue
                return DetailActiviteVue(self.activity_id, "Modifications annulées")

        # Appliquer les modifications
        return self._appliquer_modifications(activite, nouvelles_valeurs)

    def _appliquer_modifications(self, activite, nouvelles_valeurs):
        """Applique les modifications à l'activité"""
        
        # Mettre à jour les champs de l'activité
        for champ, valeur in nouvelles_valeurs.items():
            setattr(activite, champ, valeur)

        # Sauvegarder en base de données
        try:
            if self.activity_service.modifier_activite(activite):
                print("\n✅ Activité modifiée avec succès !")
                from view.activite.detail_activite_vue import DetailActiviteVue
                return DetailActiviteVue(self.activity_id, "✅ Modifications enregistrées")
            else:
                print("\n❌ Erreur lors de la sauvegarde des modifications")
                retry = inquirer.confirm(
                    message="Voulez-vous réessayer ?",
                    default=True
                ).execute()
                
                if retry:
                    return ModifierActiviteVue(self.activity_id)
                else:
                    from view.activite.detail_activite_vue import DetailActiviteVue
                    return DetailActiviteVue(self.activity_id, "❌ Modifications non enregistrées")
        
        except Exception as e:
            print(f"\n❌ Erreur inattendue: {e}")
            from view.activite.detail_activite_vue import DetailActiviteVue
            return DetailActiviteVue(self.activity_id, "❌ Erreur lors de la modification")