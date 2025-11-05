import secrets
import gpxpy

from fastapi import Depends, FastAPI, HTTPException, status, UploadFile, File
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# Imports des services
from service.activity_service import ActivityService

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
USERS = {
    "alice": {"password": "wonderland", "roles": ["admin"], "id": 1},
    "bob": {"password": "builder", "roles": ["user"], "id": 2},
}
FAKE_ACTIVITIES = [
    {
        "id": 1,
        "titre": "Footing matinal",
        "description": "Course tranquille au parc",
        "sport": "course",
        "date_activite": "2025-11-01",
        "lieu": "Parc Central",
        "distance": 5.0,
        "duree": 0.5,
        "id_user": 1,
    },
    {
        "id": 2,
        "titre": "Balade à vélo",
        "description": "Tour de la ville en vélo",
        "sport": "cyclisme",
        "date_activite": "2025-11-03",
        "lieu": "Centre-ville",
        "distance": 20.0,
        "duree": 1.0,
        "id_user": 2,
    },
    {
        "id": 3,
        "titre": "Séance natation",
        "description": "Entraînement intensif 1000m",
        "sport": "natation",
        "date_activite": "2025-11-05",
        "lieu": "Piscine municipale",
        "distance": 1.0,
        "duree": 0.4,
        "id_user": 1,
    },
    {
        "id": 4,
        "titre": "Randonnée en montagne",
        "description": "Montée et descente du sentier rouge",
        "sport": "randonnee",
        "date_activite": "2025-11-07",
        "lieu": "Montagne Bleue",
        "distance": 10.0,
        "duree": 2.0,
        "id_user": 2,
    },
    {
        "id": 5,
        "titre": "Course rapide",
        "description": "Sprint sur 3 km",
        "sport": "course",
        "date_activite": "2025-11-09",
        "lieu": "Stade municipal",
        "distance": 3.0,
        "duree": 0.25,
        "id_user": 1,
    },
]


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    """Authentification basique de l'utilisateur"""
    username = credentials.username
    password = credentials.password
    user = USERS.get(username)
    if not user or not secrets.compare_digest(password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user


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








# ============================================================================
# ENDPOINTS ACTIVITÉS
# ============================================================================


@app.post("/activities")
def create_activity(
    titre: str,
    description: str,
    sport: str,
    date_activite: str,
    lieu: str,
    distance: float,
    duree: float = None,
    current_user: dict = Depends(get_current_user),
):
    """Créer une nouvelle activité

    Parameters:
    - titre: Titre de l'activité
    - description: Description de l'activité
    - sport: Type de sport (course, cyclisme, natation, randonnee)
    - date_activite: Date de l'activité au format YYYY-MM-DD
    - lieu: Lieu de l'activité
    - distance: Distance en km
    - duree: Durée en heures (optionnel)
    """
    try:
        from datetime import datetime

        from business_object.Activity_object.course_a_pieds import CoursePied
        from business_object.Activity_object.cyclisme import Cyclisme
        from business_object.Activity_object.natation import Natation
        from business_object.Activity_object.randonnee import Randonnee

        # Validation du type de sport
        sports_valides = ["course", "cyclisme", "natation", "randonnee"]
        if sport not in sports_valides:
            raise HTTPException(
                status_code=400,
                detail=f"Type de sport invalide. Valeurs acceptées: {', '.join(sports_valides)}",
            )

        # Conversion de la date
        try:
            date_obj = datetime.strptime(date_activite, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(
                status_code=400, detail="Format de date invalide. Utilisez YYYY-MM-DD"
            )

        # Validation des valeurs numériques
        if distance <= 0:
            raise HTTPException(status_code=400, detail="La distance doit être positive")
        if duree is not None and duree <= 0:
            raise HTTPException(status_code=400, detail="La durée doit être positive")

        # Création de l'activité selon le type
        user_id = current_user["id"]

        # Note: id_activite sera None car il sera auto-généré par la base de données
        if sport == "course":
            activity = CoursePied(
                id_activite=None,
                titre=titre,
                description=description,
                date_activite=date_obj,
                lieu=lieu,
                distance=distance,
                id_user=user_id,
                duree=duree,
            )
        elif sport == "cyclisme":
            activity = Cyclisme(
                id_activite=None,
                titre=titre,
                description=description,
                date_activite=date_obj,
                lieu=lieu,
                distance=distance,
                id_user=user_id,
                duree=duree,
            )
        elif sport == "natation":
            activity = Natation(
                id_activite=None,
                titre=titre,
                description=description,
                date_activite=date_obj,
                lieu=lieu,
                distance=distance,
                id_user=user_id,
                duree=duree,
            )
        elif sport == "randonnee":
            activity = Randonnee(
                id_activite=None,
                titre=titre,
                description=description,
                date_activite=date_obj,
                lieu=lieu,
                distance=distance,
                id_user=user_id,
                duree=duree,
            )

        # Enregistrement de l'activité
        activity_service = ActivityService()
        success = activity_service.creer_activite(activity)

        if not success:
            raise HTTPException(status_code=500, detail="Erreur lors de la création de l'activité")

        return {
            "message": "Activité créée avec succès",
            "activity": {
                "titre": activity.titre,
                "sport": activity.sport,
                "date_activite": activity.date_activite.isoformat(),
                "distance": activity.distance,
                "duree": activity.duree,
                "lieu": activity.lieu,
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
    """Supprime une activité"""
    try:
        activity_service = ActivityService()
        success = activity_service.supprimer_activite(activity_id)

        if not success:
            raise HTTPException(status_code=404, detail="Activity not found or cannot be deleted")

        return {"message": f"Activity {activity_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
        if not success:
            raise HTTPException(status_code=400, detail="Cannot create comment")

        return {"message": f"Comment added to activity {activity_id}"}
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
