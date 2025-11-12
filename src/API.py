import secrets
import gpxpy
from fastapi import Depends, FastAPI, HTTPException, status, UploadFile, File
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import RedirectResponse
from datetime import time, datetime, date
import logging
import hashlib # Added for password hashing

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- DAO & Business Object Imports ---
# Assuming these service imports work and their classes handle database interaction
from service.utilisateur_service import UtilisateurService
from service.activity_service import ActivityService
from service.commentaire_service import CommentaireService
from service.like_service import LikeService

try:
    # 1. FIX: Import all necessary components from activite_model
    from dao.models.activite_model import ActivityModel, Base, engine, SessionLocal

    # 2. NEW/FIX: Import all other model files to ensure their Mappers are loaded!
    # These imports are CRITICAL for resolving Foreign Key errors.
    import dao.models.utilisateur_model
    import dao.models.commentaire_model
    # Assuming you have a file for likes as well:
    import dao.models.like_model

    # Import Business Objects
    from business_object.user_object.utilisateur import Utilisateur
    from business_object.like_comment_object.like import Like
    from business_object.like_comment_object.commentaire import Commentaire

    # 3. FIX: Create all tables based on Base metadata *before* server starts
    print(Base.metadata.tables.keys())
    Base.metadata.create_all(bind=engine)

    logger.info("SQLAlchemy Mappers loaded and database initialized successfully.")
except ImportError as e:
    logger.error(f"ATTENTION: Failed to load all SQLAlchemy models: {e}")
    # Re-raise the error to stop server startup if critical models aren't loaded
    raise

# --- FastAPI Initialization ---
app = FastAPI(title="Striv API - Application de sport connectée", root_path="/proxy/8000")
security = HTTPBasic()

# --- Utility Functions ---

def parse_strava_gpx(content):
    gpx = gpxpy.parse(content)
    distance_m = gpx.length_3d()
    duration_s = gpx.get_duration()
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

def convert_to_time(duree):
    if duree is None:
        return None
    hours = int(duree)
    minutes = int((duree - hours) * 60)
    return time(hours, minutes)

# --- API Endpoints ---

@app.get("/")
def root():
    return RedirectResponse(url="/docs")

@app.post("/login")
def login(username: str, password: str):
    user_service = UtilisateurService()
    user = user_service.se_connecter(nom_user=username, mdp=password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Nom d'utilisateur ou mot de passe incorrect")
    return {
        "message": "Connexion réussie",
        "user": {
            "id": user.id_user,
            "username": user.nom_user,
            "email": user.mail_user,
        }
    }

@app.post("/users")
def create_user(nom_user: str, mail_user: str, mdp: str):
    utilisateur_service = UtilisateurService()

    if utilisateur_service.nom_user_deja_utilise(nom_user):
        raise HTTPException(status_code=400, detail="Ce nom d'utilisateur est déjà utilisé")
    if not nom_user or len(nom_user.strip()) == 0:
        raise HTTPException(status_code=400, detail="Le nom d'utilisateur ne peut pas être vide")
    if not mail_user or "@" not in mail_user:
        raise HTTPException(status_code=400, detail="Email invalide")
    if not mdp or len(mdp) < 4:
        raise HTTPException(status_code=400, detail="Le mot de passe doit contenir au moins 4 caractères")

    nouvel_utilisateur = utilisateur_service.creer(nom_user=nom_user, mail_user=mail_user, mdp=mdp)

    if not nouvel_utilisateur:
        raise HTTPException(status_code=500, detail="Erreur lors de la création de l'utilisateur")
    return {"message": "Utilisateur créé avec succès", "user": nouvel_utilisateur}

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    user_service = UtilisateurService()
    user = user_service.se_connecter(nom_user=credentials.username, mdp=credentials.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Identifiants invalides", headers={"WWW-Authenticate": "Basic"})
    return {"id": user.id_user, "username": user.nom_user, "email": user.mail_user}

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
    if gpx_file:
        content = await gpx_file.read()
        gpx_data = parse_strava_gpx(content)
        titre = titre or gpx_data.get("nom") or "Activité importée"
        sport = sport or gpx_data.get("type") or "course"
        distance = distance if distance is not None else gpx_data.get("distance totale (km)")
        duree = duree if duree is not None else gpx_data.get("temps en mouvement (min)")
        if not date_activite:
            date_obj = date.today()
        else:
            try:
                date_obj = datetime.strptime(date_activite, "%Y-%m-%d").date()
            except ValueError:
                raise HTTPException(status_code=400, detail="Format de date invalide. Utilisez YYYY-MM-DD")
    else:
        if not all([titre, sport, date_activite, distance]):
            raise HTTPException(status_code=400, detail="Les champs titre, sport, date_activite et distance sont obligatoires en mode manuel")
        try:
            date_obj = datetime.strptime(date_activite, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Format de date invalide. Utilisez YYYY-MM-DD")

    sports_valides = ["course", "cyclisme", "natation", "randonnee"]
    if sport not in sports_valides:
        raise HTTPException(status_code=400, detail=f"Type de sport invalide. Valeurs acceptées: {', '.join(sports_valides)}")

    if distance is None or distance <= 0:
        raise HTTPException(status_code=400, detail="La distance doit être positive")
    if duree is not None and duree <= 0:
        raise HTTPException(status_code=400, detail="La durée doit être positive")

    duree_formatee = convert_to_time(duree)

    activity_data = {
        "titre": titre,
        "description": description or "",
        "sport": sport,
        "date_activite": date_obj,
        "lieu": lieu or "",
        "distance": distance,
        "duree": duree_formatee,
        "id_user": current_user["id"]
    }

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
            "duree": str(duree_formatee),
            "lieu": lieu,
        },
    }

@app.get("/activities/{activity_id}")
def get_activity(activity_id: int, current_user: dict = Depends(get_current_user)):
    activity_service = ActivityService()
    activity = activity_service.get_activite_by_id(activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {
        "id": activity.id,
        "titre": getattr(activity, "titre", None),
        "description": getattr(activity, "description", None),
        "sport": getattr(activity, "sport", None),
        "distance": getattr(activity, "distance", None),
        "duree": str(getattr(activity, "duree", None)),
        "date_activite": activity.date_activite.isoformat() if hasattr(activity, "date_activite") else None,
        "lieu": getattr(activity, "lieu", None),
        "id_user": getattr(activity, "id_user", None),
    }

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

@app.post("/activities/{activity_id}/comment")
def comment_activity(activity_id: int, contenu: str, current_user: dict = Depends(get_current_user)):
    commentaire_service = CommentaireService()
    user_id = current_user["id"]
    success = commentaire_service.creer_commentaire(user_id, activity_id, contenu)
    if not success:
        # Changed status code to 500 for internal DB failure
        raise HTTPException(status_code=500, detail="Erreur interne lors de la création du commentaire")
    return {"message": f"Comment added to activity {activity_id}"}

@app.post("/activities/{activity_id}/like")
def like_activity(activity_id: int, current_user: dict = Depends(get_current_user)):
    like_service = LikeService()
    activity_service = ActivityService()
    user_id = current_user["id"]
    activity = activity_service.get_activite_by_id(activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    existing_likes = like_service.get_likes_activite(activity_id)
    if any(like.id_user == user_id for like in existing_likes):
        return {"message": f"Activity {activity_id} already liked", "already_liked": True}
    success = like_service.liker_activite(user_id, activity_id)
    if not success:
        raise HTTPException(status_code=500, detail="Cannot like activity")
    return {"message": f"Activity {activity_id} liked successfully", "already_liked": False}

@app.delete("/activities/{activity_id}/like")
def unlike_activity(activity_id: int, current_user: dict = Depends(get_current_user)):
    like_service = LikeService()
    user_id = current_user["id"]
    success = like_service.unliker_activite(user_id, activity_id)
    if not success:
        raise HTTPException(status_code=404, detail="Like not found")
    return {"message": f"Like removed from activity {activity_id}"}

@app.get("/activities/{activity_id}/likes")
def get_activity_likes(activity_id: int, current_user: dict = Depends(get_current_user)):
    like_service = LikeService()
    likes = like_service.get_likes_activite(activity_id)
    count = like_service.count_likes_activite(activity_id)
    return {
        "activity_id": activity_id,
        "likes_count": count,
        "likes": [
            {
                "id_user": like.id_user,
                "date_like": like.date_like.isoformat() if hasattr(like.date_like, "isoformat") else str(like.date_like),
            }
            for like in likes
        ],
    }

@app.post("/upload-gpx")
async def upload_gpx(file: UploadFile = File(...)):
    content = await file.read()
    return parse_strava_gpx(content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)