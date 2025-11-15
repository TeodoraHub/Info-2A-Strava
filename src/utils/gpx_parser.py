"""
Module pour parser les fichiers GPX et extraire les données d'activités sportives
"""

import logging
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

import gpxpy
from fastapi import HTTPException


class GPXParser:
    """Classe pour parser les fichiers GPX"""

    # Namespaces GPX
    GPX_NS = {"gpx": "http://www.topografix.com/GPX/1/1"}

    @staticmethod
    def parse_gpx_file(filepath: str) -> dict:
        """Parse un fichier GPX et extrait les informations principales

        Parameters
        ----------
        filepath : str
            Chemin vers le fichier GPX

        Returns
        -------
        dict
            Dictionnaire contenant les données de l'activité
            {
                'distance': float (en mètres),
                'duree': timedelta,
                'date_activite': datetime,
                'points': list of dict avec lat, lon, ele, time
            }
        """
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()

            # Extraire les points de trace
            points = GPXParser._extract_track_points(root)

            if not points:
                logging.warning("Aucun point de trace trouvé dans le fichier GPX")
                return None

            # Calculer la distance totale
            distance = GPXParser._calculate_total_distance(points)

            # Calculer la durée
            duree = GPXParser._calculate_duration(points)

            # Date de l'activité (premier point)
            date_activite = points[0].get("time") if points else None

            return {
                "distance": distance,
                "duree": duree,
                "date_activite": date_activite,
                "points": points,
                "nb_points": len(points),
            }

        except ET.ParseError as e:
            logging.error(f"Erreur de parsing XML: {e}")
            return None
        except Exception as e:
            logging.error(f"Erreur lors du parsing du fichier GPX: {e}")
            return None

    @staticmethod
    def _extract_track_points(root) -> List[dict]:
        """Extrait les points de trace du fichier GPX

        Parameters
        ----------
        root : Element
            Élément racine du XML

        Returns
        -------
        list
            Liste de dictionnaires contenant les données de chaque point
        """
        points = []

        # Chercher dans les tracks
        for trk in root.findall(".//gpx:trk", GPXParser.GPX_NS):
            for trkseg in trk.findall(".//gpx:trkseg", GPXParser.GPX_NS):
                for trkpt in trkseg.findall(".//gpx:trkpt", GPXParser.GPX_NS):
                    point = GPXParser._parse_track_point(trkpt)
                    if point:
                        points.append(point)

        # Si pas de tracks, chercher dans les routes
        if not points:
            for rte in root.findall(".//gpx:rte", GPXParser.GPX_NS):
                for rtept in rte.findall(".//gpx:rtept", GPXParser.GPX_NS):
                    point = GPXParser._parse_track_point(rtept)
                    if point:
                        points.append(point)

        return points

    @staticmethod
    def _parse_track_point(trkpt) -> Optional[dict]:
        """Parse un point de trace individuel

        Parameters
        ----------
        trkpt : Element
            Élément XML du point de trace

        Returns
        -------
        dict ou None
            Dictionnaire avec lat, lon, ele (optionnel), time (optionnel)
        """
        try:
            lat = float(trkpt.get("lat"))
            lon = float(trkpt.get("lon"))

            point = {"lat": lat, "lon": lon}

            # Élévation (optionnel)
            ele = trkpt.find("gpx:ele", GPXParser.GPX_NS)
            if ele is not None and ele.text:
                point["ele"] = float(ele.text)

            # Temps (optionnel)
            time = trkpt.find("gpx:time", GPXParser.GPX_NS)
            if time is not None and time.text:
                point["time"] = datetime.fromisoformat(time.text.replace("Z", "+00:00"))

            return point

        except (ValueError, AttributeError) as e:
            logging.warning(f"Erreur lors du parsing d'un point: {e}")
            return None

    @staticmethod
    def _calculate_total_distance(points: List[dict]) -> float:
        """Calcule la distance totale en mètres à partir des points

        Parameters
        ----------
        points : list
            Liste des points avec lat, lon

        Returns
        -------
        float
            Distance totale en mètres
        """
        if len(points) < 2:
            return 0.0

        total_distance = 0.0
        for i in range(len(points) - 1):
            dist = GPXParser._haversine_distance(
                points[i]["lat"],
                points[i]["lon"],
                points[i + 1]["lat"],
                points[i + 1]["lon"],
            )
            total_distance += dist

        return total_distance

    @staticmethod
    def _haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calcule la distance entre deux points GPS en utilisant la formule de Haversine

        Parameters
        ----------
        lat1, lon1 : float
            Coordonnées du premier point
        lat2, lon2 : float
            Coordonnées du second point

        Returns
        -------
        float
            Distance en mètres
        """
        from math import atan2, cos, radians, sin, sqrt

        R = 6371000  # Rayon de la Terre en mètres

        lat1_rad = radians(lat1)
        lat2_rad = radians(lat2)
        delta_lat = radians(lat2 - lat1)
        delta_lon = radians(lon2 - lon1)

        a = sin(delta_lat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        return distance

    @staticmethod
    def _calculate_duration(points: List[dict]) -> Optional[timedelta]:
        """Calcule la durée de l'activité à partir des timestamps

        Parameters
        ----------
        points : list
            Liste des points avec time

        Returns
        -------
        timedelta ou None
            Durée de l'activité
        """
        points_with_time = [p for p in points if "time" in p]

        if len(points_with_time) < 2:
            return None

        start_time = points_with_time[0]["time"]
        end_time = points_with_time[-1]["time"]

        return end_time - start_time

    @staticmethod
    def get_elevation_gain(points: List[dict]) -> Tuple[float, float]:
        """Calcule le dénivelé positif et négatif

        Parameters
        ----------
        points : list
            Liste des points avec ele

        Returns
        -------
        tuple
            (dénivelé_positif, dénivelé_négatif) en mètres
        """
        points_with_ele = [p for p in points if "ele" in p]

        if len(points_with_ele) < 2:
            return 0.0, 0.0

        denivele_positif = 0.0
        denivele_negatif = 0.0

        for i in range(len(points_with_ele) - 1):
            diff = points_with_ele[i + 1]["ele"] - points_with_ele[i]["ele"]
            if diff > 0:
                denivele_positif += diff
            else:
                denivele_negatif += abs(diff)

        return denivele_positif, denivele_negatif


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
