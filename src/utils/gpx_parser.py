"""
Module pour parser les fichiers GPX et extraire les données d'activités sportives
"""

import logging
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import List, Optional, Tuple


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
