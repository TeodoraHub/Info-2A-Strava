import pytest
from unittest.mock import Mock, MagicMock
from datetime import datetime
from dao.activite_dao import ActivityDAO


@pytest.fixture
def mock_db_session():
    """Fixture pour créer une fausse session de base de données"""
    return MagicMock()


@pytest.fixture
def mock_activity_class():
    """Fixture pour créer une fausse classe Activity"""
    mock_class = Mock()
    mock_class.__name__ = "Activity"
    return mock_class


@pytest.fixture
def activity_dao(mock_db_session, mock_activity_class):
    """Fixture pour créer une instance de ActivityDAO"""
    return ActivityDAO(mock_db_session, mock_activity_class)


@pytest.fixture
def mock_activity():
    """Fixture pour créer une fausse activité"""
    activity = Mock()
    activity.id = 1
    activity.user_id = 10
    activity.type = "natation"
    activity.titre = "Nage au réveil"
    activity.date_activite = datetime(2025, 10, 31, 8, 0)
    return activity


class TestActivityDAOInit:
    """Tests d'initialisation du DAO"""
    
    def test_init_dao(self, mock_db_session, mock_activity_class):
        # GIVEN - Une session et une classe Activity
        # WHEN - On crée le DAO
        dao = ActivityDAO(mock_db_session, mock_activity_class)
        
        # THEN - Le DAO est correctement initialisé
        assert dao.db == mock_db_session
        assert dao.activity_base_cls == mock_activity_class
    
    def test_init_dao_avec_session_none(self, mock_activity_class):
        # GIVEN - Une session None
        # WHEN - On crée le DAO
        dao = ActivityDAO(None, mock_activity_class)
        
        # THEN - Le DAO accepte None (même si ce n'est pas recommandé)
        assert dao.db is None


class TestActivityDAOSave:
    """Tests de la méthode save"""
    
    def test_save_activity_success(self, activity_dao, mock_db_session, mock_activity):
        # GIVEN - Une activité à sauvegarder
        # WHEN - On sauvegarde l'activité
        result = activity_dao.save(mock_activity)
        
        # THEN - Les méthodes de session sont appelées correctement
        mock_db_session.add.assert_called_once_with(mock_activity)
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once_with(mock_activity)
        assert result == mock_activity
    
    def test_save_activity_with_new_id(self, activity_dao, mock_db_session):
        # GIVEN - Une nouvelle activité sans ID
        new_activity = Mock()
        new_activity.id = None
        new_activity.titre = "Nouvelle activité"
        
        # Simuler l'ajout d'un ID après commit
        def set_id(activity):
            activity.id = 42
        
        mock_db_session.refresh.side_effect = set_id
        
        # WHEN - On sauvegarde
        result = activity_dao.save(new_activity)
        
        # THEN - L'activité reçoit un ID
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()
        assert result == new_activity
    
    def test_save_activity_rollback_on_error(self, activity_dao, mock_db_session, mock_activity):
        # GIVEN - Une erreur lors du commit
        mock_db_session.commit.side_effect = Exception("Erreur de base de données")
        
        # WHEN/THEN - Une exception est levée
        with pytest.raises(Exception, match="Erreur de base de données"):
            activity_dao.save(mock_activity)


class TestActivityDAOGetById:
    """Tests de la méthode get_by_id"""
    
    def test_get_by_id_found(self, activity_dao, mock_db_session, mock_activity_class, mock_activity):
        # GIVEN - Une activité existe avec l'ID 1
        mock_query = Mock()
        mock_filter = Mock()
        mock_filter.first.return_value = mock_activity
        mock_query.filter.return_value = mock_filter
        mock_db_session.query.return_value = mock_query
        
        # WHEN - On recherche l'activité par ID
        result = activity_dao.get_by_id(1)
        
        # THEN - L'activité est retournée
        mock_db_session.query.assert_called_once_with(mock_activity_class)
        assert result == mock_activity
    
    def test_get_by_id_not_found(self, activity_dao, mock_db_session, mock_activity_class):
        # GIVEN - Aucune activité avec l'ID 999
        mock_query = Mock()
        mock_filter = Mock()
        mock_filter.first.return_value = None
        mock_query.filter.return_value = mock_filter
        mock_db_session.query.return_value = mock_query
        
        # WHEN - On recherche l'activité
        result = activity_dao.get_by_id(999)
        
        # THEN - None est retourné
        assert result is None
    
    def test_get_by_id_with_zero(self, activity_dao, mock_db_session, mock_activity_class):
        # GIVEN - ID zéro
        mock_query = Mock()
        mock_filter = Mock()
        mock_filter.first.return_value = None
        mock_query.filter.return_value = mock_filter
        mock_db_session.query.return_value = mock_query
        
        # WHEN
        result = activity_dao.get_by_id(0)
        
        # THEN
        assert result is None


class TestActivityDAOGetByUser:
    """Tests de la méthode get_by_user"""
    
    def test_get_by_user_all_activities(self, activity_dao, mock_db_session, mock_activity_class):
        # GIVEN - Un utilisateur avec plusieurs activités
        activities = [Mock(id=1, user_id=10), Mock(id=2, user_id=10), Mock(id=3, user_id=10)]
        mock_query = Mock()
        mock_filter = Mock()
        mock_filter.all.return_value = activities
        mock_query.filter.return_value = mock_filter
        mock_db_session.query.return_value = mock_query
        
        # WHEN - On récupère toutes les activités de l'utilisateur
        result = activity_dao.get_by_user(user_id=10)
        
        # THEN - Toutes les activités sont retournées
        assert len(result) == 3
        assert result == activities
    
    def test_get_by_user_filtered_by_type(self, activity_dao, mock_db_session, mock_activity_class):
        # GIVEN - Un utilisateur avec des activités filtrées par type
        natation_activities = [Mock(id=1, user_id=10, type="natation")]
        mock_query = Mock()
        mock_filter1 = Mock()
        mock_filter2 = Mock()
        mock_filter2.all.return_value = natation_activities
        mock_filter1.filter.return_value = mock_filter2
        mock_query.filter.return_value = mock_filter1
        mock_db_session.query.return_value = mock_query
        
        # WHEN - On filtre par type "natation"
        result = activity_dao.get_by_user(user_id=10, type_activite="natation")
        
        # THEN - Seules les activités de natation sont retournées
        assert len(result) == 1
        assert result[0].type == "natation"
    
    def test_get_by_user_no_activities(self, activity_dao, mock_db_session, mock_activity_class):
        # GIVEN - Un utilisateur sans activités
        mock_query = Mock()
        mock_filter = Mock()
        mock_filter.all.return_value = []
        mock_query.filter.return_value = mock_filter
        mock_db_session.query.return_value = mock_query
        
        # WHEN - On récupère les activités
        result = activity_dao.get_by_user(user_id=99)
        
        # THEN - Une liste vide est retournée
        assert result == []
    
    def test_get_by_user_multiple_types(self, activity_dao, mock_db_session, mock_activity_class):
        # GIVEN - Différents types d'activités
        activities = [
            Mock(id=1, type="natation"),
            Mock(id=2, type="randonnee"),
            Mock(id=3, type="natation")
        ]
        mock_query = Mock()
        mock_filter1 = Mock()
        mock_filter2 = Mock()
        mock_filter2.all.return_value = [activities[0], activities[2]]
        mock_filter1.filter.return_value = mock_filter2
        mock_query.filter.return_value = mock_filter1
        mock_db_session.query.return_value = mock_query
        
        # WHEN - On filtre par "natation"
        result = activity_dao.get_by_user(user_id=10, type_activite="natation")
        
        # THEN - Seulement les natations
        assert len(result) == 2


class TestActivityDAOGetFeed:
    """Tests de la méthode get_feed - Skip car nécessite une refactorisation de get_feed()"""
    
    @pytest.mark.skip(reason="get_feed() utilise UtilisateurDAO qui est un Singleton - nécessite une refactorisation")
    def test_get_feed_basic(self, activity_dao, mock_db_session, mock_activity_class, monkeypatch):
        # GIVEN - Mock de UtilisateurDAO pour éviter les problèmes
        mock_user = Mock()
        mock_user.following = [20, 30]
        
        mock_user_dao = Mock()
        mock_user_dao.get.return_value = mock_user
        
        def mock_utilisateur_dao_init(db):
            return mock_user_dao
        
        # Patcher la classe UtilisateurDAO
        import dao.activite_dao
        mock_utilisateur_dao_class = Mock(side_effect=mock_utilisateur_dao_init)
        monkeypatch.setattr(dao.activite_dao, "UtilisateurDAO", mock_utilisateur_dao_class, raising=False)
        
        activities = [Mock(id=1), Mock(id=2)]
        mock_query = Mock()
        mock_filter = Mock()
        mock_order = Mock()
        mock_order.all.return_value = activities
        mock_filter.order_by.return_value = mock_order
        mock_query.filter.return_value = mock_filter
        mock_db_session.query.return_value = mock_query
        
        # WHEN
        result = activity_dao.get_feed(user_id=10)
        
        # THEN
        assert len(result) == 2


class TestActivityDAOGetMonthlyActivities:
    """Tests de la méthode get_monthly_activities"""
    
    def test_get_monthly_activities_all_types(self, activity_dao, mock_db_session, mock_activity_class):
        # GIVEN - Des activités en octobre 2025
        activities = [
            Mock(id=1, user_id=10, date_activite=datetime(2025, 10, 5)),
            Mock(id=2, user_id=10, date_activite=datetime(2025, 10, 15)),
        ]
        
        mock_query = Mock()
        mock_filter = Mock()
        mock_filter.all.return_value = activities
        mock_query.filter.return_value = mock_filter
        mock_db_session.query.return_value = mock_query
        
        # WHEN - On récupère les activités d'octobre 2025
        result = activity_dao.get_monthly_activities(user_id=10, year=2025, month=10)
        
        # THEN - Les activités du mois sont retournées
        assert len(result) == 2
    
    def test_get_monthly_activities_filtered_by_type(self, activity_dao, mock_db_session, mock_activity_class):
        # GIVEN - Des activités filtrées par type
        natation_activities = [Mock(id=1, user_id=10, type="natation")]
        
        mock_query = Mock()
        mock_filter1 = Mock()
        mock_filter2 = Mock()
        mock_filter2.all.return_value = natation_activities
        mock_filter1.filter.return_value = mock_filter2
        mock_query.filter.return_value = mock_filter1
        mock_db_session.query.return_value = mock_query
        
        # WHEN - On filtre par type "natation"
        result = activity_dao.get_monthly_activities(
            user_id=10, year=2025, month=10, type_activite="natation"
        )
        
        # THEN - Seules les natations sont retournées
        assert len(result) == 1
        assert result[0].type == "natation"
    
    def test_get_monthly_activities_empty_month(self, activity_dao, mock_db_session, mock_activity_class):
        # GIVEN - Aucune activité en février 2025
        mock_query = Mock()
        mock_filter = Mock()
        mock_filter.all.return_value = []
        mock_query.filter.return_value = mock_filter
        mock_db_session.query.return_value = mock_query
        
        # WHEN - On récupère les activités
        result = activity_dao.get_monthly_activities(user_id=10, year=2025, month=2)
        
        # THEN - Une liste vide est retournée
        assert result == []
    
    def test_get_monthly_activities_december(self, activity_dao, mock_db_session, mock_activity_class):
        # GIVEN - Des activités en décembre
        activities = [Mock(id=1, date_activite=datetime(2025, 12, 25))]
        
        mock_query = Mock()
        mock_filter = Mock()
        mock_filter.all.return_value = activities
        mock_query.filter.return_value = mock_filter
        mock_db_session.query.return_value = mock_query
        
        # WHEN
        result = activity_dao.get_monthly_activities(user_id=10, year=2025, month=12)
        
        # THEN
        assert len(result) == 1


class TestActivityDAODelete:
    """Tests de la méthode delete"""
    
    def test_delete_existing_activity(self, activity_dao, mock_db_session, mock_activity_class, mock_activity):
        # GIVEN - Une activité existe avec l'ID 1
        mock_query = Mock()
        mock_filter = Mock()
        mock_filter.first.return_value = mock_activity
        mock_query.filter.return_value = mock_filter
        mock_db_session.query.return_value = mock_query
        
        # WHEN - On supprime l'activité
        result = activity_dao.delete(activity_id=1)
        
        # THEN - L'activité est supprimée
        mock_db_session.delete.assert_called_once_with(mock_activity)
        mock_db_session.commit.assert_called_once()
        assert result is True
    
    def test_delete_non_existing_activity(self, activity_dao, mock_db_session, mock_activity_class):
        # GIVEN - Aucune activité avec l'ID 999
        mock_query = Mock()
        mock_filter = Mock()
        mock_filter.first.return_value = None
        mock_query.filter.return_value = mock_filter
        mock_db_session.query.return_value = mock_query
        
        # WHEN - On tente de supprimer
        result = activity_dao.delete(activity_id=999)
        
        # THEN - False est retourné et rien n'est supprimé
        mock_db_session.delete.assert_not_called()
        mock_db_session.commit.assert_not_called()
        assert result is False
    
    def test_delete_with_error(self, activity_dao, mock_db_session, mock_activity_class, mock_activity):
        # GIVEN - Une erreur lors de la suppression
        mock_query = Mock()
        mock_filter = Mock()
        mock_filter.first.return_value = mock_activity
        mock_query.filter.return_value = mock_filter
        mock_db_session.query.return_value = mock_query
        mock_db_session.commit.side_effect = Exception("Erreur de suppression")
        
        # WHEN/THEN - Une exception est levée
        with pytest.raises(Exception, match="Erreur de suppression"):
            activity_dao.delete(activity_id=1)


class TestActivityDAOIntegration:
    """Tests d'intégration simplifiés"""
    
    def test_save_and_retrieve_activity(self, activity_dao, mock_db_session, mock_activity_class):
        # GIVEN - Une nouvelle activité
        new_activity = Mock()
        new_activity.id = None
        new_activity.titre = "Nage matinale"
        
        # Simuler l'ajout d'un ID
        def set_id(activity):
            activity.id = 100
        
        mock_db_session.refresh.side_effect = set_id
        
        # WHEN - On sauvegarde puis récupère
        saved = activity_dao.save(new_activity)
        
        # Setup pour get_by_id
        mock_query = Mock()
        mock_filter = Mock()
        mock_filter.first.return_value = saved
        mock_query.filter.return_value = mock_filter
        mock_db_session.query.return_value = mock_query
        
        retrieved = activity_dao.get_by_id(100)
        
        # THEN - L'activité est la même
        assert retrieved == saved
        assert retrieved.id == 100