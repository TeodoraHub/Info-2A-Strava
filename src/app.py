
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import List, Dict, Optional
from datetime import datetime
import secrets

# Tes DAO et services (à importer depuis tes fichiers)
from dao import UtilisateurDAO, ActivityDAO
from service import ActivityService

app = FastAPI(title="Striv API")
security = HTTPBasic()

# Mock de base de données (à remplacer par ta vraie session SQLAlchemy)
def get_db():
    # Ici, tu devrais retourner une session SQLAlchemy réelle
    # Exemple : yield SessionLocal()
    pass

# Authentification basique (comme dans ton code)
USERS = {
    "alice": {"password": "wonderland", "roles": ["admin"], "id": 1},
    "bob": {"password": "builder", "roles": ["user"], "id": 2},
}

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    user = USERS.get(username)
    if not user or not secrets.compare_digest(password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return user

@app.get("/users/{user_id}/profil")
def get_profil(
    user_id: int,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Retourne le profil d'un utilisateur, ses followers et ses suivis.
    """
    user_dao = UtilisateurDAO(db)
    user = user_dao.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    followers = user_dao.get_followers(user_id)
    following = user_dao.get_following(user_id)

    return {
        "username": user.username,
        "email": user.email,
        "followers": [{"id": f.id, "username": f.username} for f in followers],
        "following": [{"id": f.id, "username": f.username} for f in following],
    }

@app.get("/f1")
def me(user = Depends(get_current_user)):
    return {"user": user}
# ----------------------------------------------------------


# Jamais de DAO dans les méthodes des objets métiers
# Les services orchestrent l'utilisation des objets métiers et de la DAO
# On peut aussi se passer des services et orchestrer directement dans le endpoint

@app.get("/users/{user_id}/activities")
def get_activities(
    user_id: int,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Retourne la liste des activités d'un utilisateur.
    """
    activity_dao = ActivityDAO(db)
    activities = activity_dao.get_by_user(user_id)
    return [
        {
            "id": a.id,
            "type": a.type,
            "distance": a.distance,
            "duration": a.duration,
            "date": a.date.isoformat(),
        }
        for a in activities
    ]

from datetime import datetime, timedelta

def get_last_month_year():
    today = datetime.now()
    first_day_of_current_month = today.replace(day=1)
    last_day_of_last_month = first_day_of_current_month - timedelta(days=1)
    return last_day_of_last_month.year, last_day_of_last_month.month

def get_monthly_stats(self, user_id: int):
    # Récupère l'année et le mois précédents
    year, month = get_last_month_year()

    # Récupère les activités de l'utilisateur
    activities = self.activity_dao.get_by_user(user_id)

    # Filtre les activités du mois précédent
    monthly_activities = [
        a for a in activities
        if a.date.year == year and a.date.month == month
    ]

    # Calcule les statistiques
    total_distance = sum(a.distance for a in monthly_activities)
    total_duration = sum(a.duration for a in monthly_activities)

    return {
        "year": year,
        "month": month,
        "total_distance": total_distance,
        "total_duration": total_duration,
        "activities_count": len(monthly_activities),
    }


@app.get("/users/{user_id}/feed")
def get_feed(
    user_id: int,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Retourne le fil d'activités de l'utilisateur et des personnes qu'il suit.
    """
    activity_service = ActivityService(db)
    feed = activity_service.get_feed(user_id)
    return [
        {
            "id": a.id,
            "user_id": a.user_id,
            "type": a.type,
            "distance": a.distance,
            "duration": a.duration,
            "date": a.date.isoformat(),
        }
        for a in feed
    ]

@app.post("users/{user_id}/activities")
def create_activity(user_id):
    user = UtilisateurDAO().get(user_id)
    activity = user.create_activity()
    AcitivityDAO().save(activity)
    # OU
    # UtilisateurService().create_activity(user_id)

@app.post("/users/{user_id}/follow/{target_user_id}")
def follow_user(
    user_id: int,
    target_user_id: int,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Permet à un utilisateur de suivre un autre utilisateur.
    """
    user_dao = UtilisateurDAO(db)
    success = user_dao.follow(user_id, target_user_id)
    if not success:
        raise HTTPException(status_code=400, detail="Already following or user not found")
    return {"message": f"User {user_id} now follows user {target_user_id}"}

@app.get("/users/{user_id}/feed")
def get_feed(
    user_id: int,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Retourne le fil d'activités de l'utilisateur et des personnes qu'il suit.
    """
    activity_service = ActivityService(db)
    feed = activity_service.get_feed(user_id)
    return [
        {
            "id": a.id,
            "user_id": a.user_id,
            "type": a.type,
            "distance": a.distance,
            "duration": a.duration,
            "date": a.date.isoformat(),
        }
        for a in feed
    ]

    