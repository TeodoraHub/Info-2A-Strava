"""
Tests unitaires pour la classe Utilisateur
"""

import pytest
from unittest.mock import Mock, MagicMock, mock_open, patch
from datetime import datetime
import sys

# Mock des modules qui pourraient ne pas exister
sys.modules['dao.activite_dao'] = MagicMock()
sys.modules['business_object.Activity_object.abstract_activity'] = MagicMock()

from business_object.user_object.utilisateur import Utilisateur


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
        assert user.activites == []
        assert isinstance(user.activites, list)


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

    @patch("business_object.User_object.utilisateur.CoursePied")
    @patch("builtins.open", new_callable=mock_open, read_data="<gpx></gpx>")
    @patch("gpxpy.parse")
    def test_creer_activite_course_pied(self, mock_gpx_parse, mock_file, mock_course_pied):
        # GIVEN - Un utilisateur et des données de course à pied
        user = Utilisateur(1, "Runner", "runner@test.fr", "pass")
        mock_gpx = Mock()
        mock_gpx.length_3d.return_value = 5000.0
        mock_gpx.get_duration.return_value = 1800
        mock_gpx_parse.return_value = mock_gpx
        
        mock_activite = Mock()
        mock_activite.titre = "Morning Run"
        mock_activite.description = "Course matinale"
        mock_activite.distance = 5000.0
        mock_activite.duree = 1800
        mock_activite.id_user = 1
        mock_course_pied.return_value = mock_activite

        # WHEN - On crée une activité de course
        activite = user.creer_activite(
            type_activite="course",
            titre="Morning Run",
            description="Course matinale",
            lieu="Parc",
            fichier_gpx="test.gpx"
        )

        # THEN - Une activité CoursePied est créée
        assert activite.titre == "Morning Run"
        assert activite.description == "Course matinale"
        assert activite.distance == 5000.0
        assert activite.duree == 1800
        assert activite.id_user == 1
        mock_file.assert_called_once_with("test.gpx", "r", encoding="utf-8")
        mock_course_pied.assert_called_once()

    @patch("business_object.User_object.utilisateur.Cyclism")
    @patch("builtins.open", new_callable=mock_open, read_data="<gpx></gpx>")
    @patch("gpxpy.parse")
    def test_creer_activite_cyclisme(self, mock_gpx_parse, mock_file, mock_cyclism):
        # GIVEN - Un utilisateur et des données de cyclisme
        user = Utilisateur(2, "Cyclist", "cyclist@test.fr", "pass")
        mock_gpx = Mock()
        mock_gpx.length_3d.return_value = 30000.0
        mock_gpx.get_duration.return_value = 3600
        mock_gpx_parse.return_value = mock_gpx
        
        mock_activite = Mock()
        mock_activite.titre = "Sortie vélo"
        mock_activite.distance = 30000.0
        mock_activite.id_user = 2
        mock_cyclism.return_value = mock_activite

        # WHEN - On crée une activité de cyclisme avec type de vélo
        activite = user.creer_activite(
            type_activite="cyclisme",
            titre="Sortie vélo",
            description="Route de campagne",
            lieu="Campagne",
            fichier_gpx="velo.gpx",
            type_velo="route"
        )

        # THEN - Une activité Cyclism est créée
        assert activite.titre == "Sortie vélo"
        assert activite.distance == 30000.0
        assert activite.id_user == 2
        mock_cyclism.assert_called_once()

    @patch("business_object.User_object.utilisateur.Natation")
    @patch("builtins.open", new_callable=mock_open, read_data="<gpx></gpx>")
    @patch("gpxpy.parse")
    def test_creer_activite_natation(self, mock_gpx_parse, mock_file, mock_natation):
        # GIVEN - Un utilisateur et des données de natation
        user = Utilisateur(3, "Swimmer", "swim@test.fr", "pass")
        mock_gpx = Mock()
        mock_gpx.length_3d.return_value = 1000.0
        mock_gpx.get_duration.return_value = 1200
        mock_gpx_parse.return_value = mock_gpx
        
        mock_activite = Mock()
        mock_activite.titre = "Piscine"
        mock_activite.duree = 1200
        mock_activite.id_user = 3
        mock_natation.return_value = mock_activite

        # WHEN - On crée une activité de natation
        activite = user.creer_activite(
            type_activite="natation",
            titre="Piscine",
            description="Entraînement natation",
            lieu="Piscine municipale",
            fichier_gpx="natation.gpx",
            type_nage="crawl"
        )

        # THEN - Une activité Natation est créée
        assert activite.titre == "Piscine"
        assert activite.duree == 1200
        assert activite.id_user == 3
        mock_natation.assert_called_once()

    @patch("business_object.User_object.utilisateur.Randonnee")
    @patch("builtins.open", new_callable=mock_open, read_data="<gpx></gpx>")
    @patch("gpxpy.parse")
    def test_creer_activite_randonnee(self, mock_gpx_parse, mock_file, mock_randonnee):
        # GIVEN - Un utilisateur et des données de randonnée
        user = Utilisateur(4, "Hiker", "hiker@test.fr", "pass")
        mock_gpx = Mock()
        mock_gpx.length_3d.return_value = 10000.0
        mock_gpx.get_duration.return_value = 7200
        mock_gpx_parse.return_value = mock_gpx
        
        mock_activite = Mock()
        mock_activite.titre = "Montagne"
        mock_activite.distance = 10000.0
        mock_activite.id_user = 4
        mock_randonnee.return_value = mock_activite

        # WHEN - On crée une activité de randonnée
        activite = user.creer_activite(
            type_activite="randonnee",
            titre="Montagne",
            description="Randonnée en altitude",
            lieu="Alpes",
            fichier_gpx="rando.gpx",
            type_terrain="montagne"
        )

        # THEN - Une activité Randonnee est créée
        assert activite.titre == "Montagne"
        assert activite.distance == 10000.0
        assert activite.id_user == 4
        mock_randonnee.assert_called_once()

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
        with pytest.raises(ValueError, match="Type d'activité inconnu: invalid"):
            user.creer_activite(
                type_activite="invalid",
                titre="Test",
                description="Test",
                lieu="Test",
                fichier_gpx="test.gpx"
            )


class TestConsulterActivites:
    """Tests de la méthode consulter_activites"""

    @patch("business_object.User_object.utilisateur.Session")
    @patch("business_object.User_object.utilisateur.ActivityDAO")
    def test_consulter_activites_succes(self, mock_dao_class, mock_session_class):
        # GIVEN - Un utilisateur connecté avec une session DB
        user = Utilisateur(1, "Test", "test@test.fr", "pass")
        mock_session = Mock()
        mock_user = Mock()
        mock_user.db_session = Mock()
        mock_session.return_value.utilisateur = mock_user
        mock_session_class.return_value = mock_session.return_value
        
        mock_dao = Mock()
        mock_activites = [Mock(), Mock()]
        mock_dao.get_by_user.return_value = mock_activites
        mock_dao_class.return_value = mock_dao

        # WHEN - On consulte les activités
        activites = user.consulter_activites()

        # THEN - Les activités sont récupérées via le DAO
        assert activites == mock_activites
        mock_dao.get_by_user.assert_called_once_with(1)

    @patch("business_object.User_object.utilisateur.Session")
    def test_consulter_activites_pas_de_session(self, mock_session_class):
        # GIVEN - Aucun utilisateur connecté
        user = Utilisateur(1, "Test", "test@test.fr", "pass")
        mock_session = Mock()
        mock_session.return_value.utilisateur = None
        mock_session_class.return_value = mock_session.return_value

        # WHEN / THEN - Une exception est levée
        with pytest.raises(RuntimeError, match="Aucun utilisateur connecté"):
            user.consulter_activites()


class TestModifierActivite:
    """Tests de la méthode modifier_activite"""

    @patch("business_object.User_object.utilisateur.Session")
    @patch("business_object.User_object.utilisateur.ActivityDAO")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_modifier_activite_succes(self, mock_print, mock_input, mock_dao_class, mock_session_class):
        # GIVEN - Un utilisateur avec une activité existante
        user = Utilisateur(1, "Test", "test@test.fr", "pass")
        user.db_session = Mock()
        
        mock_session = Mock()
        mock_user = Mock()
        mock_user.db_session = user.db_session
        mock_session.return_value.utilisateur = mock_user
        mock_session_class.return_value = mock_session.return_value
        
        mock_activite = Mock()
        mock_activite.id = 100
        mock_activite.titre = "Ancien titre"
        mock_activite.description = "Ancienne description"
        
        mock_dao = Mock()
        mock_dao.get_by_user.return_value = [mock_activite]
        mock_dao_class.return_value = mock_dao
        
        mock_input.side_effect = ["100", "Nouveau titre", "Nouvelle description"]

        # WHEN - On modifie l'activité
        user.modifier_activite()

        # THEN - L'activité est modifiée et la session commit est appelée
        assert mock_activite.titre == "Nouveau titre"
        assert mock_activite.description == "Nouvelle description"
        user.db_session.commit.assert_called_once()

    @patch("business_object.User_object.utilisateur.Session")
    @patch("business_object.User_object.utilisateur.ActivityDAO")
    @patch("builtins.print")
    def test_modifier_activite_aucune_activite(self, mock_print, mock_dao_class, mock_session_class):
        # GIVEN - Un utilisateur sans activités
        user = Utilisateur(1, "Test", "test@test.fr", "pass")
        user.db_session = Mock()
        
        mock_session = Mock()
        mock_user = Mock()
        mock_user.db_session = user.db_session
        mock_session.return_value.utilisateur = mock_user
        mock_session_class.return_value = mock_session.return_value
        
        mock_dao = Mock()
        mock_dao.get_by_user.return_value = []
        mock_dao_class.return_value = mock_dao

        # WHEN - On tente de modifier une activité
        user.modifier_activite()

        # THEN - Un message est affiché et aucune modification n'est faite
        mock_print.assert_called_with("Aucune activité à modifier.")


class TestSupprimerActivite:
    """Tests de la méthode supprimer_activite"""

    @patch("business_object.User_object.utilisateur.Session")
    @patch("business_object.User_object.utilisateur.ActivityDAO")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_supprimer_activite_succes(self, mock_print, mock_input, mock_dao_class, mock_session_class):
        # GIVEN - Un utilisateur avec une activité à supprimer
        user = Utilisateur(1, "Test", "test@test.fr", "pass")
        user.db_session = Mock()
        
        mock_session = Mock()
        mock_user = Mock()
        mock_user.db_session = user.db_session
        mock_session.return_value.utilisateur = mock_user
        mock_session_class.return_value = mock_session.return_value
        
        mock_activite = Mock()
        mock_activite.id = 100
        mock_activite.titre = "Activité à supprimer"
        
        mock_dao = Mock()
        mock_dao.get_by_user.return_value = [mock_activite]
        mock_dao_class.return_value = mock_dao
        
        mock_input.return_value = "100"

        # WHEN - On supprime l'activité
        user.supprimer_activite()

        # THEN - L'activité est supprimée et la session commit est appelée
        user.db_session.delete.assert_called_once_with(mock_activite)
        user.db_session.commit.assert_called_once()

    @patch("business_object.User_object.utilisateur.Session")
    @patch("business_object.User_object.utilisateur.ActivityDAO")
    @patch("builtins.input")
    def test_supprimer_activite_id_invalide(self, mock_input, mock_dao_class, mock_session_class):
        # GIVEN - Un utilisateur avec une activité mais un ID invalide
        user = Utilisateur(1, "Test", "test@test.fr", "pass")
        user.db_session = Mock()
        
        mock_session = Mock()
        mock_user = Mock()
        mock_user.db_session = user.db_session
        mock_session.return_value.utilisateur = mock_user
        mock_session_class.return_value = mock_session.return_value
        
        mock_activite = Mock()
        mock_activite.id = 100
        
        mock_dao = Mock()
        mock_dao.get_by_user.return_value = [mock_activite]
        mock_dao_class.return_value = mock_dao
        
        mock_input.return_value = "999"

        # WHEN / THEN - Une exception est levée pour ID invalide
        with pytest.raises(ValueError, match="ID invalide : aucune activité correspondante"):
            user.supprimer_activite()


class TestSuivreUtilisateur:
    """Tests de la méthode suivre_utilisateur"""

    @patch("business_object.User_object.utilisateur.Session")
    @patch("business_object.User_object.utilisateur.SuiviDAO")
    def test_suivre_utilisateur_succes(self, mock_dao_class, mock_session_class):
        # GIVEN - Deux utilisateurs différents
        user1 = Utilisateur(1, "User1", "user1@test.fr", "pass")
        user2 = Utilisateur(2, "User2", "user2@test.fr", "pass")
        
        mock_session = Mock()
        mock_user = Mock()
        mock_user.id_user = 1
        mock_user.db_session = Mock()
        mock_session.return_value.utilisateur = mock_user
        mock_session_class.return_value = mock_session.return_value
        
        mock_dao = Mock()
        mock_dao.existe_suivi.return_value = False
        mock_dao_class.return_value = mock_dao

        # WHEN - User1 suit User2
        user1.suivre_utilisateur(user2)

        # THEN - Le suivi est ajouté
        mock_dao.existe_suivi.assert_called_once_with(1, 2)
        mock_dao.ajouter_suivi.assert_called_once_with(1, 2)

    @patch("business_object.User_object.utilisateur.Session")
    def test_suivre_utilisateur_soi_meme(self, mock_session_class):
        # GIVEN - Un utilisateur qui tente de se suivre lui-même
        user = Utilisateur(1, "User", "user@test.fr", "pass")
        
        mock_session = Mock()
        mock_user = Mock()
        mock_user.id_user = 1
        mock_session.return_value.utilisateur = mock_user
        mock_session_class.return_value = mock_session.return_value

        # WHEN / THEN - Une exception est levée
        with pytest.raises(ValueError, match="Impossible de se suivre soi-même"):
            user.suivre_utilisateur(user)

    @patch("business_object.User_object.utilisateur.Session")
    @patch("business_object.User_object.utilisateur.SuiviDAO")
    def test_suivre_utilisateur_deja_suivi(self, mock_dao_class, mock_session_class):
        # GIVEN - Deux utilisateurs avec un suivi existant
        user1 = Utilisateur(1, "User1", "user1@test.fr", "pass")
        user2 = Utilisateur(2, "User2", "user2@test.fr", "pass")
        
        mock_session = Mock()
        mock_user = Mock()
        mock_user.id_user = 1
        mock_user.db_session = Mock()
        mock_session.return_value.utilisateur = mock_user
        mock_session_class.return_value = mock_session.return_value
        
        mock_dao = Mock()
        mock_dao.existe_suivi.return_value = True
        mock_dao_class.return_value = mock_dao

        # WHEN / THEN - Une exception est levée
        with pytest.raises(ValueError, match="Utilisateur déjà suivi"):
            user1.suivre_utilisateur(user2)


class TestObtenerStatistiques:
    """Tests de la méthode obtenir_statistiques"""

    @patch("business_object.User_object.utilisateur.Session")
    @patch("business_object.User_object.utilisateur.Statistiques")
    def test_obtenir_statistiques_sans_filtre(self, mock_stats_class, mock_session_class):
        # GIVEN - Un utilisateur connecté
        user = Utilisateur(1, "User", "user@test.fr", "pass")
        
        mock_session = Mock()
        mock_user = Mock()
        mock_session.return_value.utilisateur = mock_user
        mock_session_class.return_value = mock_session.return_value
        
        mock_stats_class.nombre_activites.return_value = 10
        mock_stats_class.kilometres.return_value = 50.5
        mock_stats_class.heures_activite.return_value = 8.5

        # WHEN - On obtient les statistiques sans filtre
        stats = user.obtenir_statistiques()

        # THEN - Les statistiques sont retournées
        assert stats["nombre_activites"] == 10
        assert stats["kilometres"] == 50.5
        assert stats["heures"] == 8.5
        mock_stats_class.nombre_activites.assert_called_once_with(mock_user, None, None)

    @patch("business_object.User_object.utilisateur.Session")
    @patch("business_object.User_object.utilisateur.Statistiques")
    def test_obtenir_statistiques_avec_filtres(self, mock_stats_class, mock_session_class):
        # GIVEN - Un utilisateur connecté et des filtres
        user = Utilisateur(1, "User", "user@test.fr", "pass")
        
        mock_session = Mock()
        mock_user = Mock()
        mock_session.return_value.utilisateur = mock_user
        mock_session_class.return_value = mock_session.return_value
        
        mock_stats_class.nombre_activites.return_value = 5
        mock_stats_class.kilometres.return_value = 25.0
        mock_stats_class.heures_activite.return_value = 4.0

        # WHEN - On obtient les statistiques avec filtres
        stats = user.obtenir_statistiques(periode="7j", sport="course")

        # THEN - Les statistiques filtrées sont retournées
        assert stats["nombre_activites"] == 5
        assert stats["kilometres"] == 25.0
        assert stats["heures"] == 4.0
        mock_stats_class.nombre_activites.assert_called_once_with(mock_user, "7j", "course")
        mock_stats_class.kilometres.assert_called_once_with(mock_user, "7j", "course")
        mock_stats_class.heures_activite.assert_called_once_with(mock_user, "7j", "course")