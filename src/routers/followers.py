from fastapi import APIRouter, Depends, HTTPException

from routers.auth import get_current_user
from service.suivi_service import SuiviService
from service.utilisateur_service import UtilisateurService

router = APIRouter(prefix="/users", tags=["Followers"])


@router.get("")
def list_users(current_user: dict = Depends(get_current_user)):
    """Lister tous les utilisateurs (pour pouvoir les suivre)"""
    try:
        user_service = UtilisateurService()
        users = user_service.lister_tous()

        return [
            {"id_user": user.id_user, "nom_user": user.nom_user, "mail_user": user.mail_user}
            for user in users
            if user.id_user != current_user["id"]
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{user_id}/follow")
def follow_user(user_id: int, current_user: dict = Depends(get_current_user)):
    """Suivre un utilisateur"""
    try:
        if user_id == current_user["id"]:
            raise HTTPException(status_code=400, detail="Vous ne pouvez pas vous suivre vous-meme")

        suivi_service = SuiviService()
        success = suivi_service.suivre_utilisateur(current_user["id"], user_id)

        if not success:
            raise HTTPException(
                status_code=400,
                detail="Vous suivez deja cet utilisateur ou l'utilisateur n'existe pas",
            )

        return {"message": f"Vous suivez maintenant l'utilisateur {user_id}"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{user_id}/follow")
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


@router.get("/{user_id}/following")
def get_following(user_id: int, current_user: dict = Depends(get_current_user)):
    """Recuperer la liste des utilisateurs suivis"""
    try:
        suivi_service = SuiviService()
        following = suivi_service.get_following(user_id)

        return [
            {"id_user": user.id_user, "nom_user": user.nom_user, "mail_user": user.mail_user}
            for user in following
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{user_id}/followers")
def get_followers(user_id: int, current_user: dict = Depends(get_current_user)):
    """Recuperer la liste des followers"""
    try:
        suivi_service = SuiviService()
        followers = suivi_service.get_followers(user_id)

        return [
            {"id_user": user.id_user, "nom_user": user.nom_user, "mail_user": user.mail_user}
            for user in followers
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{user_id}/is-following/{target_user_id}")
def is_following(user_id: int, target_user_id: int, current_user: dict = Depends(get_current_user)):
    """Verifier si un utilisateur en suit un autre"""
    try:
        suivi_service = SuiviService()
        is_following = suivi_service.user_suit(user_id, target_user_id)

        return {"is_following": is_following}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
