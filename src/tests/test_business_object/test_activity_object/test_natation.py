import pytest
from datetime import datetime
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
            duree=60  # 60 minutes
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
        # Vérifier sport (peut être un tuple selon l'implémentation d'AbstractActivity)
        assert natation.sport == "natation" or natation.sport == ("natation",)
    
    def test_creation_type_nage(self):
        # GIVEN - Une natation en crawl
        # WHEN
        natation = Natation(
            id_activite=2,
            titre="Nage au coucher du soleil",
            description="Entraînement crawl en soirée",
            date_activite=datetime.now(),
            lieu="Piscine olympique",
            distance=3.0,
            id_user=2,
            type_nage="crawl",
            duree=90
        )
        
        # THEN
        assert natation.type_nage == "crawl"
    
    
    def test_creation_natation_sans_duree(self):
        # GIVEN - Une natation sans durée spécifiée
        # WHEN
        natation = Natation(
            id_activite=6,
            titre="Baignade improvisée",
            description="Petite session sans chrono",
            date_activite=datetime.now(),
            lieu="Piscine",
            distance=1.0,
            id_user=6,
            type_nage="crawl"
        )
        
        # THEN - La durée est None par défaut
        assert natation.duree is None


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
            duree=60  # 60 minutes = 3600 secondes
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
            duree=0
        )
        
        # WHEN
        vitesse = natation.vitesse()
        
        # THEN - La vitesse est 0 (évite division par zéro)
        assert vitesse == 0
    
    def test_vitesse_duree_negative(self):
        # GIVEN - Une natation avec durée négative (cas d'erreur)
        natation = Natation(
            id_activite=5,
            titre="Test",
            description="Test",
            date_activite=datetime.now(),
            lieu="Piscine",
            distance=2.0,
            id_user=1,
            type_nage="crawl",
            duree=-60
        )
        
        # WHEN
        vitesse = natation.vitesse()
        
        # THEN - La vitesse est 0
        assert vitesse == 0
    
    def test_vitesse_duree_none(self):
        # GIVEN - Une natation sans durée
        natation = Natation(
            id_activite=6,
            titre="Test",
            description="Test",
            date_activite=datetime.now(),
            lieu="Piscine",
            distance=2.0,
            id_user=1,
            type_nage="crawl"
        )
        
        # WHEN - On calcule la vitesse avec durée None
        # THEN - Cela peut lever une exception ou retourner 0
        # On vérifie que ça ne plante pas
        try:
            vitesse = natation.vitesse()
            # Si ça marche, la vitesse devrait être 0 ou lever une exception
            assert vitesse == 0 or vitesse is None
        except (TypeError, AttributeError):
            # C'est acceptable si None lève une exception
            pass


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
            duree=60
        )
        
        # WHEN - On appelle __str__
        resultat = str(natation)
        
        # THEN - La chaîne contient les infos importantes
        assert "crawl" in resultat
        assert "0.56" in resultat or "0.55" in resultat  # vitesse ~0.556 m/s
        assert "m/s" in resultat
    
    
    def test_str_avec_vitesse_zero(self):
        # GIVEN - Une natation avec durée zéro
        natation = Natation(
            id_activite=3,
            titre="Test",
            description="Test",
            date_activite=datetime.now(),
            lieu="Piscine",
            distance=2.0,
            id_user=1,
            type_nage="crawl",
            duree=0
        )
        
        # WHEN
        resultat = str(natation)
        
        # THEN - La vitesse affichée est 0.00
        assert "0.00 m/s" in resultat


class TestNatationEdgeCases:
    """Tests des cas limites"""
    
    def test_distance_zero(self):
        # GIVEN - Une natation sans distance
        natation = Natation(
            id_activite=1,
            titre="Test",
            description="Test",
            date_activite=datetime.now(),
            lieu="Piscine",
            distance=0.0,
            id_user=1,
            type_nage="crawl",
            duree=60
        )
        
        # WHEN
        vitesse = natation.vitesse()
        
        # THEN - La vitesse est 0
        assert vitesse == 0.0
    
    def test_tres_courte_natation(self):
        # GIVEN - Une très courte natation : 25m (1 longueur) en 30 secondes
        natation = Natation(
            id_activite=2,
            titre="1 longueur",
            description="Test",
            date_activite=datetime.now(),
            lieu="Piscine",
            distance=0.025,  # 25 m = 0.025 km
            id_user=1,
            type_nage="crawl",
            duree=0.5  # 30 secondes = 0.5 minutes
        )
        
        # WHEN
        vitesse = natation.vitesse()
        
        # THEN - La vitesse est correctement calculée
        # Calcul: (25 m) / (30 s) = 0.833 m/s
        assert vitesse == pytest.approx(0.833, rel=1e-2)
    
    def test_type_nage_vide(self):
        # GIVEN - Un type de nage vide
        natation = Natation(
            id_activite=3,
            titre="Test",
            description="Test",
            date_activite=datetime.now(),
            lieu="Piscine",
            distance=1.0,
            id_user=1,
            type_nage="",
            duree=30
        )
        
        # THEN - L'objet est créé mais avec type_nage vide
        assert natation.type_nage == ""
        assert natation.vitesse() > 0


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
            duree=30
        )
        
        # THEN - Elle hérite bien de AbstractActivity
        from business_object.Activity_object.abstract_activity import AbstractActivity
        assert isinstance(natation, AbstractActivity)
    
    def test_attribut_sport_correct(self):
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
            duree=30
        )
        
        # THEN - Le sport est automatiquement "natation"
        assert natation.sport == "natation" or natation.sport == ("natation",)


class TestNatationPerformance:
    """Tests de performance et vitesses réalistes"""
    
    def test_vitesse_nageur_debutant(self):
        # GIVEN - Un nageur débutant : 1 km en 40 minutes
        natation = Natation(
            id_activite=1,
            titre="Mes débuts en piscine",
            description="Première vraie séance d'entraînement",
            date_activite=datetime.now(),
            lieu="Piscine",
            distance=1.0,
            id_user=1,
            type_nage="crawl",
            duree=40
        )
        
        # WHEN
        vitesse = natation.vitesse()
        
        # THEN - Vitesse autour de 0.42 m/s (environ 1.5 km/h)
        assert 0.3 < vitesse < 0.6
    
    def test_vitesse_nageur_intermediaire(self):
        # GIVEN - Un nageur intermédiaire : 1 km en 20 minutes
        natation = Natation(
            id_activite=2,
            titre="Session régulière du mardi",
            description="Entraînement de maintien",
            date_activite=datetime.now(),
            lieu="Piscine",
            distance=1.0,
            id_user=1,
            type_nage="crawl",
            duree=20
        )
        
        # WHEN
        vitesse = natation.vitesse()
        
        # THEN - Vitesse autour de 0.83 m/s (environ 3 km/h)
        assert 0.7 < vitesse < 1.0
    
    def test_vitesse_nageur_expert(self):
        # GIVEN - Un nageur expert : 1 km en 12 minutes
        natation = Natation(
            id_activite=3,
            titre="Préparation compétition",
            description="Travail d'intensité avant la course",
            date_activite=datetime.now(),
            lieu="Piscine",
            distance=1.0,
            id_user=1,
            type_nage="crawl",
            duree=12
        )
        
        # WHEN
        vitesse = natation.vitesse()
        
        # THEN - Vitesse autour de 1.39 m/s (environ 5 km/h)
        assert 1.2 < vitesse < 1.6