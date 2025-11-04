from datetime import datetime
import pytest
from business_object.Activity_object.course_a_pieds import CoursePied


class TestCoursePiedCreation:
    """Tests de création et de comportement d'une activité de course à pied"""

    def test_creation_course_pied_complete(self):
        # GIVEN - Des données complètes pour une activité de course
        date_activite = datetime(2025, 11, 4, 7, 0)

        # WHEN - On crée une instance de CoursePied
        course = CoursePied(
            id_activite=1,
            titre="Footing du matin",
            description="Petit run de récupération",
            date_activite=date_activite,
            lieu="Parc de la Tête d'Or",
            distance=10.0,  # km
            id_user=2,
            duree=1.0  # heures
        )

        # THEN - L'objet est correctement initialisé
        assert course.id == 1
        assert course.titre == "Footing du matin"
        assert course.description == "Petit run de récupération"
        assert course.date_activite == date_activite
        assert course.lieu == "Parc de la Tête d'Or"
        assert course.distance == 10.0
        assert course.id_user == 2
        assert course.duree == 1.0
        assert course.sport == "course" or course.sport == ("course",)

    def test_vitesse_normale(self):
        # GIVEN - Une course de 12 km en 1h
        course = CoursePied(
            id_activite=2,
            titre="Course tempo",
            description="Entraînement soutenu",
            date_activite=datetime(2025, 11, 4, 18, 0),
            lieu="Lyon",
            distance=12.0,
            id_user=1,
            duree=1.0
        )

        # WHEN - On calcule la vitesse
        vitesse = course.vitesse()

        # THEN - 12 km / 1 h = 12 km/h
        assert vitesse == pytest.approx(12.0)

    def test_vitesse_duree_zero(self):
        # GIVEN - Une durée nulle
        course = CoursePied(
            id_activite=3,
            titre="Erreur de durée",
            description="Durée nulle",
            date_activite=datetime(2025, 11, 4, 10, 0),
            lieu="Paris",
            distance=5.0,
            id_user=3,
            duree=0
        )

        # WHEN
        vitesse = course.vitesse()

        # THEN - La vitesse doit être 0.0
        assert vitesse == 0.0
