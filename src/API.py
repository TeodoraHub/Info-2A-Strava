import secrets
import gpxpy
from service.commentaire_service import CommentaireService
from fastapi import Depends, FastAPI, HTTPException, status, UploadFile, File
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from service.utilisateur_service import UtilisateurService
from datetime import time
# Imports des services
from service.activity_service import ActivityService
from service.commentaire_service import CommentaireService
from service.like_service import LikeService

app = FastAPI(title="Striv API - Application de sport connectée", root_path="/proxy/8001")
security = HTTPBasic()


def parse_strava_gpx(content):
    """Parse un fichier GPX et extrait les données principales."""
    gpx = gpxpy.parse(content)
    # Distance totale en 3D (mètres)
    distance_m = gpx.length_3d()
    # Durée totale (secondes)
    duration_s = gpx.get_duration()
    # Temps/distance/vitesse en mouvement
    moving = gpx.get_moving_data()
    return {
        "nom": gpx.tracks[0].name if gpx.tracks else None,
        "type": gpx.tracks[0].type if gpx.tracks else None,
        "distance totale (km)": distance_m/1000,
        "durée totale (min)": duration_s/60,
        "temps en mouvement (min)": moving.moving_time/60,
        "distance en mouvement (km)": moving.moving_distance/1000,
        "vitesse moyenne (km/h)": (moving.moving_distance/moving.moving_time)*3.6 if moving.moving_time > 0 else 0,
        "vitesse max (km/h)": moving.max_speed*3.6
    }


# ============================================================================
# AUTHENTIFICATION
# ============================================================================

# ATTENTION: Ceci est une authentification basique pour le développement
# En production, utiliser JWT tokens et base de données réelle

@app.post("/login")
def login(username: str, password: str):
    """
    Authentifie un utilisateur via paramètres simples :
    """

    user_service = UtilisateurService()

    user = user_service.se_connecter(
        nom_user=username,
        mdp=password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur ou mot de passe incorrect"
        )

    return {
        "message": "Connexion réussie",
        "user": {
            "id": user.id_user,
            "username": user.nom_user,
            "email": user.mail_user,
        }
    }


# ============================================================================
# ENDPOINTS UTILISATEURS
# ============================================================================


@app.post("/users")
def create_user(nom_user: str, mail_user: str, mdp: str):
    """Créer un nouvel utilisateur

    Parameters:
    - nom_user: Nom d'utilisateur (unique)
    - mail_user: Email de l'utilisateur
    - mdp: Mot de passe
    """
    try:
        from service.utilisateur_service import UtilisateurService

        utilisateur_service = UtilisateurService()

        # Vérifier que le nom d'utilisateur n'existe pas déjà
        if utilisateur_service.nom_user_deja_utilise(nom_user):
            raise HTTPException(status_code=400, detail="Ce nom d'utilisateur est déjà utilisé")

        # Validation basique
        if not nom_user or len(nom_user.strip()) == 0:
            raise HTTPException(
                status_code=400, detail="Le nom d'utilisateur ne peut pas être vide"
            )

        if not mail_user or "@" not in mail_user:
            raise HTTPException(status_code=400, detail="Email invalide")

        if not mdp or len(mdp) < 4:
            raise HTTPException(
                status_code=400, detail="Le mot de passe doit contenir au moins 4 caractères"
            )

        # Créer l'utilisateur (id_user=None car auto-généré par la base)
        nouvel_utilisateur = utilisateur_service.creer(nom_user=nom_user, mail_user=mail_user, mdp=mdp)

        if not nouvel_utilisateur:
            raise HTTPException(status_code=500, detail="Erreur lors de la création de l'utilisateur")

        return {"message": "Utilisateur créé avec succès","user": nouvel_utilisateur}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création: {str(e)}")


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Authentifie un utilisateur via Authorization: Basic ... sur chaque requête
    """
    user_service = UtilisateurService()

    user = user_service.se_connecter(
        nom_user=credentials.username,
        mdp=credentials.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides",
            headers={"WWW-Authenticate": "Basic"},
        )

    return {
        "id": user.id_user,
        "username": user.nom_user,
        "email": user.mail_user
    }






# ============================================================================
# ENDPOINTS ACTIVITÉS
# ============================================================================
def convert_to_time(duree):
    """Convertir la durée en heures décimales (ex: 5.5) en un objet `time`."""
    if duree is None:
        return None
    hours = int(duree)  # Récupérer la partie entière (heures)
    minutes = int((duree - hours) * 60)  # Convertir la partie décimale en minutes
    return time(hours, minutes)

@app.post("/activities")
async def create_activity(
    titre: str = None,
    description: str = None,
    sport: str = None,
    date_activite: str = None,
    lieu: str = None,
    distance: float = None,
    duree: float = None,
    gpx_file: UploadFile = File(None),
    current_user: dict = Depends(get_current_user),
):
    """Créer une nouvelle activité (manuellement ou via fichier GPX)"""
    try:
        from datetime import datetime, date

        # Si un fichier GPX est fourni, on extrait les données
        if gpx_file:
            content = await gpx_file.read()
            gpx_data = parse_strava_gpx(content)
            
            # Utiliser les données du GPX comme valeurs par défaut
            # Les paramètres fournis manuellement ont la priorité
            titre = titre or gpx_data.get("nom") or "Activité importée"
            sport = sport or gpx_data.get("type") or "course"
            distance = distance if distance is not None else gpx_data.get("distance totale (km)")
            duree = duree if duree is not None else gpx_data.get("temps en mouvement (min)")

            # Si pas de date fournie, utiliser la date du jour
            if not date_activite:
                date_obj = date.today()
            else:
                try:
                    date_obj = datetime.strptime(date_activite, "%Y-%m-%d").date()
                except ValueError:
                    raise HTTPException(
                        status_code=400, detail="Format de date invalide. Utilisez YYYY-MM-DD"
                    )
        else:
            # Mode manuel : tous les champs sont obligatoires
            if not all([titre, sport, date_activite, distance]):
                raise HTTPException(
                    status_code=400,
                    detail="Les champs titre, sport, date_activite et distance sont obligatoires en mode manuel"
                )
            
            # Conversion de la date
            try:
                date_obj = datetime.strptime(date_activite, "%Y-%m-%d").date()
            except ValueError:
                raise HTTPException(
                    status_code=400, detail="Format de date invalide. Utilisez YYYY-MM-DD"
                )

        # Validation du type de sport
        sports_valides = ["course", "cyclisme", "natation", "randonnee"]
        if sport not in sports_valides:
            raise HTTPException(
                status_code=400,
                detail=f"Type de sport invalide. Valeurs acceptées: {', '.join(sports_valides)}",
            )

        # Validation des valeurs numériques
        if distance is None or distance <= 0:
            raise HTTPException(status_code=400, detail="La distance doit être positive")
        if duree is not None and duree <= 0:
            raise HTTPException(status_code=400, detail="La durée doit être positive")

        # Convertir la durée en `time` avant de l'ajouter à l'activité
        duree_formatee = convert_to_time(duree)

        # Création d'un dictionnaire au lieu d'objets métier
        activity_data = {
            "titre": titre,
            "description": description or "",
            "sport": sport,
            "date_activite": date_obj,
            "lieu": lieu or "",
            "distance": distance,
            "duree": duree_formatee,  # Utilisation de la durée formatée en `time`
            "id_user": current_user["id"]
        }

        # Enregistrement de l'activité
        activity_service = ActivityService()
        success = activity_service.creer_activite_from_dict(activity_data)
        
        if not success:
            raise HTTPException(status_code=500, detail="Erreur lors de la création de l'activité")

        return {
            "message": "Activité créée avec succès",
            "activity": {
                "titre": titre,
                "sport": sport,
                "date_activite": date_obj.isoformat(),
                "distance": distance,
                "duree": str(duree_formatee),  # On affiche la durée au format 'HH:MM:00'
                "lieu": lieu,
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création: {str(e)}")

@app.get("/activities/{activity_id}")
def get_activity(activity_id: int, current_user: dict = Depends(get_current_user)):
    """Récupère les détails d'une activité"""
    try:
        activity_service = ActivityService()
        activity = activity_service.get_activite_by_id(activity_id)
        print(activity)
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")

        return {
            "id": activity.id,
            "titre": activity.titre if hasattr(activity, "titre") else None,
            "description": activity.description if hasattr(activity, "description") else None,
            "sport": activity.sport if hasattr(activity, "sport") else None,
            "distance": activity.distance if hasattr(activity, "distance") else None,
            "duree": str(activity.duree) if hasattr(activity, "duree") else None,
            "date_activite": activity.date_activite.isoformat()
            if hasattr(activity, "date_activite")
            else None,
            "lieu": activity.lieu if hasattr(activity, "lieu") else None,
            "id_user": activity.id_user if hasattr(activity, "id_user") else None,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/activities/{activity_id}")
def delete_activity(activity_id: int, current_user: dict = Depends(get_current_user)):
    activity_service = ActivityService()
    activity = activity_service.get_activite_by_id(activity_id)

    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    if activity.id_user != current_user["id"]:
        raise HTTPException(status_code=403, detail="Vous n'êtes pas le propriétaire de cette activité")

    success = activity_service.supprimer_activite(activity_id)
    if not success:
        raise HTTPException(status_code=500, detail="Impossible de supprimer l'activité")

    return {"message": f"Activité {activity_id} supprimée avec succès"}



# ============================================================================
# ENDPOINTS COMMENTAIRES
# ============================================================================


@app.post("/activities/{activity_id}/comment")
def comment_activity(
    activity_id: int, contenu: str, current_user: dict = Depends(get_current_user)
):
    """Commenter une activité"""
    try:
        commentaire_service = CommentaireService()
        user_id = current_user["id"]

        success = commentaire_service.creer_commentaire(user_id, activity_id, contenu)
        print(success)
        if not success:
            raise HTTPException(status_code=400, detail="Cannot create comment")

        return {"message": f"Comment added to activity {activity_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# ============================================================================
# ENDPOINTS LIKES
# ============================================================================


@app.post("/activities/{activity_id}/like")
def like_activity(activity_id: int, current_user: dict = Depends(get_current_user)):
    """Liker une activité"""
    try:
        like_service = LikeService()
        activity_service = ActivityService()
        user_id = current_user["id"]

        # 1. Vérifier si l'activité existe
        activity = activity_service.get_activite_by_id(activity_id)
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")

        # 2. Vérifier si déjà liké
        existing_likes = like_service.get_likes_activite(activity_id)
        already_liked = any(like.id_user == user_id for like in existing_likes)
        
        if already_liked:
            return {
                "message": f"Activity {activity_id} already liked",
                "already_liked": True
            }

        # 3. Liker l'activité
        success = like_service.liker_activite(user_id, activity_id)
        
        if not success:
            # Ceci attrape le cas où le service retourne False (échec DAO/DB)
            raise HTTPException(status_code=500, detail="Cannot like activity")

        return {
            "message": f"Activity {activity_id} liked successfully",
            "already_liked": False
        }
    except HTTPException:
        raise
    except Exception as e:
        # Ceci attrape les erreurs non gérées dans les services (la cause du 500 dans vos logs)
        print(f"Erreur critique lors du like de l'activité {activity_id}: {e}")
        # Optionnel: traceback.print_exc() ici pour le débogage
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")


@app.delete("/activities/{activity_id}/like")
def unlike_activity(activity_id: int, current_user: dict = Depends(get_current_user)):
    """Retirer un like d'une activité"""
    try:
        like_service = LikeService()
        user_id = current_user["id"]

        success = like_service.unliker_activite(user_id, activity_id)
        if not success:
            raise HTTPException(status_code=404, detail="Like not found")

        return {"message": f"Like removed from activity {activity_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/activities/{activity_id}/likes")
def get_activity_likes(activity_id: int, current_user: dict = Depends(get_current_user)):
    """Récupère les likes d'une activité"""
    try:
        like_service = LikeService()
        likes = like_service.get_likes_activite(activity_id)
        count = like_service.count_likes_activite(activity_id)

        return {
            "activity_id": activity_id,
            "likes_count": count,
            "likes": [
                {
                    "id_user": like.id_user,
                    "date_like": like.date_like.isoformat()
                    if hasattr(like.date_like, "isoformat")
                    else str(like.date_like),
                }
                for like in likes
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ENDPOINTS ParserGPX
# ============================================================================



@app.post("/upload-gpx")
async def upload_gpx(file: UploadFile = File(...)):
    # Lecture du contenu du fichier (texte)
    content = await file.read()
    # Parsing
    return parse_strava_gpx(content)

# ============================================================================
# LANCEMENT DE L'APPLICATION
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
