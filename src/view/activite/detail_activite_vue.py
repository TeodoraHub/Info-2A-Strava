from InquirerPy import inquirer
from datetime import datetime

from view.vue_abstraite import VueAbstraite
from service.activity_service import ActivityService
from service.like_service import LikeService
from service.commentaire_service import CommentaireService
from session import Session


class DetailActiviteVue(VueAbstraite):
    """Vue pour afficher les détails d'une activité"""

    def __init__(self, activity_id: int, message=""):
        super().__init__(message)
        self.activity_id = activity_id
        self.activity_service = ActivityService()
        self.like_service = LikeService()
        self.commentaire_service = CommentaireService()
        self.session = Session()

    def choisir_menu(self):
        """Affiche les détails de l'activité et propose des actions"""
        
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

        # Afficher les détails
        self._afficher_details_activite(activite, utilisateur)

        # Proposer des actions
        return self._proposer_actions(activite, utilisateur)

    def _afficher_details_activite(self, activite, utilisateur):
        """Affiche tous les détails de l'activité"""
        
        print("\n" + "=" * 70)
        print(f"🏃 {activite.titre}")
        print("=" * 70)
        
        # Informations principales
        print(f"\n📅 Date: {activite.date_activite}")
        print(f"🏷️  Sport: {activite.sport}")
        print(f"📍 Lieu: {activite.lieu if activite.lieu else 'Non renseigné'}")
        
        # Métriques
        print("\n📊 Métriques:")
        print(f"  • Distance: {activite.distance:.2f} km" if activite.distance else "  • Distance: N/A")
        
        if activite.duree:
            heures = int(activite.duree // 60)
            minutes = int(activite.duree % 60)
            print(f"  • Durée: {heures}h {minutes}min")
        
        # Vitesse moyenne (si applicable)
        if activite.distance and activite.duree and activite.duree > 0:
            vitesse_kmh = (activite.distance / activite.duree) * 60
            print(f"  • Vitesse moyenne: {vitesse_kmh:.2f} km/h")
        
        # Description
        if activite.description:
            print("\n📝 Description:")
            print(f"  {activite.description}")
        
        # Statistiques sociales
        nb_likes = self.like_service.count_likes_activite(self.activity_id)
        nb_commentaires = self.commentaire_service.count_commentaires_activite(self.activity_id)
        user_a_like = self.like_service.user_a_like(utilisateur.id_user, self.activity_id)
        
        print("\n💬 Interactions:")
        print(f"  • {nb_likes} like(s) {'❤️ (vous avez liké)' if user_a_like else '🤍'}")
        print(f"  • {nb_commentaires} commentaire(s)")
        
        # Afficher les commentaires
        self._afficher_commentaires()
        
        print("\n" + "=" * 70)

    def _afficher_commentaires(self):
        """Affiche la liste des commentaires"""
        commentaires = self.commentaire_service.get_commentaires_activite(self.activity_id)
        
        if commentaires:
            print(f"\n💬 Commentaires ({len(commentaires)}):")
            print("-" * 70)
            for comment in commentaires:
                # Afficher le nom de l'utilisateur si disponible
                auteur = f"Utilisateur #{comment.id_user}"
                if hasattr(comment, 'utilisateur') and comment.utilisateur:
                    auteur = comment.utilisateur.nom_user
                
                print(f"\n👤 {auteur}")
                print(f"   {comment.contenu}")
                if hasattr(comment, 'date_comment'):
                    print(f"   📅 {comment.date_comment}")
            print("-" * 70)

    def _proposer_actions(self, activite, utilisateur):
        """Propose les actions possibles selon le contexte"""
        
        # Vérifier si l'utilisateur est propriétaire de l'activité
        est_proprietaire = activite.id_user == utilisateur.id_user
        user_a_like = self.like_service.user_a_like(utilisateur.id_user, self.activity_id)
        
        # Construire la liste des choix
        choix = []
        
        # Actions de like
        if user_a_like:
            choix.append("💔 Retirer mon like")
        else:
            choix.append("❤️  Liker cette activité")
        
        # Actions de commentaire
        choix.append("💬 Ajouter un commentaire")
        
        # Voir les likes
        choix.append("👥 Voir qui a liké")
        
        # Actions propriétaire
        if est_proprietaire:
            choix.append("✏️  Modifier l'activité")
            choix.append("🗑️  Supprimer l'activité")
        
        # Navigation
        choix.append("⬅️  Retour à la liste des activités")
        
        # Demander le choix
        action = inquirer.select(
            message="Que voulez-vous faire ?",
            choices=choix
        ).execute()
        
        # Traiter l'action
        return self._traiter_action(action, activite, utilisateur)

    def _traiter_action(self, action, activite, utilisateur):
        """Traite l'action choisie par l'utilisateur"""
        
        if "Liker cette activité" in action:
            if self.like_service.liker_activite(utilisateur.id_user, self.activity_id):
                return DetailActiviteVue(self.activity_id, "✅ Activité likée !")
            else:
                return DetailActiviteVue(self.activity_id, "❌ Erreur lors du like")
        
        elif "Retirer mon like" in action:
            if self.like_service.unliker_activite(utilisateur.id_user, self.activity_id):
                return DetailActiviteVue(self.activity_id, "✅ Like retiré")
            else:
                return DetailActiviteVue(self.activity_id, "❌ Erreur")
        
        elif "Ajouter un commentaire" in action:
            contenu = inquirer.text(
                message="Votre commentaire:",
                validate=lambda text: len(text.strip()) > 0
            ).execute()
            
            if self.commentaire_service.creer_commentaire(
                utilisateur.id_user, 
                self.activity_id, 
                contenu
            ):
                return DetailActiviteVue(self.activity_id, "✅ Commentaire ajouté !")
            else:
                return DetailActiviteVue(self.activity_id, "❌ Erreur lors de l'ajout du commentaire")
        
        elif "Voir qui a liké" in action:
            self._afficher_likes()
            input("\nAppuyez sur Entrée pour continuer...")
            return DetailActiviteVue(self.activity_id)
        
        elif "Modifier l'activité" in action:
            from view.activite.modifier_activite_vue import ModifierActiviteVue
            return ModifierActiviteVue(activity_id=self.activity_id)
        
        elif "Supprimer l'activité" in action:
            confirmer = inquirer.confirm(
                message="⚠️  Êtes-vous sûr de vouloir supprimer cette activité ?",
                default=False
            ).execute()
            
            if confirmer:
                if self.activity_service.supprimer_activite(self.activity_id):
                    from view.activite.liste_activites_vue import ListeActivitesVue
                    return ListeActivitesVue("✅ Activité supprimée")
                else:
                    return DetailActiviteVue(self.activity_id, "❌ Erreur lors de la suppression")
            else:
                return DetailActiviteVue(self.activity_id)
        
        elif "Retour à la liste" in action:
            from view.activite.liste_activites_vue import ListeActivitesVue
            return ListeActivitesVue()

    def _afficher_likes(self):
        """Affiche la liste des utilisateurs qui ont liké"""
        likes = self.like_service.get_likes_activite(self.activity_id)
        
        if not likes:
            print("\n🤍 Aucun like pour le moment")
            return
        
        print(f"\n❤️  Personnes qui ont liké ({len(likes)}):")
        print("-" * 50)
        for like in likes:
            # Afficher le nom de l'utilisateur si disponible
            nom = f"Utilisateur #{like.id_user}"
            if hasattr(like, 'utilisateur') and like.utilisateur:
                nom = like.utilisateur.nom_user
            print(f"  • {nom}")
        print("-" * 50)