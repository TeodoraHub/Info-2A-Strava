
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator, PathValidator
from datetime import datetime

from view.vue_abstraite import VueAbstraite
from service.activity_service import ActivityService
from utils.gpx_parser import parse_gpx_file
from session import Session


class CreerActiviteVue(VueAbstraite):
    """Vue pour créer une nouvelle activité avec upload GPX"""

    def __init__(self, message=""):
        super().__init__(message)
        self.activity_service = ActivityService()
        self.session = Session()

    def choisir_menu(self):
        """Processus de création d'une activité"""
        
        # Récupérer l'utilisateur connecté
        utilisateur = self.session.utilisateur
        if not utilisateur:
            print("Erreur : Aucun utilisateur connecté")
            from view.connexion_vue import ConnexionVue
            return ConnexionVue("Veuillez vous connecter")

        print("\n" + "=" * 70)
        print("➕ CRÉER UNE NOUVELLE ACTIVITÉ")
        print("=" * 70 + "\n")

        # Étape 1 : Choix du mode de création
        mode = self._choisir_mode_creation()
        
        if mode == "retour":
            from view.activite.liste_activites_vue import ListeActivitesVue
            return ListeActivitesVue()

        # Étape 2 : Collecte des informations
        if mode == "gpx":
            return self._creer_avec_gpx(utilisateur)
        else:
            return self._creer_manuellement(utilisateur)

    def _choisir_mode_creation(self):
        """Demande le mode de création de l'activité"""
        choix = inquirer.select(
            message="Comment voulez-vous créer l'activité ?",
            choices=[
                {"name": "📁 Importer un fichier GPX (recommandé)", "value": "gpx"},
                {"name": "✍️  Saisie manuelle", "value": "manuel"},
                {"name": "⬅️  Retour", "value": "retour"}
            ]
        ).execute()
        
        return choix

    def _creer_avec_gpx(self, utilisateur):
        """Création d'activité à partir d'un fichier GPX"""
        
        print("\n📁 Import d'un fichier GPX")
        print("-" * 70)
        print("Le fichier GPX doit contenir les données de votre activité.")
        print("Formats acceptés : .gpx")
        print("-" * 70 + "\n")

        # Demander le chemin du fichier GPX
        fichier_gpx = inquirer.filepath(
            message="Chemin du fichier GPX:",
            validate=PathValidator(is_file=True, message="Le fichier n'existe pas"),
            only_files=True
        ).execute()

        # Vérifier l'extension
        if not fichier_gpx.lower().endswith('.gpx'):
            print("\n❌ Le fichier doit avoir l'extension .gpx")
            retry = inquirer.confirm(
                message="Réessayer ?",
                default=True
            ).execute()
            
            if retry:
                return CreerActiviteVue()
            else:
                from view.activite.liste_activites_vue import ListeActivitesVue
                return ListeActivitesVue()

        # Parser le fichier GPX
        try:
            print("\n⏳ Analyse du fichier GPX en cours...")
            gpx_data = parse_gpx_file(fichier_gpx)
            
            if not gpx_data:
                print("❌ Impossible de lire le fichier GPX")
                return self._gerer_erreur_gpx()
            
            print("✅ Fichier GPX analysé avec succès !")
            self._afficher_donnees_gpx(gpx_data)
            
        except Exception as e:
            print(f"❌ Erreur lors de la lecture du fichier : {e}")
            return self._gerer_erreur_gpx()

        # Compléter avec les informations manquantes
        return self._completer_infos_activite(utilisateur, gpx_data)

    def _afficher_donnees_gpx(self, gpx_data):
        """Affiche les données extraites du GPX"""
        print("\n📊 Données extraites du fichier:")
        print("-" * 50)
        
        if gpx_data.get('distance'):
            print(f"  • Distance: {gpx_data['distance']:.2f} km")
        
        if gpx_data.get('duration_minutes'):
            heures = int(gpx_data['duration_minutes'] // 60)
            minutes = int(gpx_data['duration_minutes'] % 60)
            print(f"  • Durée: {heures}h {minutes}min")
        
        if gpx_data.get('elevation_gain'):
            print(f"  • Dénivelé positif: {gpx_data['elevation_gain']:.0f} m")
        
        if gpx_data.get('start_time'):
            print(f"  • Date de début: {gpx_data['start_time']}")
        
        print("-" * 50 + "\n")

    def _gerer_erreur_gpx(self):
        """Gère les erreurs de lecture GPX"""
        choix = inquirer.select(
            message="Que voulez-vous faire ?",
            choices=[
                "Réessayer avec un autre fichier",
                "Créer manuellement",
                "Annuler"
            ]
        ).execute()
        
        if choix == "Réessayer avec un autre fichier":
            return CreerActiviteVue()
        elif choix == "Créer manuellement":
            return self._creer_manuellement(self.session.utilisateur)
        else:
            from view.activite.liste_activites_vue import ListeActivitesVue
            return ListeActivitesVue()

    def _completer_infos_activite(self, utilisateur, gpx_data=None):
        """Demande les informations complémentaires pour l'activité"""
        
        print("\n📝 Informations complémentaires")
        print("-" * 70)
        
        # Titre
        titre = inquirer.text(
            message="Titre de l'activité:",
            validate=EmptyInputValidator("Le titre est obligatoire")
        ).execute()

        # Type de sport
        sport = inquirer.select(
            message="Type de sport:",
            choices=[
                "Course à pied",
                "Cyclisme",
                "Natation",
                "Randonnée",
                "Autre"
            ]
        ).execute()

        # Lieu
        lieu = inquirer.text(
            message="Lieu:",
            default=""
        ).execute()

        # Description
        description = inquirer.text(
            message="Description (optionnel):",
            default=""
        ).execute()

        # Date
        if gpx_data and gpx_data.get('start_time'):
            date_activite = gpx_data['start_time']
            print(f"\n📅 Date extraite du GPX: {date_activite}")
            modifier_date = inquirer.confirm(
                message="Voulez-vous modifier la date ?",
                default=False
            ).execute()
            
            if modifier_date:
                date_activite = self._demander_date()
        else:
            date_activite = self._demander_date()

        # Distance et durée
        if gpx_data:
            distance = gpx_data.get('distance', 0)
            duree = gpx_data.get('duration_minutes', 0)
        else:
            distance = self._demander_distance()
            duree = self._demander_duree()

        # Créer le dictionnaire de données
        activity_data = {
            "titre": titre,
            "description": description,
            "sport": sport,
            "date_activite": date_activite,
            "lieu": lieu,
            "distance": distance,
            "duree": duree,
            "id_user": utilisateur.id_user
        }

        # Afficher le récapitulatif et confirmer
        return self._confirmer_creation(activity_data)

    def _creer_manuellement(self, utilisateur):
        """Création manuelle d'une activité sans fichier GPX"""
        
        print("\n✍️  Création manuelle d'activité")
        print("-" * 70)
        
        return self._completer_infos_activite(utilisateur, gpx_data=None)

    def _demander_date(self):
        """Demande la date de l'activité"""
        
        utiliser_aujourdhui = inquirer.confirm(
            message="Utiliser la date d'aujourd'hui ?",
            default=True
        ).execute()
        
        if utiliser_aujourdhui:
            return datetime.now().date()
        
        print("\nFormat attendu: JJ/MM/AAAA (ex: 25/12/2025)")
        
        while True:
            date_str = inquirer.text(
                message="Date de l'activité:",
                default=datetime.now().strftime("%d/%m/%Y")
            ).execute()
            
            try:
                return datetime.strptime(date_str, "%d/%m/%Y").date()
            except ValueError:
                print("❌ Format de date invalide. Utilisez JJ/MM/AAAA")
                retry = inquirer.confirm(
                    message="Réessayer ?",
                    default=True
                ).execute()
                if not retry:
                    return datetime.now().date()

    def _demander_distance(self):
        """Demande la distance en km"""
        while True:
            distance_str = inquirer.text(
                message="Distance (en km):",
                validate=EmptyInputValidator("La distance est obligatoire")
            ).execute()
            
            try:
                distance = float(distance_str.replace(',', '.'))
                if distance <= 0:
                    print("❌ La distance doit être positive")
                    continue
                return distance
            except ValueError:
                print("❌ Veuillez entrer un nombre valide")

    def _demander_duree(self):
        """Demande la durée en minutes"""
        while True:
            duree_str = inquirer.text(
                message="Durée (en minutes):",
                validate=EmptyInputValidator("La durée est obligatoire")
            ).execute()
            
            try:
                duree = float(duree_str.replace(',', '.'))
                if duree <= 0:
                    print("❌ La durée doit être positive")
                    continue
                return duree
            except ValueError:
                print("❌ Veuillez entrer un nombre valide")

    def _confirmer_creation(self, activity_data):
        """Affiche un récapitulatif et demande confirmation"""
        
        print("\n" + "=" * 70)
        print("📋 RÉCAPITULATIF DE L'ACTIVITÉ")
        print("=" * 70)
        print(f"\n🏷️  Titre: {activity_data['titre']}")
        print(f"🏃 Sport: {activity_data['sport']}")
        print(f"📅 Date: {activity_data['date_activite']}")
        print(f"📍 Lieu: {activity_data['lieu'] if activity_data['lieu'] else 'Non renseigné'}")
        print(f"📏 Distance: {activity_data['distance']:.2f} km")
        
        heures = int(activity_data['duree'] // 60)
        minutes = int(activity_data['duree'] % 60)
        print(f"⏱️  Durée: {heures}h {minutes}min")
        
        if activity_data['description']:
            print(f"📝 Description: {activity_data['description']}")
        
        print("=" * 70)
        
        confirmer = inquirer.confirm(
            message="\n✅ Créer cette activité ?",
            default=True
        ).execute()
        
        if not confirmer:
            retry = inquirer.confirm(
                message="Voulez-vous recommencer ?",
                default=False
            ).execute()
            
            if retry:
                return CreerActiviteVue()
            else:
                from view.activite.liste_activites_vue import ListeActivitesVue
                return ListeActivitesVue("Création annulée")

        # Créer l'activité
        return self._sauvegarder_activite(activity_data)

    def _sauvegarder_activite(self, activity_data):
        """Sauvegarde l'activité en base de données"""
        
        try:
            print("\n⏳ Création de l'activité en cours...")
            
            if self.activity_service.creer_activite_from_dict(activity_data):
                print("✅ Activité créée avec succès !")
                from view.activite.liste_activites_vue import ListeActivitesVue
                return ListeActivitesVue("✅ Activité créée avec succès !")
            else:
                print("❌ Erreur lors de la création de l'activité")
                retry = inquirer.confirm(
                    message="Voulez-vous réessayer ?",
                    default=True
                ).execute()
                
                if retry:
                    return CreerActiviteVue()
                else:
                    from view.activite.liste_activites_vue import ListeActivitesVue
                    return ListeActivitesVue("❌ Création annulée")
        
        except Exception as e:
            print(f"\n❌ Erreur inattendue: {e}")
            from view.activite.liste_activites_vue import ListeActivitesVue
            return ListeActivitesVue("❌ Erreur lors de la création")