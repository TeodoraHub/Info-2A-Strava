"""
Tests unitaires pour la classe ActivityService
"""

import sys
from datetime import timedelta
from unittest.mock import MagicMock, Mock, patch
import pytest

# Mock des modules AVANT l'import pour éviter les importations circulaires
sys.modules["dao.activite_dao"] = MagicMock()
sys.modules["dao.activity_model"] = MagicMock()

# Mock du décorateur log pour qu'il retourne la fonction sans modification
mock_log = MagicMock()
mock_log.side_effect = lambda f: f
sys.modules["utils.log_decorator"] = MagicMock(log=mock_log)

# Mock du Singleton pour qu'il se comporte comme une classe normale
sys.modules["utils.singleton"] = MagicMock(Singleton=type)

from service.activity_service import ActivityService


class TestActivityServiceInit:
    """Tests du constructeur de la classe ActivityService"""

    @patch("service.activity_service.ActivityDAO")
    def test_init_activity_service(self, mock_dao):
        # GIVEN - La classe ActivityService
        mock_dao_instance = Mock()
        mock_dao.return_value = mock_dao_instance

        # WHEN - On crée une instance du service
        service = ActivityService()

        # THEN - Le service est créé avec un DAO
        assert service.activity_dao is not None
        mock_dao.assert_called_once()


class TestNormalizeDuration:
    """Tests de la méthode _normalize_duration"""

    def test_normalize_duration_none(self):
        # GIVEN - Une valeur None
        service = ActivityService()

        # WHEN - On normalise None
        result = service._normalize_duration(None)

        # THEN - On obtient None
        assert result is None

    def test_normalize_duration_timedelta(self):
        # GIVEN - Un objet timedelta de 2 heures
        service = ActivityService()
        duration = timedelta(hours=2)

        # WHEN - On normalise le timedelta
        result = service._normalize_duration(duration)

        # THEN - On obtient 2.0 heures
        assert result == 2.0

    def test_normalize_duration_float(self):
        # GIVEN - Une valeur float
        service = ActivityService()
        duration = 3.5

        # WHEN - On normalise le float
        result = service._normalize_duration(duration)

        # THEN - On obtient la même valeur
        assert result == 3.5

    def test_normalize_duration_string_valid(self):
        # GIVEN - Une chaîne convertible en float
        service = ActivityService()
        duration = "1.5"

        # WHEN - On normalise la chaîne
        result = service._normalize_duration(duration)

        # THEN - On obtient un float
        assert result == 1.5

    def test_normalize_duration_invalid(self):
        # GIVEN - Une valeur invalide
        service = ActivityService()
        duration = "invalid"

        # WHEN - On normalise une valeur invalide
        result = service._normalize_duration(duration)

        # THEN - On obtient None
        assert result is None


class TestExtractDetailSport:
    """Tests de la méthode _extract_detail_sport"""

    def test_extract_detail_sport_avec_detail_sport(self):
        # GIVEN - Un objet avec un attribut detail_sport
        service = ActivityService()
        activity = Mock()
        activity.detail_sport = "trail"

        # WHEN - On extrait le détail sport
        result = service._extract_detail_sport(activity)

        # THEN - On obtient la valeur de detail_sport
        assert result == "trail"

    def test_extract_detail_sport_avec_type_velo(self):
        # GIVEN - Un objet avec un attribut type_velo
        service = ActivityService()
        activity = Mock()
        activity.detail_sport = None
        activity.type_velo = "route"

        # WHEN - On extrait le détail sport
        result = service._extract_detail_sport(activity)

        # THEN - On obtient la valeur de type_velo
        assert result == "route"

    def test_extract_detail_sport_avec_type_nage(self):
        # GIVEN - Un objet avec un attribut type_nage
        service = ActivityService()
        activity = Mock()
        activity.detail_sport = None
        activity.type_velo = None
        activity.type_nage = "crawl"

        # WHEN - On extrait le détail sport
        result = service._extract_detail_sport(activity)

        # THEN - On obtient la valeur de type_nage
        assert result == "crawl"

    def test_extract_detail_sport_avec_type_terrain(self):
        # GIVEN - Un objet avec un attribut type_terrain
        service = ActivityService()
        activity = Mock()
        activity.detail_sport = None
        activity.type_velo = None
        activity.type_nage = None
        activity.type_terrain = "montagne"

        # WHEN - On extrait le détail sport
        result = service._extract_detail_sport(activity)

        # THEN - On obtient la valeur de type_terrain
        assert result == "montagne"

    def test_extract_detail_sport_sans_detail(self):
        # GIVEN - Un objet sans détail sport
        service = ActivityService()
        activity = Mock(spec=[])

        # WHEN - On extrait le détail sport
        result = service._extract_detail_sport(activity)

        # THEN - On obtient None
        assert result is None


class TestCreerActivite:
    """Tests de la méthode creer_activite"""

    @patch("service.activity_service.ActivityDAO")
    def test_creer_activite_succes(self, mock_dao_class):
        # GIVEN - Un service et un objet activité valide
        mock_dao = Mock()
        mock_dao.save.return_value = Mock(id=1)
        mock_dao_class.return_value = mock_dao
        
        service = ActivityService()
        activity = Mock()
        activity.titre = "Course matinale"
        activity.description = "Belle course"
        activity.sport = "course"
        activity.date_activite = "2025-01-15"
        activity.lieu = "Parc"
        activity.distance = 5.0
        activity.duree = timedelta(hours=1)
        activity.id_user = 1
        activity.id = 10

        # WHEN - On crée l'activité
        result = service.creer_activite(activity)

        # THEN - L'activité est créée avec succès
        assert result is True
        mock_dao.save.assert_called_once()

    @patch("service.activity_service.ActivityDAO")
    def test_creer_activite_sans_id(self, mock_dao_class):
        # GIVEN - Un service et un objet activité sans id
        mock_dao = Mock()
        mock_dao.save.return_value = Mock(id=1)
        mock_dao_class.return_value = mock_dao
        
        service = ActivityService()
        activity = Mock(spec=[])
        activity.titre = "Natation"
        activity.sport = "natation"
        activity.date_activite = "2025-01-15"
        activity.id_user = 2

        # WHEN - On crée l'activité
        result = service.creer_activite(activity)

        # THEN - L'activité est créée sans id
        assert result is True


class TestCreerActiviteFromDict:
    """Tests de la méthode creer_activite_from_dict"""

    @patch("service.activity_service.ActivityDAO")
    @patch("service.activity_service.ActivityModel")
    def test_creer_activite_from_dict_succes(self, mock_model, mock_dao_class):
        # GIVEN - Un service et un dictionnaire valide
        mock_dao = Mock()
        mock_dao.save.return_value = Mock(id=1)
        mock_dao_class.return_value = mock_dao
        
        service = ActivityService()
        activity_data = {
            "id_activite": 1,
            "titre": "Vélo",
            "description": "Sortie vélo",
            "sport": "cyclisme",
            "date_activite": "2025-01-15",
            "lieu": "Campagne",
            "distance": 30.0,
            "duree": 2.0,
            "detail_sport": "route",
            "id_user": 1,
        }

        # WHEN - On crée l'activité depuis le dictionnaire
        result = service.creer_activite_from_dict(activity_data)

        # THEN - L'activité est créée avec succès
        assert result is True
        mock_dao.save.assert_called_once()

    @patch("service.activity_service.ActivityDAO")
    def test_creer_activite_from_dict_erreur(self, mock_dao_class):
        # GIVEN - Un service et un dictionnaire invalide
        mock_dao = Mock()
        mock_dao.save.side_effect = Exception("Erreur DB")
        mock_dao_class.return_value = mock_dao
        
        service = ActivityService()
        activity_data = {
            "titre": "Test",
            "sport": "course",
            "date_activite": "2025-01-15",
            "distance": 5.0,
            "id_user": 1,
        }

        # WHEN - On tente de créer l'activité
        result = service.creer_activite_from_dict(activity_data)

        # THEN - La création échoue
        assert result is False


class TestGetActiviteById:
    """Tests de la méthode get_activite_by_id"""

    @patch("service.activity_service.ActivityDAO")
    def test_get_activite_by_id_succes(self, mock_dao_class):
        # GIVEN - Un service et un ID d'activité existant
        mock_dao = Mock()
        mock_activity = Mock()
        mock_dao.get_by_id.return_value = mock_activity
        mock_dao_class.return_value = mock_dao
        
        service = ActivityService()

        # WHEN - On récupère l'activité
        result = service.get_activite_by_id(1)

        # THEN - L'activité est récupérée
        assert result == mock_activity
        mock_dao.get_by_id.assert_called_once_with(1)

    @patch("service.activity_service.ActivityDAO")
    def test_get_activite_by_id_erreur(self, mock_dao_class):
        # GIVEN - Un service et une erreur lors de la récupération
        mock_dao = Mock()
        mock_dao.get_by_id.side_effect = Exception("Erreur DB")
        mock_dao_class.return_value = mock_dao
        
        service = ActivityService()

        # WHEN - On tente de récupérer l'activité
        result = service.get_activite_by_id(999)

        # THEN - On obtient None
        assert result is None


class TestGetActivitesByUser:
    """Tests de la méthode get_activites_by_user"""

    @patch("service.activity_service.ActivityDAO")
    def test_get_activites_by_user_succes(self, mock_dao_class):
        # GIVEN - Un service et un ID utilisateur
        mock_dao = Mock()
        mock_activities = [Mock(), Mock()]
        mock_dao.get_by_user.return_value = mock_activities
        mock_dao_class.return_value = mock_dao
        
        service = ActivityService()

        # WHEN - On récupère les activités de l'utilisateur
        result = service.get_activites_by_user(1)

        # THEN - Les activités sont récupérées
        assert result == mock_activities
        mock_dao.get_by_user.assert_called_once_with(1, None)

    @patch("service.activity_service.ActivityDAO")
    def test_get_activites_by_user_avec_type(self, mock_dao_class):
        # GIVEN - Un service, un ID utilisateur et un type d'activité
        mock_dao = Mock()
        mock_activities = [Mock()]
        mock_dao.get_by_user.return_value = mock_activities
        mock_dao_class.return_value = mock_dao
        
        service = ActivityService()

        # WHEN - On récupère les activités filtrées par type
        result = service.get_activites_by_user(1, "course")

        # THEN - Les activités sont récupérées avec le filtre
        assert result == mock_activities
        mock_dao.get_by_user.assert_called_once_with(1, "course")

    @patch("service.activity_service.ActivityDAO")
    def test_get_activites_by_user_erreur(self, mock_dao_class):
        # GIVEN - Un service et une erreur lors de la récupération
        mock_dao = Mock()
        mock_dao.get_by_user.side_effect = Exception("Erreur DB")
        mock_dao_class.return_value = mock_dao
        
        service = ActivityService()

        # WHEN - On tente de récupérer les activités
        result = service.get_activites_by_user(1)

        # THEN - On obtient une liste vide
        assert result == []


class TestGetFeed:
    """Tests de la méthode get_feed"""

    @patch("service.activity_service.ActivityDAO")
    def test_get_feed_succes(self, mock_dao_class):
        # GIVEN - Un service et un ID utilisateur
        mock_dao = Mock()
        mock_feed = [Mock(), Mock(), Mock()]
        mock_dao.get_feed.return_value = mock_feed
        mock_dao_class.return_value = mock_dao
        
        service = ActivityService()

        # WHEN - On récupère le fil d'activités
        result = service.get_feed(1)

        # THEN - Le fil est récupéré
        assert result == mock_feed
        mock_dao.get_feed.assert_called_once_with(1)

    @patch("service.activity_service.ActivityDAO")
    def test_get_feed_erreur(self, mock_dao_class):
        # GIVEN - Un service et une erreur lors de la récupération
        mock_dao = Mock()
        mock_dao.get_feed.side_effect = Exception("Erreur DB")
        mock_dao_class.return_value = mock_dao
        
        service = ActivityService()

        # WHEN - On tente de récupérer le fil
        result = service.get_feed(1)

        # THEN - On obtient une liste vide
        assert result == []


class TestGetMonthlyActivities:
    """Tests de la méthode get_monthly_activities"""

    @patch("service.activity_service.ActivityDAO")
    def test_get_monthly_activities_succes(self, mock_dao_class):
        # GIVEN - Un service, un ID utilisateur et une période
        mock_dao = Mock()
        mock_activities = [Mock(), Mock()]
        mock_dao.get_monthly_activities.return_value = mock_activities
        mock_dao_class.return_value = mock_dao
        
        service = ActivityService()

        # WHEN - On récupère les activités mensuelles
        result = service.get_monthly_activities(1, 2025, 1)

        # THEN - Les activités sont récupérées
        assert result == mock_activities
        mock_dao.get_monthly_activities.assert_called_once_with(1, 2025, 1, None)

    @patch("service.activity_service.ActivityDAO")
    def test_get_monthly_activities_avec_type(self, mock_dao_class):
        # GIVEN - Un service, un ID utilisateur, une période et un type
        mock_dao = Mock()
        mock_activities = [Mock()]
        mock_dao.get_monthly_activities.return_value = mock_activities
        mock_dao_class.return_value = mock_dao
        
        service = ActivityService()

        # WHEN - On récupère les activités mensuelles filtrées
        result = service.get_monthly_activities(1, 2025, 1, "course")

        # THEN - Les activités sont récupérées avec le filtre
        assert result == mock_activities
        mock_dao.get_monthly_activities.assert_called_once_with(1, 2025, 1, "course")

    @patch("service.activity_service.ActivityDAO")
    def test_get_monthly_activities_erreur(self, mock_dao_class):
        # GIVEN - Un service et une erreur lors de la récupération
        mock_dao = Mock()
        mock_dao.get_monthly_activities.side_effect = Exception("Erreur DB")
        mock_dao_class.return_value = mock_dao
        
        service = ActivityService()

        # WHEN - On tente de récupérer les activités mensuelles
        result = service.get_monthly_activities(1, 2025, 1)

        # THEN - On obtient une liste vide
        assert result == []


class TestSupprimerActivite:
    """Tests de la méthode supprimer_activite"""

    @patch("service.activity_service.ActivityDAO")
    def test_supprimer_activite_succes(self, mock_dao_class):
        # GIVEN - Un service et un ID d'activité
        mock_dao = Mock()
        mock_dao.delete.return_value = True
        mock_dao_class.return_value = mock_dao
        
        service = ActivityService()

        # WHEN - On supprime l'activité
        result = service.supprimer_activite(1)

        # THEN - L'activité est supprimée
        assert result is True
        mock_dao.delete.assert_called_once_with(1)

    @patch("service.activity_service.ActivityDAO")
    def test_supprimer_activite_erreur(self, mock_dao_class):
        # GIVEN - Un service et une erreur lors de la suppression
        mock_dao = Mock()
        mock_dao.delete.side_effect = Exception("Erreur DB")
        mock_dao_class.return_value = mock_dao
        
        service = ActivityService()

        # WHEN - On tente de supprimer l'activité
        result = service.supprimer_activite(1)

        # THEN - La suppression échoue
        assert result is False


class TestModifierActivite:
    """Tests de la méthode modifier_activite"""

    @patch("service.activity_service.ActivityDAO")
    @patch("service.activity_service.ActivityModel")
    def test_modifier_activite_succes(self, mock_model, mock_dao_class):
        # GIVEN - Un service et un objet activité modifié
        mock_dao = Mock()
        mock_dao.delete.return_value = True
        mock_dao.save.return_value = Mock(id=1)
        mock_dao_class.return_value = mock_dao
        
        service = ActivityService()
        activity = Mock()
        activity.id = 1
        activity.titre = "Course modifiée"
        activity.description = "Nouvelle description"
        activity.sport = "course"
        activity.date_activite = "2025-01-15"
        activity.lieu = "Parc"
        activity.distance = 6.0
        activity.duree = timedelta(hours=1, minutes=15)
        activity.id_user = 1

        # WHEN - On modifie l'activité
        result = service.modifier_activite(activity)

        # THEN - L'activité est modifiée avec succès
        assert result is True
        mock_dao.delete.assert_called_once_with(1)
        mock_dao.save.assert_called_once()

    @patch("service.activity_service.ActivityDAO")
    def test_modifier_activite_sans_id(self, mock_dao_class):
        # GIVEN - Un service et un objet activité sans ID
        mock_dao = Mock()
        mock_dao_class.return_value = mock_dao
        
        service = ActivityService()
        activity = Mock(spec=[])
        activity.titre = "Test"
        activity.sport = "course"
        activity.date_activite = "2025-01-15"
        activity.id_user = 1

        # WHEN - On tente de modifier l'activité
        result = service.modifier_activite(activity)

        # THEN - La modification échoue
        assert result is False

    @patch("service.activity_service.ActivityDAO")
    def test_modifier_activite_erreur_delete(self, mock_dao_class):
        # GIVEN - Un service et une erreur lors de la suppression
        mock_dao = Mock()
        mock_dao.delete.return_value = False
        mock_dao_class.return_value = mock_dao
        
        service = ActivityService()
        activity = Mock()
        activity.id = 1
        activity.titre = "Test"
        activity.sport = "course"
        activity.date_activite = "2025-01-15"
        activity.id_user = 1

        # WHEN - On tente de modifier l'activité
        result = service.modifier_activite(activity)

        # THEN - La modification échoue
        assert result is False


class TestModifierActiviteFromDict:
    """Tests de la méthode modifier_activite_from_dict"""

    @patch("service.activity_service.ActivityDAO")
    @patch("service.activity_service.ActivityModel")
    def test_modifier_activite_from_dict_succes(self, mock_model, mock_dao_class):
        # GIVEN - Un service et un dictionnaire valide
        mock_dao = Mock()
        mock_dao.delete.return_value = True
        mock_dao.save.return_value = Mock(id=1)
        mock_dao_class.return_value = mock_dao
        
        service = ActivityService()
        activity_data = {
            "id_activite": 1,
            "titre": "Vélo modifié",
            "description": "Nouvelle sortie",
            "sport": "cyclisme",
            "date_activite": "2025-01-15",
            "lieu": "Route",
            "distance": 35.0,
            "duree": 2.5,
            "detail_sport": "route",
            "id_user": 1,
        }

        # WHEN - On modifie l'activité depuis le dictionnaire
        result = service.modifier_activite_from_dict(activity_data)

        # THEN - L'activité est modifiée avec succès
        assert result is True
        mock_dao.delete.assert_called_once_with(1)
        mock_dao.save.assert_called_once()

    @patch("service.activity_service.ActivityDAO")
    def test_modifier_activite_from_dict_sans_id(self, mock_dao_class):
        # GIVEN - Un service et un dictionnaire sans ID
        mock_dao = Mock()
        mock_dao_class.return_value = mock_dao
        
        service = ActivityService()
        activity_data = {
            "titre": "Test",
            "sport": "course",
            "date_activite": "2025-01-15",
            "distance": 5.0,
            "id_user": 1,
        }

        # WHEN - On tente de modifier l'activité
        result = service.modifier_activite_from_dict(activity_data)

        # THEN - La modification échoue
        assert result is False

    @patch("service.activity_service.ActivityDAO")
    def test_modifier_activite_from_dict_erreur(self, mock_dao_class):
        # GIVEN - Un service et une erreur lors de la modification
        mock_dao = Mock()
        mock_dao.delete.side_effect = Exception("Erreur DB")
        mock_dao_class.return_value = mock_dao
        
        service = ActivityService()
        activity_data = {
            "id_activite": 1,
            "titre": "Test",
            "sport": "course",
            "date_activite": "2025-01-15",
            "distance": 5.0,
            "id_user": 1,
        }

        # WHEN - On tente de modifier l'activité
        result = service.modifier_activite_from_dict(activity_data)

        # THEN - La modification échoue
        assert result is False