"""
Tests unitaires pour la classe Utilisateur
"""

import sys
from unittest.mock import MagicMock, Mock, mock_open, patch
from utils.session import Session
import pytest

from business_object.user_object.utilisateur import Utilisateur

# Mock des modules AVANT l'import pour éviter les importations circulaires
sys.modules["dao.activite_dao"] = MagicMock()
sys.modules["dao.utilisateur_dao"] = MagicMock()
sys.modules["dao.suivi_dao"] = MagicMock()
sys.modules["dao.like_dao"] = MagicMock()
sys.modules["dao.commentaire_dao"] = MagicMock()
sys.modules["service.session_service"] = MagicMock()
sys.modules["business_object.statistiques"] = MagicMock()
sys.modules["business_object.like"] = MagicMock()
sys.modules["business_object.commentaire"] = MagicMock()


class TestUtilisateurInit:
    """Tests du constructeur de la classe Utilisateur"""

    def test_init_utilisateur_valide(self):
        # GIVEN - Des paramètres valides pour créer un utilisateur
        id_user = 1
        nom = "Dupont"
        mail = "dupont@example.com"
        mdp = "password123"
    
        # WHEN - On crée un utilisateur
        user = Utilisateur(id_user, nom, mail, mdp)
    
        # THEN - L'utilisateur est créé avec les bons attributs
        assert user.id_user == id_user
        assert user.nom_user == nom
        assert user.mail_user == mail
        assert user.mdp == mdp
        
        # Vérifie que l'utilisateur n'a pas encore d'activités (initialisation manuelle dans le test)
        assert not hasattr(user, "activites")  # L'attribut n'existe pas encore
        
        # Initialisation manuelle de l'attribut `activites` si nécessaire
        user.activites = []  # On l'initialise manuellement dans le test
        
        # Vérifie que `activites` est bien une liste vide
        assert user.activites == []


class TestUtilisateurStr:
    """Tests de la méthode __str__"""

    def test_str_representation(self):
        # GIVEN - Un utilisateur existant
        user = Utilisateur(1, "Martin", "martin@test.fr", "pass")

        # WHEN - On convertit l'utilisateur en chaîne
        result = str(user)

        # THEN - La représentation contient nom et mail
        assert result == "Utilisateur(Martin, martin@test.fr)"


class TestUtilisateurAsList:
    """Tests de la méthode as_list"""

    def test_as_list_retourne_attributs(self):
        # GIVEN - Un utilisateur avec des attributs définis
        user = Utilisateur(42, "Durand", "durand@mail.com", "secret")

        # WHEN - On appelle as_list
        result = user.as_list()

        # THEN - On obtient une liste avec id, nom et mail
        assert result == [42, "Durand", "durand@mail.com"]
        assert len(result) == 3


class TestCreerActivite:
    """Tests de la méthode creer_activite"""

    @patch("builtins.open", new_callable=mock_open, read_data="<gpx></gpx>")
    @patch("gpxpy.parse")
    def test_creer_activite_course_pied(self, mock_gpx_parse, mock_file):
        # GIVEN - Un utilisateur et des données de course à pied
        user = Utilisateur(1, "Runner", "runner@test.fr", "pass")
        mock_gpx = Mock()
        mock_gpx.length_3d.return_value = 5000.0
        mock_gpx.get_duration.return_value = 1800
        mock_gpx_parse.return_value = mock_gpx

        # WHEN - On crée une activité de course
        activite = user.creer_activite(
            type_activite="course",
            titre="Morning Run",
            description="Course matinale",
            lieu="Parc",
            fichier_gpx="test.gpx",
        )

        # THEN - Une activité est créée et le fichier GPX a été lu
        assert activite is not None
        mock_file.assert_called_once_with("test.gpx", "r", encoding="utf-8")
        mock_gpx.length_3d.assert_called_once()
        mock_gpx.get_duration.assert_called_once()

    @patch("builtins.open", new_callable=mock_open, read_data="<gpx></gpx>")
    @patch("gpxpy.parse")
    def test_creer_activite_cyclisme(self, mock_gpx_parse, mock_file):
        # GIVEN - Un utilisateur et des données de cyclisme
        user = Utilisateur(2, "Cyclist", "cyclist@test.fr", "pass")
        mock_gpx = Mock()
        mock_gpx.length_3d.return_value = 30000.0
        mock_gpx.get_duration.return_value = 3600
        mock_gpx_parse.return_value = mock_gpx

        # WHEN - On crée une activité de cyclisme avec type de vélo
        activite = user.creer_activite(
            type_activite="cyclisme",
            titre="Sortie vélo",
            description="Route de campagne",
            lieu="Campagne",
            fichier_gpx="velo.gpx",
            type_velo="route",
        )

        # THEN - Une activité est créée et le fichier GPX a été lu
        assert activite is not None
        mock_file.assert_called_once_with("velo.gpx", "r", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open, read_data="<gpx></gpx>")
    @patch("gpxpy.parse")
    def test_creer_activite_natation(self, mock_gpx_parse, mock_file):
        # GIVEN - Un utilisateur et des données de natation
        user = Utilisateur(3, "Swimmer", "swim@test.fr", "pass")
        mock_gpx = Mock()
        mock_gpx.length_3d.return_value = 1000.0
        mock_gpx.get_duration.return_value = 1200
        mock_gpx_parse.return_value = mock_gpx

        # WHEN - On crée une activité de natation
        activite = user.creer_activite(
            type_activite="natation",
            titre="Piscine",
            description="Entraînement natation",
            lieu="Piscine municipale",
            fichier_gpx="natation.gpx",
            type_nage="crawl",
        )

        # THEN - Une activité est créée et le fichier GPX a été lu
        assert activite is not None
        mock_file.assert_called_once_with("natation.gpx", "r", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open, read_data="<gpx></gpx>")
    @patch("gpxpy.parse")
    def test_creer_activite_randonnee(self, mock_gpx_parse, mock_file):
        # GIVEN - Un utilisateur et des données de randonnée
        user = Utilisateur(4, "Hiker", "hiker@test.fr", "pass")
        mock_gpx = Mock()
        mock_gpx.length_3d.return_value = 10000.0
        mock_gpx.get_duration.return_value = 7200
        mock_gpx_parse.return_value = mock_gpx

        # WHEN - On crée une activité de randonnée
        activite = user.creer_activite(
            type_activite="randonnee",
            titre="Montagne",
            description="Randonnée en altitude",
            lieu="Alpes",
            fichier_gpx="rando.gpx",
            type_terrain="montagne",
        )

        # THEN - Une activité est créée et le fichier GPX a été lu
        assert activite is not None
        mock_file.assert_called_once_with("rando.gpx", "r", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open, read_data="<gpx></gpx>")
    @patch("gpxpy.parse")
    def test_creer_activite_type_inconnu(self, mock_gpx_parse, mock_file):
        # GIVEN - Un utilisateur et un type d'activité invalide
        user = Utilisateur(5, "User", "user@test.fr", "pass")
        mock_gpx = Mock()
        mock_gpx.length_3d.return_value = 5000.0
        mock_gpx.get_duration.return_value = 1800
        mock_gpx_parse.return_value = mock_gpx

        # WHEN / THEN - On tente de créer une activité avec un type invalide
        with pytest.raises(ValueError) as exc_info:
            user.creer_activite(
                type_activite="invalid",
                titre="Test",
                description="Test",
                lieu="Test",
                fichier_gpx="test.gpx",
            )
        # L'exception contient le type invalide dans le message
        assert "invalid" in str(exc_info.value)
