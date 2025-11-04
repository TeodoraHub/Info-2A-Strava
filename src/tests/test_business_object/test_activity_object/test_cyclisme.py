from datetime import datetime

from business_object.Activity_object.cyclisme import Cyclisme


class TestCyclismeCreation:
    """Tests de création d'une activité de cyclisme"""

    def test_creation_cyclisme_complete(self):
        # GIVEN - Des données complètes pour une activité de cyclisme
        date_activite = datetime(2025, 11, 4, 9, 0)

        # WHEN - On crée une instance de Cyclisme
        cyclisme = Cyclisme(
            id_activite=10,
            titre="Sortie montagne",
            description="Grimpe matinale au col du Galibier",
            duree=180,  # 3h
            date_activite=date_activite,
            lieu="Galibier",
            distance=75.0,  # km
            id_user=5,
            type_velo="Route",
        )

        # THEN - L'objet est correctement créé
        assert cyclisme.id == 10
        assert cyclisme.titre == "Sortie montagne"
        assert cyclisme.description == "Grimpe matinale au col du Galibier"
        assert cyclisme.date_activite == date_activite
        assert cyclisme.lieu == "Galibier"
        assert cyclisme.distance == 75.0
        assert cyclisme.id_user == 5
        assert cyclisme.type_velo == "Route"
        assert cyclisme.duree == 180
        assert cyclisme.sport == "cyclisme" or cyclisme.sport == ("cyclisme",)

    def test_vitesse_cyclisme(self):
        # GIVEN - Une activité avec 90 km en 3h (180 min)
        cyclisme = Cyclisme(
            id_activite=11,
            titre="Longue sortie",
            description="Sortie d'endurance",
            duree=180,
            date_activite=datetime(2025, 11, 4, 8, 0),
            lieu="Nice",
            distance=90.0,
            id_user=7,
            type_velo="Gravel",
        )

        # WHEN - On calcule la vitesse moyenne
        vitesse = cyclisme.vitesse()

        # THEN - 90 km / 180 min * 60 = 30 km/h
        assert vitesse == 30.0

    def test_str_cyclisme(self):
        # GIVEN
        cyclisme = Cyclisme(
            id_activite=13,
            titre="Balade du soir",
            description="Sortie tranquille",
            duree=60,
            date_activite=datetime(2025, 11, 4, 18, 0),
            lieu="Bordeaux",
            distance=20.0,
            id_user=3,
            type_velo="Ville",
        )

        # WHEN
        affichage = str(cyclisme)

        # THEN
        assert "Ville" in affichage
        assert "Vitesse moyenne" in affichage
        assert "km/h" in affichage
