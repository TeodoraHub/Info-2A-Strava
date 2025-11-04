import secrets
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# Imports des services
from service.activity_service import ActivityService
from service.commentaire_service import CommentaireService
from service.like_service import LikeService
from service.statistiques_service import StatistiquesService
from service.suivi_service import SuiviService
from service.utilisateur_service import UtilisateurService

app = FastAPI(title="Striv API - Application de sport connectée",root_path="/proxy/8000")
security = HTTPBasic()

# ============================================================================
# AUTHENTIFICATION
# ============================================================================

# ATTENTION: Ceci est une authentification basique pour le développement
# En production, utiliser JWT tokens et base de données réelle
USERS = {
    "alice": {"password": "wonderland", "roles": ["admin"], "id": 1},
    "bob": {"password": "builder", "roles": ["user"], "id": 2},
}


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


@app.get("/users/{user_id}/profil")
def get_profil(user_id: int, current_user: dict = Depends(get_current_user)):
    """Récupère le profil d'un utilisateur avec ses followers et following"""
    try:
        utilisateur_service = UtilisateurService()
        suivi_service = SuiviService()

        user = utilisateur_service.trouver_par_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        followers = suivi_service.get_followers(user_id)
        following = suivi_service.get_following(user_id)

        return {
            "id": user.id_user,
            "username": user.nom_user,
            "email": user.mail_user,
            "followers_count": len(followers),
            "following_count": len(following),
            "followers": [{"id": f.id_user, "username": f.nom_user} for f in followers],
            "following": [{"id": f.id_user, "username": f.nom_user} for f in following],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/users/{user_id}/follow/{target_user_id}")
def follow_user(user_id: int, target_user_id: int, current_user: dict = Depends(get_current_user)):
    """Permet à un utilisateur de suivre un autre utilisateur"""
    try:
        suivi_service = SuiviService()
        success = suivi_service.suivre_utilisateur(user_id, target_user_id)
        if not success:
            raise HTTPException(
                status_code=400, detail="Cannot follow user (already following or invalid users)"
            )
        return {"message": f"User {user_id} now follows user {target_user_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/users/{user_id}/follow/{target_user_id}")
def unfollow_user(
    user_id: int, target_user_id: int, current_user: dict = Depends(get_current_user)
):
    """Permet à un utilisateur de ne plus suivre un autre utilisateur"""
    try:
        suivi_service = SuiviService()
        success = suivi_service.ne_plus_suivre(user_id, target_user_id)
        if not success:
            raise HTTPException(status_code=400, detail="Cannot unfollow user")
        return {"message": f"User {user_id} unfollowed user {target_user_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users/{user_id}/statistics")
def get_user_statistics(
    user_id: int, period: str = "global", current_user: dict = Depends(get_current_user)
):
    """Récupère les statistiques d'un utilisateur

    Parameters:
    - period: 'monthly', 'yearly', or 'global' (default)
    """
    try:
        stats_service = StatistiquesService()

        if period == "monthly":
            stats = stats_service.get_statistiques_mensuelles(user_id)
        elif period == "yearly":
            stats = stats_service.get_statistiques_annuelles(user_id)
        else:
            stats = stats_service.get_statistiques_globales(user_id)

        if not stats:
            raise HTTPException(status_code=404, detail="Statistics not found")

        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ENDPOINTS ACTIVITÉS
# ============================================================================


@app.get("/users/{user_id}/activities")
def get_user_activities(
    user_id: int,
    type_activite: Optional[str] = None,
    current_user: dict = Depends(get_current_user),
):
    """Récupère toutes les activités d'un utilisateur"""
    try:
        activity_service = ActivityService()
        activities = activity_service.get_activites_by_user(user_id, type_activite)

        return [
            {
                "id": a.id,
                "titre": a.titre if hasattr(a, "titre") else None,
                "sport": a.sport if hasattr(a, "sport") else None,
                "distance": a.distance if hasattr(a, "distance") else None,
                "duree": str(a.duree) if hasattr(a, "duree") else None,
                "date_activite": a.date_activite.isoformat()
                if hasattr(a, "date_activite")
                else None,
                "id_user": a.id_user if hasattr(a, "id_user") else None,
            }
            for a in activities
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users/{user_id}/feed")
def get_feed(user_id: int, current_user: dict = Depends(get_current_user)):
    """Récupère le fil d'actualités d'un utilisateur (ses activités + celles qu'il suit)"""
    try:
        activity_service = ActivityService()
        feed = activity_service.get_feed(user_id)

        return [
            {
                "id": a.id,
                "titre": a.titre if hasattr(a, "titre") else None,
                "sport": a.sport if hasattr(a, "sport") else None,
                "distance": a.distance if hasattr(a, "distance") else None,
                "duree": str(a.duree) if hasattr(a, "duree") else None,
                "date_activite": a.date_activite.isoformat()
                if hasattr(a, "date_activite")
                else None,
                "id_user": a.id_user if hasattr(a, "id_user") else None,
            }
            for a in feed
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
# ENDPOINTS LIKES
# ============================================================================


@app.post("/activities/{activity_id}/like")
def like_activity(activity_id: int, current_user: dict = Depends(get_current_user)):
    """Liker une activité"""
    try:
        like_service = LikeService()
        user_id = current_user["id"]

        success = like_service.liker_activite(user_id, activity_id)
        if not success:
            raise HTTPException(status_code=400, detail="Cannot like activity (already liked)")

        return {"message": f"Activity {activity_id} liked successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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


@app.get("/activities/{activity_id}/comments")
def get_activity_comments(activity_id: int, current_user: dict = Depends(get_current_user)):
    """Récupère les commentaires d'une activité"""
    try:
        commentaire_service = CommentaireService()
        comments = commentaire_service.get_commentaires_activite(activity_id)
        count = commentaire_service.count_commentaires_activite(activity_id)

        return {
            "activity_id": activity_id,
            "comments_count": count,
            "comments": [
                {
                    "id_comment": comment.id_comment,
                    "id_user": comment.id_user,
                    "contenu": comment.contenu,
                    "date_comment": comment.date_commentaire.isoformat()
                    if hasattr(comment.date_commentaire, "isoformat")
                    else str(comment.date_commentaire),
                }
                for comment in comments
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, current_user: dict = Depends(get_current_user)):
    """Supprime un commentaire"""
    try:
        commentaire_service = CommentaireService()
        success = commentaire_service.supprimer_commentaire(comment_id)

        if not success:
            raise HTTPException(status_code=404, detail="Comment not found")

        return {"message": f"Comment {comment_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ENDPOINT DE TEST
# ============================================================================


@app.get("/")
def root():
    """Endpoint racine de l'API"""
    return {
        "name": "Striv API",
        "version": "1.0.0",
        "description": "API pour l'application de sport connectée Striv",
    }


@app.get("/me")
def me(current_user: dict = Depends(get_current_user)):
    """Retourne les informations de l'utilisateur connecté"""
    return {"user": current_user}


# ============================================================================
# LANCEMENT DE L'APPLICATION
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
