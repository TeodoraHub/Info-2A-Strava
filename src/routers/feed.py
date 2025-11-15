from fastapi import APIRouter, Depends, HTTPException

from routers.auth import get_current_user
from service.activity_service import ActivityService
from utils.gpx_parser import _activity_to_dict

router = APIRouter(tags=["Feed"])


@router.get("/feed")
def get_feed_endpoint(current_user: dict = Depends(get_current_user)):
    """Recuperer le feed des activites"""
    try:
        activities = ActivityService().get_feed(current_user["id"])
        return [_activity_to_dict(a) for a in activities]
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
