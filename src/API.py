import secrets

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

        # ✅ Vérifie si l'utilisateur courant (authentifié) existe toujours
        current = utilisateur_service.trouver_par_id(current_user["id"])
        if not current:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Utilisateur courant invalide ou supprimé",
            )

        # ✅ Vérifie si le profil demandé existe dans la base
        user = utilisateur_service.trouver_par_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Utilisateur avec l'id {user_id} introuvable",
            )

        # Récupère les followers et followings
        followers = suivi_service.get_followers(user_id)
        following = suivi_service.get_following(user_id)

        # ✅ Construit la réponse finale
        return {
            "id": user.id_user,
            "username": user.nom_user,
            "email": user.mail_user,
            "followers_count": len(followers),
            "following_count": len(following),
            "followers": [{"id": f.id_user, "username": f.nom_user} for f in followers],
            "following": [{"id": f.id_user, "username": f.nom_user} for f in following],
        }

    except HTTPException:
        # On relance les exceptions HTTP définies ci-dessus
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne : {e}")


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


# ============================================================================
# ENDPOINTS ACTIVITÉS
# ============================================================================


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


@app.get("/health")
def health_check():
    """Vérifie l'état de santé de l'API"""
    return {"status": "healthy", "service": "Striv API"}


@app.get("/test/complete-workflow")
def test_complete_workflow(current_user: dict = Depends(get_current_user)):
    """
    Endpoint de test complet qui teste plusieurs fonctionnalités de l'application

    Ce endpoint teste :
    - La récupération du profil utilisateur
    - Les statistiques
    - Les activités
    - Le fil d'actualités
    - Les likes et commentaires
    """
    try:
        user_id = current_user["id"]
        results = {
            "test_name": "Complete Workflow Test",
            "user_tested": current_user["username"],
            "tests": {},
        }

        # Test 1: Récupération du profil
        try:
            utilisateur_service = UtilisateurService()
            suivi_service = SuiviService()

            user = utilisateur_service.trouver_par_id(user_id)
            followers = suivi_service.get_followers(user_id)
            following = suivi_service.get_following(user_id)

            results["tests"]["profil"] = {
                "status": "SUCCESS",
                "data": {
                    "username": user.nom_user if user else None,
                    "followers_count": len(followers),
                    "following_count": len(following),
                },
            }
        except Exception as e:
            results["tests"]["profil"] = {"status": "FAILED", "error": str(e)}

        # Test 2: Statistiques utilisateur
        try:
            stats_service = StatistiquesService()
            stats = stats_service.get_statistiques_globales(user_id)

            results["tests"]["statistiques"] = {
                "status": "SUCCESS",
                "data": stats if stats else "No statistics available",
            }
        except Exception as e:
            results["tests"]["statistiques"] = {"status": "FAILED", "error": str(e)}

        # Test 3: Activités de l'utilisateur
        try:
            activity_service = ActivityService()
            activities = activity_service.get_activites_by_user(user_id)

            results["tests"]["activites"] = {
                "status": "SUCCESS",
                "data": {"count": len(activities), "activities_found": len(activities) > 0},
            }
        except Exception as e:
            results["tests"]["activites"] = {"status": "FAILED", "error": str(e)}

        # Test 4: Fil d'actualités
        try:
            feed = activity_service.get_feed(user_id)

            results["tests"]["feed"] = {
                "status": "SUCCESS",
                "data": {"count": len(feed), "feed_working": True},
            }
        except Exception as e:
            results["tests"]["feed"] = {"status": "FAILED", "error": str(e)}

        # Calculer le résultat global
        total_tests = len(results["tests"])
        successful_tests = sum(
            1 for test in results["tests"].values() if test["status"] == "SUCCESS"
        )

        results["summary"] = {
            "total_tests": total_tests,
            "successful": successful_tests,
            "failed": total_tests - successful_tests,
            "success_rate": f"{(successful_tests / total_tests) * 100:.2f}%",
        }

        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test failed: {str(e)}")


# ============================================================================
# LANCEMENT DE L'APPLICATION
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
