import pytest
from unittest.mock import MagicMock, patch
from src.dao.utilisateur_dao import UtilisateurDAO
from src.business_object.user_object.utilisateur import Utilisateur

@pytest.fixture
def mock_utilisateur():
    # Ajouter id_user=None pour un utilisateur non encore créé en base
    return Utilisateur(
        nom_user="Test", 
        mail_user="test@example.com", 
        mdp="password",
        id_user=None
    )

def test_creer_utilisateur_success(mock_utilisateur):
    # Mock de la connexion et du curseur
    with patch("src.dao.utilisateur_dao.DBConnection") as mock_db:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value.connection.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        
        # Simuler le retour de fetchone (comme si l'INSERT a réussi)
        mock_cursor.fetchone.return_value = {"id_user": 1}
        
        # Instanciation du DAO
        dao = UtilisateurDAO()
        
        # Appel de la méthode
        result = dao.creer(mock_utilisateur)
        
        # Vérifications
        assert result is True
        assert mock_utilisateur.id_user == 1
        mock_cursor.execute.assert_called_once()

def test_creer_utilisateur_failure(mock_utilisateur):
    # Mock de la connexion et du curseur
    with patch("src.dao.utilisateur_dao.DBConnection") as mock_db:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value.connection.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        
        # Simuler une exception
        mock_cursor.execute.side_effect = Exception("Erreur de base de données")
        
        # Instanciation du DAO
        dao = UtilisateurDAO()
        
        # Appel de la méthode
        result = dao.creer(mock_utilisateur)
        
        # Vérifications
        assert result is False
        assert mock_utilisateur.id_user is None

def test_creer_utilisateur_no_return(mock_utilisateur):
    # Mock de la connexion et du curseur
    with patch("src.dao.utilisateur_dao.DBConnection") as mock_db:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value.connection.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        
        # Simuler fetchone retournant None (comme si l'INSERT n'a pas retourné d'ID)
        mock_cursor.fetchone.return_value = None
        
        # Instanciation du DAO
        dao = UtilisateurDAO()
        
        # Appel de la méthode
        result = dao.creer(mock_utilisateur)
        
        # Vérifications
        assert result is False
        assert mock_utilisateur.id_user is None
