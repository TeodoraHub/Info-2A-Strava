from datetime import datetime

import pytest

from business_object.Activity_object.natation import Natation


class TestNatationCreation:
    """Tests de création d'une activité de natation"""

    def test_creation_natation_complete(self):
        # GIVEN - Des données complètes pour une natation
        date = datetime(2025, 10, 31, 14, 30)

        # WHEN - On crée une natation
        natation = Natation(
            id_activite=1,
            titre="Nage au réveil",
            description="Séance matinale pour bien commencer la journée",
            date_activite=date,
            lieu="Piscine municipale",
            distance=2.0,  # 2 km
            id_user=1,
            type_nage="crawl",
            duree=60,  # 60 minutes
        )

        # THEN - L'objet est correctement créé
        assert natation.id == 1
        assert natation.titre == "Nage au réveil"
        assert natation.description == "Séance matinale pour bien commencer la journée"
        assert natation.date_activite == date
        assert natation.lieu == "Piscine municipale"
        assert natation.distance == 2.0
        assert natation.id_user == 1
        assert natation.type_nage == "crawl"
        assert natation.duree == 60
        assert natation.sport == "natation" or natation.sport == ("natation",)


class TestNatationVitesse:
    """Tests du calcul de vitesse en m/s"""

    def test_vitesse_nage(self):
        # GIVEN - Une natation de 2 km en 60 minutes
        natation = Natation(
            id_activite=1,
            titre="Test",
            description="Test",
            date_activite=datetime.now(),
            lieu="Piscine",
            distance=2.0,  # 2 km = 2000 m
            id_user=1,
            type_nage="crawl",
            duree=60,  # 60 minutes = 3600 secondes
        )

        # WHEN - On calcule la vitesse
        vitesse = natation.vitesse()

        # THEN - La vitesse est d'environ 0.556 m/s
        # Calcul: (2000 m) / (3600 s) = 0.556 m/s
        assert vitesse == pytest.approx(0.556, rel=1e-2)

    def test_vitesse_duree_zero(self):
        # GIVEN - Une natation avec durée zéro
        natation = Natation(
            id_activite=4,
            titre="Test",
            description="Test",
            date_activite=datetime.now(),
            lieu="Piscine",
            distance=2.0,
            id_user=1,
            type_nage="crawl",
            duree=0,
        )

        # WHEN
        vitesse = natation.vitesse()

        # THEN - La vitesse est 0 (évite division par zéro)
        assert vitesse == 0


class TestNatationString:
    """Tests de la représentation en chaîne"""

    def test_str_representation_crawl(self):
        # GIVEN - Une natation en crawl
        natation = Natation(
            id_activite=1,
            titre="Nage matinale énergisante",
            description="Réveil en douceur dans l'eau",
            date_activite=datetime(2025, 10, 31, 10, 0),
            lieu="Piscine",
            distance=2.0,
            id_user=1,
            type_nage="crawl",
            duree=60,
        )

        # WHEN - On appelle __str__
        resultat = str(natation)

        # THEN - La chaîne contient les infos importantes
        assert "crawl" in resultat
        assert "0.56" in resultat or "0.55" in resultat  # vitesse ~0.556 m/s
        assert "m/s" in resultat


class TestNatationHeritage:
    """Tests de l'héritage de AbstractActivity"""

    def test_heritage_abstract_activity(self):
        # GIVEN - Une natation
        natation = Natation(
            id_activite=1,
            titre="Test",
            description="Test",
            date_activite=datetime.now(),
            lieu="Piscine",
            distance=1.0,
            id_user=1,
            type_nage="crawl",
            duree=30,
        )

        # THEN - Elle hérite bien de AbstractActivity
        from business_object.Activity_object.abstract_activity import AbstractActivity

        assert isinstance(natation, AbstractActivity)
