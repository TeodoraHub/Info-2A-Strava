import pytest
from unittest.mock import MagicMock, patch
from dao.suivi_dao import SuiviDAO


@pytest.fixture
def suivi_dao():
    """Fixture pour créer une instance de SuiviDAO"""
    return SuiviDAO()


class TestSuiviDAOCreerSuivi:
    """Tests de la méthode creer_suivi"""
    
    def test_creer_suivi_success(self, suivi_dao):
        # GIVEN - Deux utilisateurs différents
        with patch("dao.suivi_dao.DBConnection") as mock_db:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_db.return_value.connection.__enter__.return_value = mock_conn
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_cursor.rowcount = 1
            
            # WHEN - On crée une relation de suivi
            result = suivi_dao.creer_suivi(id_suiveur=1, id_suivi=2)
            
            # THEN - La création réussit
            assert result is True
            mock_cursor.execute.assert_called_once()
    
    def test_creer_suivi_same_user(self, suivi_dao):
        # GIVEN - Un utilisateur qui tente de se suivre lui-même
        # WHEN - On essaie de créer une relation de suivi sur soi-même
        result = suivi_dao.creer_suivi(id_suiveur=1, id_suivi=1)
        
        # THEN - La création échoue
        assert result is False
    
    def test_creer_suivi_database_error(self, suivi_dao):
        # GIVEN - Une erreur de base de données
        with patch("dao.suivi_dao.DBConnection") as mock_db:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_db.return_value.connection.__enter__.return_value = mock_conn
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_cursor.execute.side_effect = Exception("Erreur BD")
            
            # WHEN - On tente de créer une relation
            result = suivi_dao.creer_suivi(id_suiveur=1, id_suivi=2)
            
            # THEN - La création échoue
            assert result is False
    
    def test_creer_suivi_no_rows_affected(self, suivi_dao):
        # GIVEN - Aucune ligne affectée (cas rare)
        with patch("dao.suivi_dao.DBConnection") as mock_db:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_db.return_value.connection.__enter__.return_value = mock_conn
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_cursor.rowcount = 0
            
            # WHEN - On crée une relation
            result = suivi_dao.creer_suivi(id_suiveur=1, id_suivi=2)
            
            # THEN - La création échoue
            assert result is False
    
    def test_creer_suivi_duplicate(self, suivi_dao):
        # GIVEN - Une relation déjà existante (violation de contrainte unique)
        with patch("dao.suivi_dao.DBConnection") as mock_db:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_db.return_value.connection.__enter__.return_value = mock_conn
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_cursor.execute.side_effect = Exception("duplicate key value")
            
            # WHEN - On tente de créer une relation en double
            result = suivi_dao.creer_suivi(id_suiveur=1, id_suivi=2)
            
            # THEN - La création échoue
            assert result is False


class TestSuiviDAOSupprimerSuivi:
    """Tests de la méthode supprimer_suivi"""
    
    def test_supprimer_suivi_success(self, suivi_dao):
        # GIVEN - Une relation de suivi existante
        with patch("dao.suivi_dao.DBConnection") as mock_db:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_db.return_value.connection.__enter__.return_value = mock_conn
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_cursor.rowcount = 1
            
            # WHEN - On supprime la relation
            result = suivi_dao.supprimer_suivi(id_suiveur=1, id_suivi=2)
            
            # THEN - La suppression réussit
            assert result is True
            mock_cursor.execute.assert_called_once()
    
    def test_supprimer_suivi_not_found(self, suivi_dao):
        # GIVEN - Une relation qui n'existe pas
        with patch("dao.suivi_dao.DBConnection") as mock_db:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_db.return_value.connection.__enter__.return_value = mock_conn
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_cursor.rowcount = 0
            
            # WHEN - On tente de supprimer
            result = suivi_dao.supprimer_suivi(id_suiveur=1, id_suivi=2)
            
            # THEN - La suppression échoue
            assert result is False
    
    def test_supprimer_suivi_database_error(self, suivi_dao):
        # GIVEN - Une erreur de base de données
        with patch("dao.suivi_dao.DBConnection") as mock_db:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_db.return_value.connection.__enter__.return_value = mock_conn
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_cursor.execute.side_effect = Exception("Erreur BD")
            
            # WHEN - On tente de supprimer
            result = suivi_dao.supprimer_suivi(id_suiveur=1, id_suivi=2)
            
            # THEN - La suppression échoue
            assert result is False


class TestSuiviDAOGetFollowers:
    """Tests de la méthode get_followers"""
    
    def test_get_followers_with_followers(self, suivi_dao):
        # GIVEN - Un utilisateur avec plusieurs followers
        with patch("dao.suivi_dao.DBConnection") as mock_db:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_db.return_value.connection.__enter__.return_value = mock_conn
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_cursor.fetchall.return_value = [
                {"id_suiveur": 10},
                {"id_suiveur": 20},
                {"id_suiveur": 30}
            ]
            
            # WHEN - On récupère les followers
            result = suivi_dao.get_followers(id_user=1)
            
            # THEN - La liste des followers est retournée
            assert result == [10, 20, 30]
            assert len(result) == 3
    
    def test_get_followers_no_followers(self, suivi_dao):
        # GIVEN - Un utilisateur sans followers
        with patch("dao.suivi_dao.DBConnection") as mock_db:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_db.return_value.connection.__enter__.return_value = mock_conn
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_cursor.fetchall.return_value = []
            
            # WHEN - On récupère les followers
            result = suivi_dao.get_followers(id_user=1)
            
            # THEN - Une liste vide est retournée
            assert result == []
    
    def test_get_followers_database_error(self, suivi_dao):
        # GIVEN - Une erreur de base de données
        with patch("dao.suivi_dao.DBConnection") as mock_db:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_db.return_value.connection.__enter__.return_value = mock_conn
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_cursor.execute.side_effect = Exception("Erreur BD")
            
            # WHEN - On tente de récupérer les followers
            result = suivi_dao.get_followers(id_user=1)
            
            # THEN - Une liste vide est retournée
            assert result == []


class TestSuiviDAOGetFollowing:
    """Tests de la méthode get_following"""
    
    def test_get_following_with_following(self, suivi_dao):
        # GIVEN - Un utilisateur qui suit plusieurs personnes
        with patch("dao.suivi_dao.DBConnection") as mock_db:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_db.return_value.connection.__enter__.return_value = mock_conn
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_cursor.fetchall.return_value = [
                {"id_suivi": 5},
                {"id_suivi": 15},
                {"id_suivi": 25}
            ]
            
            # WHEN - On récupère les personnes suivies
            result = suivi_dao.get_following(id_user=1)
            
            # THEN - La liste est retournée
            assert result == [5, 15, 25]
            assert len(result) == 3
    
    def test_get_following_no_following(self, suivi_dao):
        # GIVEN - Un utilisateur qui ne suit personne
        with patch("dao.suivi_dao.DBConnection") as mock_db:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_db.return_value.connection.__enter__.return_value = mock_conn
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_cursor.fetchall.return_value = []
            
            # WHEN - On récupère les personnes suivies
            result = suivi_dao.get_following(id_user=1)
            
            # THEN - Une liste vide est retournée
            assert result == []
    
    def test_get_following_database_error(self, suivi_dao):
        # GIVEN - Une erreur de base de données
        with patch("dao.suivi_dao.DBConnection") as mock_db:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_db.return_value.connection.__enter__.return_value = mock_conn
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_cursor.execute.side_effect = Exception("Erreur BD")
            
            # WHEN - On tente de récupérer les personnes suivies
            result = suivi_dao.get_following(id_user=1)
            
            # THEN - Une liste vide est retournée
            assert result == []


class TestSuiviDAOUserSuit:
    """Tests de la méthode user_suit"""
    
    def test_user_suit_true(self, suivi_dao):
        # GIVEN - Un utilisateur qui suit un autre
        with patch("dao.suivi_dao.DBConnection") as mock_db:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_db.return_value.connection.__enter__.return_value = mock_conn
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_cursor.fetchone.return_value = {"nb": 1}
            
            # WHEN - On vérifie si l'utilisateur 1 suit l'utilisateur 2
            result = suivi_dao.user_suit(id_suiveur=1, id_suivi=2)
            
            # THEN - Le résultat est True
            assert result is True
    
    def test_user_suit_false(self, suivi_dao):
        # GIVEN - Un utilisateur qui ne suit pas un autre
        with patch("dao.suivi_dao.DBConnection") as mock_db:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_db.return_value.connection.__enter__.return_value = mock_conn
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_cursor.fetchone.return_value = {"nb": 0}
            
            # WHEN - On vérifie
            result = suivi_dao.user_suit(id_suiveur=1, id_suivi=2)
            
            # THEN - Le résultat est False
            assert result is False
    
    def test_user_suit_no_result(self, suivi_dao):
        # GIVEN - Aucun résultat de la requête
        with patch("dao.suivi_dao.DBConnection") as mock_db:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_db.return_value.connection.__enter__.return_value = mock_conn
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_cursor.fetchone.return_value = None
            
            # WHEN - On vérifie
            result = suivi_dao.user_suit(id_suiveur=1, id_suivi=2)
            
            # THEN - Le résultat est False
            assert result is False
    
    def test_user_suit_database_error(self, suivi_dao):
        # GIVEN - Une erreur de base de données
        with patch("dao.suivi_dao.DBConnection") as mock_db:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_db.return_value.connection.__enter__.return_value = mock_conn
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_cursor.execute.side_effect = Exception("Erreur BD")
            
            # WHEN - On vérifie
            result = suivi_dao.user_suit(id_suiveur=1, id_suivi=2)
            
            # THEN - Le résultat est False
            assert result is False


class TestSuiviDAOCountFollowers:
    """Tests de la méthode count_followers"""
    
    def test_count_followers_with_followers(self, suivi_dao):
        # GIVEN - Un utilisateur avec 5 followers
        with patch("dao.suivi_dao.DBConnection") as mock_db:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_db.return_value.connection.__enter__.return_value = mock_conn
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_cursor.fetchone.return_value = {"nb_followers": 5}
            
            # WHEN - On compte les followers
            result = suivi_dao.count_followers(id_user=1)
            
            # THEN - Le nombre est correct
            assert result == 5
    
    def test_count_followers_no_followers(self, suivi_dao):
        # GIVEN - Un utilisateur sans followers
        with patch("dao.suivi_dao.DBConnection") as mock_db:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_db.return_value.connection.__enter__.return_value = mock_conn
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_cursor.fetchone.return_value = {"nb_followers": 0}
            
            # WHEN - On compte les followers
            result = suivi_dao.count_followers(id_user=1)
            
            # THEN - Le résultat est 0
            assert result == 0
    
    def test_count_followers_no_result(self, suivi_dao):
        # GIVEN - Aucun résultat
        with patch("dao.suivi_dao.DBConnection") as mock_db:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_db.return_value.connection.__enter__.return_value = mock_conn
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_cursor.fetchone.return_value = None
            
            # WHEN - On compte les followers
            result = suivi_dao.count_followers(id_user=1)
            
            # THEN - Le résultat est 0
            assert result == 0
    
    def test_count_followers_database_error(self, suivi_dao):
        # GIVEN - Une erreur de base de données
        with patch("dao.suivi_dao.DBConnection") as mock_db:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_db.return_value.connection.__enter__.return_value = mock_conn
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_cursor.execute.side_effect = Exception("Erreur BD")
            
            # WHEN - On compte les followers
            result = suivi_dao.count_followers(id_user=1)
            
            # THEN - Le résultat est 0
            assert result == 0


class TestSuiviDAOCountFollowing:
    """Tests de la méthode count_following"""
    
    def test_count_following_with_following(self, suivi_dao):
        # GIVEN - Un utilisateur qui suit 3 personnes
        with patch("dao.suivi_dao.DBConnection") as mock_db:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_db.return_value.connection.__enter__.return_value = mock_conn
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_cursor.fetchone.return_value = {"nb_following": 3}
            
            # WHEN - On compte les personnes suivies
            result = suivi_dao.count_following(id_user=1)
            
            # THEN - Le nombre est correct
            assert result == 3
    
    def test_count_following_no_following(self, suivi_dao):
        # GIVEN - Un utilisateur qui ne suit personne
        with patch("dao.suivi_dao.DBConnection") as mock_db:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_db.return_value.connection.__enter__.return_value = mock_conn
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_cursor.fetchone.return_value = {"nb_following": 0}
            
            # WHEN - On compte les personnes suivies
            result = suivi_dao.count_following(id_user=1)
            
            # THEN - Le résultat est 0
            assert result == 0
    
    def test_count_following_no_result(self, suivi_dao):
        # GIVEN - Aucun résultat
        with patch("dao.suivi_dao.DBConnection") as mock_db:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_db.return_value.connection.__enter__.return_value = mock_conn
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_cursor.fetchone.return_value = None
            
            # WHEN - On compte les personnes suivies
            result = suivi_dao.count_following(id_user=1)
            
            # THEN - Le résultat est 0
            assert result == 0
    
    def test_count_following_database_error(self, suivi_dao):
        # GIVEN - Une erreur de base de données
        with patch("dao.suivi_dao.DBConnection") as mock_db:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_db.return_value.connection.__enter__.return_value = mock_conn
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_cursor.execute.side_effect = Exception("Erreur BD")
            
            # WHEN - On compte les personnes suivies
            result = suivi_dao.count_following(id_user=1)
            
            # THEN - Le résultat est 0
            assert result == 0


class TestSuiviDAOIntegration:
    """Tests d'intégration simulant des scénarios réels"""
    
    def test_workflow_suivi_complet(self, suivi_dao):
        # GIVEN - Setup complet pour simuler un workflow
        with patch("dao.suivi_dao.DBConnection") as mock_db:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_db.return_value.connection.__enter__.return_value = mock_conn
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            
            # Simulation : création de suivi réussie
            mock_cursor.rowcount = 1
            created = suivi_dao.creer_suivi(id_suiveur=1, id_suivi=2)
            assert created is True
            
            # Simulation : vérification que l'utilisateur suit bien
            mock_cursor.fetchone.return_value = {"nb": 1}
            suit = suivi_dao.user_suit(id_suiveur=1, id_suivi=2)
            assert suit is True
            
            # Simulation : suppression du suivi
            mock_cursor.rowcount = 1
            deleted = suivi_dao.supprimer_suivi(id_suiveur=1, id_suivi=2)
            assert deleted is True