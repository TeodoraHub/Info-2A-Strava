from fastapi import APIRouter, Depends, HTTPException

from routers.auth import get_current_user
from service.activity_service import ActivityService
from service.like_service import LikeService

router = APIRouter(prefix="/activities", tags=["Likes"])


@router.post("/{activity_id}/like")
def like_activity(activity_id: int, current_user: dict = Depends(get_current_user)):
    """Liker une activite"""
    try:
        like_service = LikeService()
        activity_service = ActivityService()
        user_id = current_user["id"]

        activity = activity_service.get_activite_by_id(activity_id)
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")

        existing_likes = like_service.get_likes_activite(activity_id)
        already_liked = any(like.id_user == user_id for like in existing_likes)

        if already_liked:
            return {"message": f"Activity {activity_id} already liked", "already_liked": True}

        success = like_service.liker_activite(user_id, activity_id)

        if not success:
            raise HTTPException(status_code=500, detail="Cannot like activity")

        return {"message": f"Activity {activity_id} liked successfully", "already_liked": False}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erreur critique lors du like de l'activite {activity_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")


@router.delete("/{activity_id}/like")
def unlike_activity(activity_id: int, current_user: dict = Depends(get_current_user)):
    """Retirer un like d'une activite"""
    try:
        like_service = LikeService()
        user_id = current_user["id"]

        success = like_service.unliker_activite(user_id, activity_id)
        if not success:
            raise HTTPException(status_code=404, detail="Like not found")

        return {"message": f"Like removed from activity {activity_id}"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{activity_id}/likes")
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
