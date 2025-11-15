from datetime import datetime

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from routers.auth import get_current_user
from service.activity_service import ActivityService
from utils.gpx_parser import _activity_to_dict, _coerce_float, _parse_date, parse_strava_gpx

router = APIRouter(prefix="/activities", tags=["Activities"])


@router.post("")
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
    """Creer une activite (manuelle ou via fichier GPX)"""
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


@router.get("/{activity_id}")
def get_activity(activity_id: int, current_user: dict = Depends(get_current_user)):
    """Recuperer une activite par son ID"""
    try:
        activity_service = ActivityService()
        activity = activity_service.get_activite_by_id(activity_id)

        if not activity:
            raise HTTPException(status_code=404, detail="Activite non trouvee")

        return _activity_to_dict(activity)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{activity_id}")
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
    """Modifier une activite existante"""
    try:
        activity_service = ActivityService()
        activity = activity_service.get_activite_by_id(activity_id)
        if not activity:
            raise HTTPException(status_code=404, detail="Activite non trouvee")

        if activity.id_user != current_user["id"]:
            raise HTTPException(
                status_code=403, detail="Vous n'etes pas autorise a modifier cette activite"
            )

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

        return {"message": "Activite modifiee avec succes"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{activity_id}")
def delete_activity(activity_id: int, current_user: dict = Depends(get_current_user)):
    """Supprimer une activite"""
    try:
        activity_service = ActivityService()
        activity = activity_service.get_activite_by_id(activity_id)
        if not activity:
            raise HTTPException(status_code=404, detail="Activite non trouvee")

        if activity.id_user != current_user["id"]:
            raise HTTPException(
                status_code=403, detail="Vous n'etes pas autorise a supprimer cette activite"
            )

        success = activity_service.supprimer_activite(activity_id)

        if not success:
            raise HTTPException(status_code=500, detail="Erreur lors de la suppression")

        return {"message": "Activite supprimee avec succes"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload-gpx")
async def upload_gpx(file: UploadFile = File(...)):
    """Uploader et parser un fichier GPX"""
    content = await file.read()
    return parse_strava_gpx(content)
