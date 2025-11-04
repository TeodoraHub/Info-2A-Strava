from InquirerPy import prompt

from view.vue_abstraite import VueAbstraite
from service.activity_service import ActivityService
from session import Session


class ListeActivitesVue(VueAbstraite):
    """Vue pour afficher la liste des activités d'un utilisateur"""

    def __init__(self, message=""):
        super().__init__(message)
        self.activity_service = ActivityService()
        self.session = Session()

    def choisir_menu(self):
        """Affiche la liste des activités et propose des actions"""
        
        # Récupérer l'utilisateur connecté
        utilisateur = self.session.utilisateur
        if not utilisateur:
            print("Erreur : Aucun utilisateur connecté")
            from view.connexion_vue import ConnexionVue
            return ConnexionVue("Veuillez vous connecter")

        # Récupérer les activités de l'utilisateur
        activites = self.activity_service.get_activites_by_user(utilisateur.id_utilisateur)

        # Cas où il n'y a aucune activité
        if not activites:
            print("📭 Vous n'avez encore aucune activité enregistrée.\n")
            choix = prompt([
                {
                    'type': 'list',
                    'name': 'action',
                    'message': 'Que voulez-vous faire ?',
                    'choices': [
                        'Créer une activité',
                        'Retour au menu principal'
                    ]
                }
            ])

            if choix['action'] == 'Créer une activité':
                from view.activite.creer_activite_vue import CreerActiviteVue
                return CreerActiviteVue()
            else:
                from view.menu_utilisateur_vue import MenuUtilisateurVue
                return MenuUtilisateurVue()

        # Afficher le résumé des activités
        self._afficher_resume(activites)

        # Préparer les choix pour le menu
        choix_activites = []
        for act in activites:
            # Format d'affichage : "Date - Type - Distance - Durée"
            distance = f"{act.distance:.2f} km" if hasattr(act, 'distance') and act.distance else "N/A"
            duree = f"{act.duree} min" if hasattr(act, 'duree') and act.duree else "N/A"
            
            label = f"{act.date_activite} - {act.type_activite} - {distance} - {duree}"
            choix_activites.append({
                'name': label,
                'value': act.id
            })

        # Ajouter les options de menu
        choix_activites.extend([
            {'name': '➕ Créer une nouvelle activité', 'value': 'creer'},
            {'name': '⬅️  Retour au menu principal', 'value': 'retour'}
        ])

        # Demander l'action à effectuer
        questions = [
            {
                'type': 'list',
                'name': 'choix',
                'message': 'Sélectionnez une activité pour voir les détails ou choisissez une action :',
                'choices': choix_activites
            }
        ]

        reponse = prompt(questions)

        # Traiter le choix
        if reponse['choix'] == 'creer':
            from view.activite.creer_activite_vue import CreerActiviteVue
            return CreerActiviteVue()
        elif reponse['choix'] == 'retour':
            from view.menu_utilisateur_vue import MenuUtilisateurVue
            return MenuUtilisateurVue()
        else:
            # Afficher les détails de l'activité sélectionnée
            from view.activite.detail_activite_vue import DetailActiviteVue
            return DetailActiviteVue(activity_id=reponse['choix'])

    def _afficher_resume(self, activites):
        """Affiche un résumé statistique des activités"""
        print(f"\n{'='*60}")
        print(f"📊 VOS ACTIVITÉS ({len(activites)} au total)")
        print(f"{'='*60}\n")

        # Calculer quelques statistiques
        types_activites = {}
        distance_totale = 0
        duree_totale = 0

        for act in activites:
            # Compter par type
            if act.type_activite not in types_activites:
                types_activites[act.type_activite] = 0
            types_activites[act.type_activite] += 1

            # Cumuler distance et durée
            if hasattr(act, 'distance') and act.distance:
                distance_totale += act.distance
            if hasattr(act, 'duree') and act.duree:
                duree_totale += act.duree

        # Afficher les statistiques
        print("📈 Résumé :")
        for type_act, count in types_activites.items():
            print(f"  • {type_act}: {count} activité(s)")
        
        if distance_totale > 0:
            print(f"\n🏃 Distance totale : {distance_totale:.2f} km")
        if duree_totale > 0:
            heures = duree_totale // 60
            minutes = duree_totale % 60
            print(f"⏱️  Durée totale : {heures}h {minutes}min")
        
        print(f"\n{'='*60}\n")