from datetime import datetime, timedelta

from src.business_object.user_object.statistiques import Statistiques


class FakeActivity:
    """Fausse classe activité pour les tests"""

    def __init__(self, sport, days_ago, distance=0, duree=0):
        self.date_activite = datetime.now() - timedelta(days=days_ago)
        self.distance = distance  # en mètres
        self.duree = duree  # en secondes
        self.__class__ = type(sport, (), {})


class FakeUtilisateur:
    """Fausse classe utilisateur pour les tests"""

    def __init__(self, activites):
        self.activites = activites


def test_filtrer_date():
    """Vérifie que le filtre par la date a fonctionné"""
    activites = [FakeActivity("Course", 3), FakeActivity("Course", 12), FakeActivity("Course", 2)]
    utilisateur = FakeUtilisateur(activites)

    resultat = Statistiques._filtrer(utilisateur, periode="7j", sport="Course")
    assert len(resultat) == 2
    assert resultat[0].__class__.__name__ == "Course"


def test_filtrer_sport():
    """Vérifie que le filtre par le sport a fonctionné"""
    activites = [
        FakeActivity("Natation", 3),
        FakeActivity("Course", 12),
        FakeActivity("Natation", 2),
    ]
    utilisateur = FakeUtilisateur(activites)

    resultat = Statistiques._filtrer(utilisateur, periode="30j", sport="Course")

    assert len(resultat) == 1
    assert resultat[0].__class__.__name__ == "Course"


def test_filtrer_sport_date():
    """Vérfifie que les deux filtres ont fonctionnés"""
    activites = [
        FakeActivity("Natation", 35),
        FakeActivity("Course", 12),
        FakeActivity("Natation", 2),
    ]
    utilisateur = FakeUtilisateur(activites)

    resultat = Statistiques._filtrer(utilisateur, periode="30j", sport="Natation")

    assert len(resultat) == 1
    assert resultat[0].__class__.__name__ == "Natation"


def test_nombre_activites():
    """Vérifie que nombre_activités a fonctionné, selon la date et le sport"""
    activites = [
        FakeActivity("Course", 1),
        FakeActivity("Course", 10),
        FakeActivity("Natation", 5),
    ]
    utilisateur = FakeUtilisateur(activites)

    nb = Statistiques.nombre_activites(utilisateur, periode="7j", sport="Course")
    assert nb == 1


def test_kilometres():
    """Vérifie que kilometres a fonctionné, selon la date et le sport"""
    activites = [
        FakeActivity("Course", 3, distance=5000),
        FakeActivity("Course", 1, distance=12000),
        FakeActivity("Course", 200, distance=3000),
        FakeActivity("Natation", 20, distance=3000),
    ]
    utilisateur = FakeUtilisateur(activites)

    total_km = Statistiques.kilometres(utilisateur, periode="30j", sport="Course")
    assert total_km == 17


def test_heures_activite():
    """Vérifie que heures_activite a fonctionné, selon la date et le sport"""
    activites = [
        FakeActivity("Course", 3, duree=3600),
        FakeActivity("Course", 10, duree=7200),
        FakeActivity("Course", 1, duree=1800),
        FakeActivity("Natation", 1, duree=1800),
    ]
    utilisateur = FakeUtilisateur(activites)

    total_heures = Statistiques.heures_activite(utilisateur, periode="7j", sport="Course")
    assert total_heures == 1.5
