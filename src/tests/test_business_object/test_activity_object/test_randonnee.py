import pytest
from datetime import datetime
from business_object.Activity_object.randonnee import Randonnee


class TestRandonneeCreation:
    """Tests de création d'une randonnée"""
    
    def test_creation_randonnee_complete(self):
        # GIVEN - Des données complètes pour une randonnée
        date = datetime(2025, 10, 31, 14, 30)
        
        # WHEN - On crée une randonnée
        randonnee = Randonnee(
            id_activite=1,
            titre="Randonnée en montagne",
            description="Belle balade",
            date_activite=date,
            lieu="Alpes",
            duree=120,  # 2 heures = 120 minutes
            distance=10.0,  # 10 km
            id_user=1,
            type_terrain="montagne"
        )
        
        # THEN - L'objet est correctement créé
        assert randonnee.id == 1
        assert randonnee.titre == "Randonnée en montagne"
        assert randonnee.description == "Belle balade"
        assert randonnee.date_activite == date
        assert randonnee.lieu == "Alpes"
        assert randonnee.duree == 120
        assert randonnee.distance == 10.0
        assert randonnee.id_user == 1
        assert randonnee.type_terrain == "montagne"
        assert randonnee.sport == "randonnee"
    
    def test_creation_randonnee_terrain_foret(self):
        # GIVEN - Une randonnée en forêt
        # WHEN
        randonnee = Randonnee(
            id_activite=2,
            titre="Balade en forêt",
            description="Sentier forestier",
            date_activite=datetime.now(),
            lieu="Forêt de Brocéliande",
            duree=90,
            distance=7.5,
            id_user=2,
            type_terrain="foret"
        )
        
        # THEN
        assert randonnee.type_terrain == "foret"
        assert randonnee.sport == "randonnee"
    
    def test_creation_randonnee_terrain_plaine(self):
        # GIVEN - Une randonnée en plaine
        # WHEN
        randonnee = Randonnee(
            id_activite=3,
            titre="Promenade champêtre",
            description="Sentier plat",
            date_activite=datetime.now(),
            lieu="Campagne",
            duree=60,
            distance=5.0,
            id_user=3,
            type_terrain="plaine"
        )
        
        # THEN
        assert randonnee.type_terrain == "plaine"


class TestRandonneeVitesse:
    """Tests du calcul de vitesse"""
    
    def test_vitesse_randonnee(self):
        # GIVEN - Une randonnée de 10 km en 2 heures (120 minutes)
        randonnee = Randonnee(
            id_activite=1,
            titre="Test",
            description="Test",
            date_activite=datetime.now(),
            lieu="Test",
            duree=120,
            distance=10.0,
            id_user=1,
            type_terrain="montagne"
        )
        
        # WHEN - On calcule la vitesse
        vitesse = randonnee.vitesse()
        
        # THEN - La vitesse est de 5 km/h
        assert vitesse == 5.0

    
    def test_vitesse_duree_zero(self):
        # GIVEN - Une randonnée avec durée zéro
        randonnee = Randonnee(
            id_activite=4,
            titre="Test",
            description="Test",
            date_activite=datetime.now(),
            lieu="Test",
            duree=0,
            distance=10.0,
            id_user=1,
            type_terrain="plaine"
        )
        
        # WHEN
        vitesse = randonnee.vitesse()
        
        # THEN - La vitesse est 0 (évite division par zéro)
        assert vitesse == 0
    
    def test_vitesse_duree_negative(self):
        # GIVEN - Une randonnée avec durée négative (cas d'erreur)
        randonnee = Randonnee(
            id_activite=5,
            titre="Test",
            description="Test",
            date_activite=datetime.now(),
            lieu="Test",
            duree=-60,
            distance=10.0,
            id_user=1,
            type_terrain="plaine"
        )
        
        # WHEN
        vitesse = randonnee.vitesse()
        
        # THEN - La vitesse est 0
        assert vitesse == 0

    
    def test_vitesse_tres_courte(self):
        # GIVEN - Une randonnée très courte
        randonnee = Randonnee(
            id_activite=7,
            titre="Test",
            description="Test",
            date_activite=datetime.now(),
            lieu="Test",
            duree=15,  # 15 minutes
            distance=1.5,
            id_user=1,
            type_terrain="plaine"
        )
        
        # WHEN
        vitesse = randonnee.vitesse()
        
        # THEN - La vitesse est de 6 km/h
        assert vitesse == pytest.approx(6.0, rel=1e-2)


class TestRandonneeString:
    """Tests de la représentation en chaîne"""
    
    def test_str_representation(self):
        # GIVEN - Une randonnée
        randonnee = Randonnee(
            id_activite=1,
            titre="Belle randonnée",
            description="Description test",
            date_activite=datetime(2025, 10, 31, 10, 0),
            lieu="Montagnes",
            duree=120,
            distance=10.0,
            id_user=1,
            type_terrain="montagne"
        )
        
        # WHEN - On appelle __str__
        resultat = str(randonnee)
        
        # THEN - La chaîne contient les infos importantes
        assert "Randonnée" in resultat
        assert "montagne" in resultat
        assert "5.00 km/h" in resultat
    
    def test_str_avec_vitesse_zero(self):
        # GIVEN - Une randonnée avec durée zéro
        randonnee = Randonnee(
            id_activite=2,
            titre="Test",
            description="Test",
            date_activite=datetime.now(),
            lieu="Test",
            duree=0,
            distance=10.0,
            id_user=1,
            type_terrain="plaine"
        )
        
        # WHEN
        resultat = str(randonnee)
        
        # THEN - La vitesse affichée est 0.00
        assert "0.00 km/h" in resultat
        assert "plaine" in resultat


class TestRandonneeEdgeCases:
    """Tests des cas limites"""
    
    def test_distance_zero(self):
        # GIVEN - Une randonnée sans distance
        randonnee = Randonnee(
            id_activite=1,
            titre="Test",
            description="Test",
            date_activite=datetime.now(),
            lieu="Test",
            duree=60,
            distance=0.0,
            id_user=1,
            type_terrain="plaine"
        )
        
        # WHEN
        vitesse = randonnee.vitesse()
        
        # THEN - La vitesse est 0
        assert vitesse == 0.0
    
    def test_tres_longue_randonnee(self):
        # GIVEN - Une randonnée très longue (ultra-trail)
        randonnee = Randonnee(
            id_activite=2,
            titre="Ultra-trail",
            description="Très long",
            date_activite=datetime.now(),
            lieu="Alpes",
            duree=1200,  # 20 heures
            distance=100.0,
            id_user=1,
            type_terrain="montagne"
        )
        
        # WHEN
        vitesse = randonnee.vitesse()
        
        # THEN - La vitesse est correctement calculée
        assert vitesse == pytest.approx(5.0, rel=1e-2)
    
    def test_type_terrain_vide(self):
        # GIVEN - Un type de terrain vide
        randonnee = Randonnee(
            id_activite=3,
            titre="Test",
            description="Test",
            date_activite=datetime.now(),
            lieu="Test",
            duree=60,
            distance=5.0,
            id_user=1,
            type_terrain=""
        )
        
        # THEN - L'objet est créé mais avec terrain vide
        assert randonnee.type_terrain == ""
        assert randonnee.vitesse() == pytest.approx(5.0, rel=1e-2)
    
    def test_valeurs_decimales_complexes(self):
        # GIVEN - Des valeurs décimales complexes
        randonnee = Randonnee(
            id_activite=4,
            titre="Test",
            description="Test",
            date_activite=datetime.now(),
            lieu="Test",
            duree=137.5,  # 2h17min30s
            distance=8.333,
            id_user=1,
            type_terrain="mixte"
        )
        
        # WHEN
        vitesse = randonnee.vitesse()
        
        # THEN - Le calcul est précis
        expected_vitesse = (8.333 / 137.5) * 60
        assert vitesse == pytest.approx(expected_vitesse, rel=1e-2)


class TestRandonneeHeritage:
    """Tests de l'héritage de AbstractActivity"""
    
    def test_heritage_abstract_activity(self):
        # GIVEN - Une randonnée
        randonnee = Randonnee(
            id_activite=1,
            titre="Test",
            description="Test",
            date_activite=datetime.now(),
            lieu="Test",
            duree=60,
            distance=5.0,
            id_user=1,
            type_terrain="montagne"
        )
        
        # THEN - Elle hérite bien de AbstractActivity
        from business_object.Activity_object.abstract_activity import AbstractActivity
        assert isinstance(randonnee, AbstractActivity)
    
    def test_attribut_sport_correct(self):
        # GIVEN - Une randonnée
        randonnee = Randonnee(
            id_activite=1,
            titre="Test",
            description="Test",
            date_activite=datetime.now(),
            lieu="Test",
            duree=60,
            distance=5.0,
            id_user=1,
            type_terrain="plaine"
        )
        
        # THEN - Le sport est automatiquement "randonnee"
        assert randonnee.sport == "randonnee"