from datetime import datetime
from typing import Any, Dict, Optional

import gpxpy
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from service.activity_service import ActivityService
from service.commentaire_service import CommentaireService
from service.like_service import LikeService
from service.statistiques_service import StatistiquesService
from service.utilisateur_service import UtilisateurService

app = FastAPI(title="Striv API - Application de sport connectee", root_path="/proxy/8000")
security = HTTPBasic()


def parse_strava_gpx(content: bytes) -> Dict[str, Any]:
    """Parse un fichier GPX et renvoie les donnees principales en km/h."""
    gpx = gpxpy.parse(content)
    distance_m = gpx.length_3d() or 0.0
    duration_s = gpx.get_duration() or 0.0
    moving = gpx.get_moving_data()
    moving_time_s = moving.moving_time if moving and moving.moving_time else 0.0
    moving_distance_m = moving.moving_distance if moving and moving.moving_distance else 0.0

    distance_km = round(distance_m / 1000, 3)
    duree_heures = round(duration_s / 3600, 3)
    temps_mouvement_heures = round(moving_time_s / 3600, 3)
    vitesse_moyenne = (moving_distance_m / moving_time_s) * 3.6 if moving_time_s > 0 else 0.0
    vitesse_max = moving.max_speed * 3.6 if moving and moving.max_speed else 0.0

    return {
        "nom": gpx.tracks[0].name if gpx.tracks else None,
        "type": gpx.tracks[0].type if gpx.tracks else None,
        "distance_km": distance_km,
        "distance totale (km)": distance_km,
        "duree_heures": duree_heures,
        "duree totale (min)": round(duration_s / 60, 3),
        "temps_mouvement_heures": temps_mouvement_heures,
        "temps en mouvement (min)": round(moving_time_s / 60, 3),
        "distance en mouvement (km)": round(moving_distance_m / 1000, 3),
        "vitesse moyenne (km/h)": vitesse_moyenne,
        "vitesse max (km/h)": vitesse_max,
    }


def _parse_date(date_str: Optional[str]) -> datetime:
    if not date_str:
        return datetime.now()
    try:
        return datetime.fromisoformat(date_str)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail="Format de date invalide. Utilisez YYYY-MM-DD ou YYYY-MM-DDTHH:MM:SS",
        ) from exc


def _coerce_float(value: Any, field: str) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=f"{field} doit etre numerique") from exc


def _activity_to_dict(activity) -> Dict[str, Any]:
    identifier = getattr(activity, "id", None) or getattr(activity, "id_activite", None)
    date_value = getattr(activity, "date_activite", None)
    return {
        "id": identifier,
        "titre": getattr(activity, "titre", None),
        "sport": getattr(activity, "sport", None),
        "distance": getattr(activity, "distance", None),
        "duree_heures": getattr(activity, "duree", None),
        "date_activite": date_value.isoformat() if date_value else None,
        "lieu": getattr(activity, "lieu", None),
        "detail_sport": getattr(activity, "detail_sport", None),
        "id_user": getattr(activity, "id_user", None),
    }


# ============================================================================
# AUTHENTIFICATION
# ============================================================================

# ATTENTION: Ceci est une authentification basique pour le developpement
# En production, utiliser JWT tokens et base de donnees reelle


@app.post("/login")
def login(username: str, password: str):
    """
    Authentifie un utilisateur via parametres simples :
    """

    user_service = UtilisateurService()

    user = user_service.se_connecter(nom_user=username, mdp=password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur ou mot de passe incorrect",
        )

    return {
        "message": "Connexion reussie",
        "user": {
            "id": user.id_user,
            "username": user.nom_user,
            "email": user.mail_user,
        },
    }


# ============================================================================
# ENDPOINTS UTILISATEURS
# ============================================================================


@app.post("/users")
def create_user(nom_user: str, mail_user: str, mdp: str):
    """Creer un nouvel utilisateur

    Parameters:
    - nom_user: Nom d'utilisateur (unique)
    - mail_user: Email de l'utilisateur
    - mdp: Mot de passe
    """
    try:
        utilisateur_service = UtilisateurService()

        # Verifier que le nom d'utilisateur n'existe pas deja
        if utilisateur_service.nom_user_deja_utilise(nom_user):
            raise HTTPException(status_code=400, detail="Ce nom d'utilisateur est deja utilise")

        # Validation basique
        if not nom_user or len(nom_user.strip()) == 0:
            raise HTTPException(
                status_code=400, detail="Le nom d'utilisateur ne peut pas etre vide"
            )

        if not mail_user or "@" not in mail_user:
            raise HTTPException(status_code=400, detail="Email invalide")

        if not mdp or len(mdp) < 4:
            raise HTTPException(
                status_code=400, detail="Le mot de passe doit contenir au moins 4 caracteres"
            )

        # Creer l'utilisateur (id_user=None car auto-genere par la base)
        nouvel_utilisateur = utilisateur_service.creer(
            nom_user=nom_user, mail_user=mail_user, mdp=mdp
        )

        if not nouvel_utilisateur:
            raise HTTPException(
                status_code=500, detail="Erreur lors de la creation de l'utilisateur"
            )

        return {"message": "Utilisateur cree avec succes", "user": nouvel_utilisateur}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la creation: {str(e)}")


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Authentifie un utilisateur via Authorization: Basic ... sur chaque requete
    """
    user_service = UtilisateurService()

    user = user_service.se_connecter(nom_user=credentials.username, mdp=credentials.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides",
            headers={"WWW-Authenticate": "Basic"},
        )

    return {"id": user.id_user, "username": user.nom_user, "email": user.mail_user}


# ============================================================================
# ENDPOINTS ACTIVITES
# ============================================================================
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
    """Creer une activite (manuelle ou via fichier GPX)."""
    try:
        gpx_data = None
        if gpx_file:
            gpx_data = parse_strava_gpx(await gpx_file.read())

        titre_final = titre or (gpx_data.get("nom") if gpx_data else None) or "Activite importee"
        sport_final = (sport or (gpx_data.get("type") if gpx_data else "course")).lower()

        if not gpx_file and not all([titre_final, sport_final, date_activite, distance]):
            raise HTTPException(
                status_code=400,
                detail="Les champs titre, sport, date_activite et distance sont obligatoires en mode manuel",
            )

        raw_distance = (
            distance
            if distance is not None
            else (gpx_data.get("distance_km") if gpx_data else None)
        )
        distance_km = _coerce_float(raw_distance, "distance")
        if distance_km is None or distance_km <= 0:
            raise HTTPException(status_code=400, detail="La distance doit etre positive")

        raw_duree = duree
        if raw_duree is None and gpx_data:
            raw_duree = gpx_data.get("temps_mouvement_heures") or gpx_data.get("duree_heures")
        duree_heures = _coerce_float(raw_duree, "duree")
        if duree_heures is not None and duree_heures <= 0:
            raise HTTPException(status_code=400, detail="La duree doit etre positive")

        date_value = _parse_date(date_activite) if date_activite else datetime.now()

        sports_valides = {"course", "cyclisme", "natation", "randonnee"}
        if sport_final not in sports_valides:
            raise HTTPException(
                status_code=400,
                detail=f"Type de sport invalide. Valeurs acceptees: {', '.join(sorted(sports_valides))}",
            )

        activity_data = {
            "titre": titre_final,
            "description": description or "",
            "sport": sport_final,
            "date_activite": date_value,
            "lieu": lieu or "",
            "distance": distance_km,
            "duree": duree_heures,
            "id_user": current_user["id"],
        }

        if not ActivityService().creer_activite_from_dict(activity_data):
            raise HTTPException(status_code=500, detail="Erreur lors de la creation de l'activite")

        return {
            "message": "Activite creee avec succes",
            "activity": {
                "titre": titre_final,
                "sport": sport_final,
                "date_activite": date_value.isoformat(),
                "distance": distance_km,
                "duree_heures": duree_heures,
                "lieu": lieu or "",
            },
        }

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/activities/{activity_id}/like")
def like_activity(activity_id: int, current_user: dict = Depends(get_current_user)):
    """Liker une activite"""
    try:
        like_service = LikeService()
        activity_service = ActivityService()
        user_id = current_user["id"]

        # 1. Verifier si l'activite existe
        activity = activity_service.get_activite_by_id(activity_id)
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")

        # 2. Verifier si deja like
        existing_likes = like_service.get_likes_activite(activity_id)
        already_liked = any(like.id_user == user_id for like in existing_likes)

        if already_liked:
            return {"message": f"Activity {activity_id} already liked", "already_liked": True}

        # 3. Liker l'activite
        success = like_service.liker_activite(user_id, activity_id)

        if not success:
            # Ceci attrape le cas ou le service retourne False (echec DAO/DB)
            raise HTTPException(status_code=500, detail="Cannot like activity")

        return {"message": f"Activity {activity_id} liked successfully", "already_liked": False}
    except HTTPException:
        raise
    except Exception as e:
        # Ceci attrape les erreurs non gerees dans les services (la cause du 500 dans vos logs)
        print(f"Erreur critique lors du like de l'activite {activity_id}: {e}")
        # Optionnel: traceback.print_exc() ici pour le debogage
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")


@app.delete("/activities/{activity_id}/like")
def unlike_activity(activity_id: int, current_user: dict = Depends(get_current_user)):
    """Retirer un like d'une activite"""
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
    """Recupere les likes d'une activite"""
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

# ============================================================================
# HEALTH & ME
# ============================================================================


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/me")
def me(current_user: dict = Depends(get_current_user)):
    return current_user


# ============================================================================
# FEED, LISTING & STATS
# ============================================================================


@app.get("/users/{user_id}/activities")
def list_user_activities(
    user_id: int,
    sport: str | None = None,
    year: int | None = None,
    month: int | None = None,
    current_user: dict = Depends(get_current_user),
):
    if current_user["id"] != user_id:
        raise HTTPException(status_code=403, detail="Acces refuse")
    service = ActivityService()
    if year and month:
        activities = service.get_monthly_activities(user_id, year, month, sport)
    else:
        activities = service.get_activites_by_user(user_id, sport)
    return [_activity_to_dict(a) for a in activities]


@app.get("/feed")
def get_feed_endpoint(current_user: dict = Depends(get_current_user)):
    try:
        activities = ActivityService().get_feed(current_user["id"])
        return [_activity_to_dict(a) for a in activities]
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/stats/monthly")
def stats_monthly(
    year: int | None = None,
    month: int | None = None,
    current_user: dict = Depends(get_current_user),
):
    svc = StatistiquesService()
    stats = svc.get_statistiques_mensuelles(current_user["id"], year, month)
    if stats is None:
        raise HTTPException(status_code=500, detail="Erreur lors du calcul des statistiques")
    return stats


@app.get("/stats/annual")
def stats_annual(year: int | None = None, current_user: dict = Depends(get_current_user)):
    svc = StatistiquesService()
    stats = svc.get_statistiques_annuelles(current_user["id"], year)
    if stats is None:
        raise HTTPException(status_code=500, detail="Erreur lors du calcul des statistiques")
    return stats


@app.get("/stats/global")
def stats_global(current_user: dict = Depends(get_current_user)):
    svc = StatistiquesService()
    stats = svc.get_statistiques_globales(current_user["id"])
    if stats is None:
        raise HTTPException(status_code=500, detail="Erreur lors du calcul des statistiques")
    return stats


@app.get("/stats/weekly-average")
def stats_weekly_average(nb_semaines: int = 4, current_user: dict = Depends(get_current_user)):
    svc = StatistiquesService()
    stats = svc.get_moyenne_par_semaine(current_user["id"], nb_semaines)
    if stats is None:
        raise HTTPException(status_code=500, detail="Erreur lors du calcul des statistiques")
    return stats


# ============================================================================
# ENDPOINTS COMMENTAIRES
# ============================================================================


@app.post("/activities/{activity_id}/comments")
def create_comment(activity_id: int, contenu: str, current_user: dict = Depends(get_current_user)):
    """Créer un commentaire sur une activité"""
    try:
        commentaire_service = CommentaireService()
        activity_service = ActivityService()

        # Vérifier que l'activité existe
        activity = activity_service.get_activite_by_id(activity_id)
        if not activity:
            raise HTTPException(status_code=404, detail="Activité non trouvée")

        success = commentaire_service.creer_commentaire(current_user["id"], activity_id, contenu)

        if not success:
            raise HTTPException(status_code=500, detail="Erreur lors de la création du commentaire")

        return {"message": "Commentaire créé avec succès"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/activities/{activity_id}/comments")
def get_activity_comments(activity_id: int, current_user: dict = Depends(get_current_user)):
    """Récupérer les commentaires d'une activité"""
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
                    "contenu": comment.contenu,
                    "id_user": comment.id_user,
                    "date_comment": comment.date_comment.isoformat()
                    if hasattr(comment.date_comment, "isoformat")
                    else str(comment.date_comment),
                }
                for comment in comments
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, current_user: dict = Depends(get_current_user)):
    """Supprimer un commentaire"""
    try:
        commentaire_service = CommentaireService()
        success = commentaire_service.supprimer_commentaire(comment_id)

        if not success:
            raise HTTPException(status_code=404, detail="Commentaire non trouvé")

        return {"message": "Commentaire supprimé avec succès"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ENDPOINTS MODIFICATIONS/SUPPRESSION ACTIVITÉS
# ============================================================================


@app.put("/activities/{activity_id}")
def update_activity(
    activity_id: int,
    titre: str = None,
    description: str = None,
    sport: str = None,
    lieu: str = None,
    distance: float = None,
    duree: float = None,
    current_user: dict = Depends(get_current_user),
):
    """Modifier une activité existante"""
    try:
        activity_service = ActivityService()

        # Récupérer l'activité existante
        activity = activity_service.get_activite_by_id(activity_id)
        if not activity:
            raise HTTPException(status_code=404, detail="Activité non trouvée")

        # Vérifier que l'utilisateur est le propriétaire
        if activity.id_user != current_user["id"]:
            raise HTTPException(
                status_code=403, detail="Vous n'êtes pas autorisé à modifier cette activité"
            )

        # Mettre à jour les champs modifiés
        activity_data = {
            "id_activite": activity_id,
            "titre": titre if titre else activity.titre,
            "description": description if description else activity.description,
            "sport": sport if sport else activity.sport,
            "date_activite": activity.date_activite,
            "lieu": lieu if lieu else activity.lieu,
            "distance": distance if distance is not None else activity.distance,
            "duree": duree if duree is not None else activity.duree,
            "id_user": activity.id_user,
            "detail_sport": activity.detail_sport,
        }

        success = activity_service.modifier_activite_from_dict(activity_data)

        if not success:
            raise HTTPException(status_code=500, detail="Erreur lors de la modification")

        return {"message": "Activité modifiée avec succès"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/activities/{activity_id}")
def delete_activity(activity_id: int, current_user: dict = Depends(get_current_user)):
    """Supprimer une activité"""
    try:
        activity_service = ActivityService()

        # Récupérer l'activité
        activity = activity_service.get_activite_by_id(activity_id)
        if not activity:
            raise HTTPException(status_code=404, detail="Activité non trouvée")

        # Vérifier que l'utilisateur est le propriétaire
        if activity.id_user != current_user["id"]:
            raise HTTPException(
                status_code=403, detail="Vous n'êtes pas autorisé à supprimer cette activité"
            )

        success = activity_service.supprimer_activite(activity_id)

        if not success:
            raise HTTPException(status_code=500, detail="Erreur lors de la suppression")

        return {"message": "Activité supprimée avec succès"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/activities/{activity_id}")
def get_activity(activity_id: int, current_user: dict = Depends(get_current_user)):
    """Récupérer une activité par son ID"""
    try:
        activity_service = ActivityService()
        activity = activity_service.get_activite_by_id(activity_id)

        if not activity:
            raise HTTPException(status_code=404, detail="Activité non trouvée")

        return _activity_to_dict(activity)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ENDPOINTS SUIVI D'UTILISATEURS
# ============================================================================

from service.suivi_service import SuiviService


@app.get("/users")
def list_users(current_user: dict = Depends(get_current_user)):
    """Lister tous les utilisateurs (pour pouvoir les suivre)"""
    try:
        user_service = UtilisateurService()
        users = user_service.lister_tous()

        return [
            {"id_user": user.id_user, "nom_user": user.nom_user, "mail_user": user.mail_user}
            for user in users
            if user.id_user != current_user["id"]  # Exclure l'utilisateur courant
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/users/{user_id}/follow")
def follow_user(user_id: int, current_user: dict = Depends(get_current_user)):
    """Suivre un utilisateur"""
    try:
        if user_id == current_user["id"]:
            raise HTTPException(status_code=400, detail="Vous ne pouvez pas vous suivre vous-même")

        suivi_service = SuiviService()
        success = suivi_service.suivre_utilisateur(current_user["id"], user_id)

        if not success:
            raise HTTPException(
                status_code=400,
                detail="Vous suivez déjà cet utilisateur ou l'utilisateur n'existe pas",
            )

        return {"message": f"Vous suivez maintenant l'utilisateur {user_id}"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/users/{user_id}/follow")
def unfollow_user(user_id: int, current_user: dict = Depends(get_current_user)):
    """Ne plus suivre un utilisateur"""
    try:
        suivi_service = SuiviService()
        success = suivi_service.ne_plus_suivre(current_user["id"], user_id)

        if not success:
            raise HTTPException(status_code=404, detail="Vous ne suivez pas cet utilisateur")

        return {"message": f"Vous ne suivez plus l'utilisateur {user_id}"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users/{user_id}/following")
def get_following(user_id: int, current_user: dict = Depends(get_current_user)):
    """Récupérer la liste des utilisateurs suivis"""
    try:
        suivi_service = SuiviService()
        following = suivi_service.get_following(user_id)

        return [
            {"id_user": user.id_user, "nom_user": user.nom_user, "mail_user": user.mail_user}
            for user in following
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users/{user_id}/followers")
def get_followers(user_id: int, current_user: dict = Depends(get_current_user)):
    """Récupérer la liste des followers"""
    try:
        suivi_service = SuiviService()
        followers = suivi_service.get_followers(user_id)

        return [
            {"id_user": user.id_user, "nom_user": user.nom_user, "mail_user": user.mail_user}
            for user in followers
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users/{user_id}/is-following/{target_user_id}")
def is_following(user_id: int, target_user_id: int, current_user: dict = Depends(get_current_user)):
    """Vérifier si un utilisateur en suit un autre"""
    try:
        suivi_service = SuiviService()
        is_following = suivi_service.user_suit(user_id, target_user_id)

        return {"is_following": is_following}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
