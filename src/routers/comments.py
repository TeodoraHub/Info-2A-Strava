from fastapi import APIRouter, Depends, HTTPException

from routers.auth import get_current_user
from service.activity_service import ActivityService
from service.commentaire_service import CommentaireService

router = APIRouter(tags=["Comments"])


@router.post("/activities/{activity_id}/comments")
def create_comment(activity_id: int, contenu: str, current_user: dict = Depends(get_current_user)):
    """Creer un commentaire sur une activite"""
    try:
        commentaire_service = CommentaireService()
        activity_service = ActivityService()

        activity = activity_service.get_activite_by_id(activity_id)
        if not activity:
            raise HTTPException(status_code=404, detail="Activite non trouvee")

        success = commentaire_service.creer_commentaire(current_user["id"], activity_id, contenu)

        if not success:
            raise HTTPException(status_code=500, detail="Erreur lors de la creation du commentaire")

        return {"message": "Commentaire cree avec succes"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/activities/{activity_id}/comments")
def get_activity_comments(activity_id: int, current_user: dict = Depends(get_current_user)):
    """Recuperer les commentaires d'une activite"""
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


@router.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, current_user: dict = Depends(get_current_user)):
    """Supprimer un commentaire"""
    try:
        commentaire_service = CommentaireService()
        success = commentaire_service.supprimer_commentaire(comment_id)

        if not success:
            raise HTTPException(status_code=404, detail="Commentaire non trouve")

        return {"message": "Commentaire supprime avec succes"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
