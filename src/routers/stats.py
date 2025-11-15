from fastapi import APIRouter, Depends, HTTPException

from routers.auth import get_current_user
from service.activity_service import ActivityService
from service.statistiques_service import StatistiquesService

router = APIRouter(prefix="/stats", tags=["Statistics"])


@router.get("/monthly")
def stats_monthly(
    year: int | None = None,
    month: int | None = None,
    current_user: dict = Depends(get_current_user),
):
    """Statistiques mensuelles"""
    svc = StatistiquesService()
    stats = svc.get_statistiques_mensuelles(current_user["id"], year, month)
    if stats is None:
        raise HTTPException(status_code=500, detail="Erreur lors du calcul des statistiques")
    return stats


@router.get("/annual")
def stats_annual(year: int | None = None, current_user: dict = Depends(get_current_user)):
    """Statistiques annuelles"""
    svc = StatistiquesService()
    stats = svc.get_statistiques_annuelles(current_user["id"], year)
    if stats is None:
        raise HTTPException(status_code=500, detail="Erreur lors du calcul des statistiques")
    return stats


@router.get("/global")
def stats_global(current_user: dict = Depends(get_current_user)):
    """Statistiques globales"""
    svc = StatistiquesService()
    stats = svc.get_statistiques_globales(current_user["id"])
    if stats is None:
        raise HTTPException(status_code=500, detail="Erreur lors du calcul des statistiques")
    return stats


@router.get("/weekly-average")
def stats_weekly_average(nb_semaines: int = 4, current_user: dict = Depends(get_current_user)):
    """Moyenne par semaine"""
    svc = StatistiquesService()
    stats = svc.get_moyenne_par_semaine(current_user["id"], nb_semaines)
    if stats is None:
        raise HTTPException(status_code=500, detail="Erreur lors du calcul des statistiques")
    return stats


@router.get("/user/{user_id}/monthly")
def user_activities_monthly(
    user_id: int,
    sport: str | None = None,
    year: int | None = None,
    month: int | None = None,
    current_user: dict = Depends(get_current_user),
):
    """Activites d'un utilisateur"""
    if current_user["id"] != user_id:
        raise HTTPException(status_code=403, detail="Acces refuse")
    service = ActivityService()
    if year and month:
        activities = service.get_monthly_activities(user_id, year, month, sport)
    else:
        activities = service.get_activites_by_user(user_id, sport)

    from utils.gpx_parser import _activity_to_dict

    return [_activity_to_dict(a) for a in activities]
