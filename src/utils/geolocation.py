import polyline as pl
import requests
from geopy.geocoders import Nominatim


def get_coordinates(address):
    """Récupère les coordonnées GPS à partir d'une adresse"""
    try:
        geolocator = Nominatim(user_agent="striv_app")
        location = geolocator.geocode(address)
        if location:
            return (location.latitude, location.longitude)
        return None
    except Exception as e:
        print(f"Erreur géolocalisation: {str(e)}")
        return None


def get_route(start_coords, end_coords):
    """Récupère un itinéraire entre deux points via OpenRouteService"""
    try:
        # Utilise OpenRouteService (gratuit, pas d'API key pour usage basique)
        url = "https://router.project-osrm.org/route/v1/foot-walking"
        params = f"{start_coords[1]},{start_coords[0]};{end_coords[1]},{end_coords[0]}"

        response = requests.get(f"{url}/{params}?overview=full&geometries=polyline")

        if response.status_code == 200:
            data = response.json()
            if data.get("routes"):
                route = data["routes"][0]
                # Décode la polyline
                coords = pl.decode(route["geometry"])
                distance = route["distance"] / 1000  # en km
                duration = distance / 10  # en heures

                return {"coordinates": coords, "distance": distance, "duration": duration}
        return None
    except Exception as e:
        print(f"Erreur itinéraire: {str(e)}")
        return None
