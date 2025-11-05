# Travaux Réalisés - Projet Striv

# Etat d'analyse de notre projet

## Date:  Octobre 2025

---

## ✅ Fichiers réalisés

### 1. DAO (Data Access Object) - Couche d'accès aux données

#### **src/dao/like_dao.py** ✅ 
- `creer_like()` - Créer un like
- `supprimer_like()` - Supprimer un like
- `get_likes_by_activity()` - Récupérer tous les likes d'une activité
- `count_likes_by_activity()` - Compter les likes d'une activité
- `user_a_like()` - Vérifier si un utilisateur a liké
- `get_likes_by_user()` - Récupérer tous les likes d'un utilisateur

#### **src/dao/suivi_dao.py** ✅ 
- `creer_suivi()` - Créer une relation de suivi
- `supprimer_suivi()` - Supprimer une relation de suivi
- `get_followers()` - Récupérer la liste des followers
- `get_following()` - Récupérer la liste des utilisateurs suivis
- `user_suit()` - Vérifier si un utilisateur en suit un autre
- `count_followers()` - Compter le nombre de followers
- `count_following()` - Compter le nombre d'utilisateurs suivis

#### **src/dao/commentaire_dao.py** ✅ 
- `creer_commentaire()` - Créer un commentaire (existant)
- `supprimer_commentaire()` - Supprimer un commentaire (ajouté)
- `get_commentaires_by_activity()` - Récupérer commentaires d'une activité (ajouté)
- `get_commentaires_by_user()` - Récupérer commentaires d'un utilisateur (ajouté)
- `count_commentaires_by_activity()` - Compter les commentaires (ajouté)
- `modifier_commentaire()` - Modifier un commentaire (ajouté)

---

### 2. SERVICES - Couche logique métier

#### **src/service/activity_service.py** ✅ 
- `creer_activite()` - Créer une activité
- `get_activite_by_id()` - Récupérer une activité par ID
- `get_activites_by_user()` - Récupérer les activités d'un utilisateur
- `get_feed()` - Récupérer le fil d'actualités
- `get_monthly_activities()` - Récupérer activités mensuelles
- `supprimer_activite()` - Supprimer une activité
- `modifier_activite()` - Modifier une activité

#### **src/service/like_service.py** ✅ 
- `liker_activite()` - Liker une activité
- `unliker_activite()` - Retirer un like
- `get_likes_activite()` - Récupérer les likes d'une activité
- `count_likes_activite()` - Compter les likes
- `user_a_like()` - Vérifier si l'utilisateur a liké
- `get_likes_user()` - Récupérer les likes d'un utilisateur

#### **src/service/commentaire_service.py** ✅ 
- `creer_commentaire()` - Créer un commentaire
- `supprimer_commentaire()` - Supprimer un commentaire
- `modifier_commentaire()` - Modifier un commentaire
- `get_commentaires_activite()` - Récupérer commentaires d'une activité
- `get_commentaires_user()` - Récupérer commentaires d'un utilisateur
- `count_commentaires_activite()` - Compter les commentaires

#### **src/service/suivi_service.py** ✅ 
- `suivre_utilisateur()` - Suivre un utilisateur
- `ne_plus_suivre()` - Ne plus suivre un utilisateur
- `get_followers()` - Récupérer les followers
- `get_following()` - Récupérer les utilisateurs suivis
- `user_suit()` - Vérifier si un utilisateur en suit un autre
- `count_followers()` - Compter les followers
- `count_following()` - Compter les utilisateurs suivis

#### **src/service/statistiques_service.py** ✅ 
- `get_statistiques_mensuelles()` - Statistiques mensuelles
- `get_statistiques_annuelles()` - Statistiques annuelles
- `get_statistiques_globales()` - Statistiques globales
- `get_sport_prefere()` - Déterminer le sport préféré
- `get_moyenne_par_semaine()` - Moyennes par semaine

---

### 3. UTILITAIRES

#### **src/utils/gpx_parser.py** ✅ 
Parser complet pour fichiers GPX:
- `parse_gpx_file()` - Parser un fichier GPX complet
- `_extract_track_points()` - Extraire les points de trace
- `_parse_track_point()` - Parser un point individuel
- `_calculate_total_distance()` - Calculer la distance totale
- `_haversine_distance()` - Calculer distance entre 2 points GPS
- `_calculate_duration()` - Calculer la durée
- `get_elevation_gain()` - Calculer le dénivelé

#### **src/utils/securite.py** ✅ 
Fonctions de sécurité renforcées:
- `hash_password()` - Hashage SHA256 (ancienne version, conservée)
- `hash_password_bcrypt()` - Hashage bcrypt (recommandé) 
- `verify_password_bcrypt()` - Vérifier mot de passe bcrypt
- `generate_secure_token()` - Générer token sécurisé 
- `valider_force_mot_de_passe()` - Valider force du mot de passe 
- `sanitize_input()` - Nettoyer les entrées utilisateur 

---

### 4. BUSINESS OBJECTS

#### **src/business_object/Like_Comment_object/commentaire.py** ✅ 
- Ajout de l'attribut `id_comment` manquant

---

### 5. DÉPENDANCES

#### **requirements.txt** ✅ 
- Ajout de `bcrypt` pour le hashage sécurisé des mots de passe

---

### 6. API REST

#### **src/API.py** ✅ 
API REST  avec la majorité endpoints:

**Endpoints Utilisateurs:**
- `GET /users/{user_id}/profil` - Profil avec followers/following
- `POST /users/{user_id}/follow/{target_user_id}` - Suivre un utilisateur
- `DELETE /users/{user_id}/follow/{target_user_id}` - Ne plus suivre
- `GET /users/{user_id}/statistics` - Statistiques (monthly/yearly/global)
- `GET /users/{user_id}/activities` - Liste des activités
- `GET /users/{user_id}/feed` - Fil d'actualités

**Endpoints Activités:**
- `GET /activities/{activity_id}` - Détails d'une activité
- `DELETE /activities/{activity_id}` - Supprimer une activité

**Endpoints Likes:**
- `POST /activities/{activity_id}/like` - Liker une activité
- `DELETE /activities/{activity_id}/like` - Retirer un like
- `GET /activities/{activity_id}/likes` - Liste des likes

**Endpoints Commentaires:**
- `POST /activities/{activity_id}/comment` - Commenter
- `GET /activities/{activity_id}/comments` - Liste des commentaires
- `DELETE /comments/{comment_id}` - Supprimer un commentaire

**Endpoints Utilitaires:**
- `GET /` - Informations sur l'API
- `GET /me` - Informations utilisateur connecté


---

## ⚠️ CE QUI RESTE À FAIRE

### 1. VUES UTILISATEUR 

On doit créer les vues suivantes: 

#### **Vues pour les activités:**
- `src/view/activite/creer_activite_vue.py` - Créer une activité avec upload GPX
- `src/view/activite/liste_activites_vue.py` - Lister ses activités
- `src/view/activite/detail_activite_vue.py` - Voir détails d'une activité
- `src/view/activite/modifier_activite_vue.py` - Modifier une activité

#### **Vues sociales:**
- `src/view/fil_actualite_vue.py` - Afficher le fil d'actualités
- `src/view/profil_vue.py` - Afficher le profil utilisateur
- `src/view/statistiques_vue.py` - Afficher les statistiques
- `src/view/followers_vue.py` - Gérer followers/following
- `src/view/recherche_utilisateurs_vue.py` - Rechercher des utilisateurs

#### **Vues d'interaction:**
- Intégrer les likes/commentaires dans les vues d'activités

### 2. INTÉGRATION DE LA SÉCURITÉ 

- Modifier `src/service/utilisateur_service.py` pour utiliser `hash_password_bcrypt()`
- Modifier `src/dao/utilisateur_dao.py` pour utiliser `verify_password_bcrypt()`
- Mettre à jour les vues d'inscription pour valider la force du mot de passe
- Ajouter la validation des entrées avec `sanitize_input()`

### 3. CONNEXION MENU UTILISATEUR 

- Modifier `src/view/menu_utilisateur_vue.py` pour intégrer toutes les nouvelles vues
- Créer le système de navigation cohérent

### 4. TESTS 
Créer des tests pour les nouveaux fichiers:
- `src/tests/test_dao/test_like_dao.py`
- `src/tests/test_dao/test_suivi_dao.py`
- `src/tests/test_dao/test_commentaire_dao.py`
- `src/tests/test_service/test_activity_service.py`
- `src/tests/test_service/test_like_service.py`

### Env pour db_connection
### il faut dans le code connecter à la base de données pour les endpoints api (user activités, comme la liste actuelle)