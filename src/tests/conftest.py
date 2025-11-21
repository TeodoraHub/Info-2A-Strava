import sys
from pathlib import Path
import pytest
import uuid


# Ajouter src au PYTHONPATH pour que les imports fonctionnent
src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from utils.reset_database import ResetDatabase


# --- Fixtures d'environnement de test---

@pytest.fixture(scope="session")
def base_user_name_prefix():
    """
    Réinitialise la base de données de test et génère un préfixe unique 
    pour éviter les conflits de noms d'utilisateurs.
    Scope='session' signifie qu'elle est exécutée une seule fois.
    """
    ResetDatabase().lancer(test_dao=True)
    return "test_user_" + str(uuid.uuid4())[:8]


@pytest.fixture(scope="session", autouse=True)
def setup_test_db(base_user_name_prefix):
    """
    Fixture autouse pour s'assurer que base_user_name_prefix est appelé au début.
    """
    pass


# --- Reset des Singletons (Nettoyage après chaque test) ---

@pytest.fixture(scope="function", autouse=True)
def reset_singletons():
    """
    Réinitialise les Singletons après chaque test pour garantir l'isolation.
    """
    yield
    
    # Reset Session
    try:
        from utils.session import Session
        Session().reset()
    except ImportError:
        pass
    
    # Reset des DAOs Singleton (Liste à compléter selon vos besoins)
    singleton_classes = []
    
    try:
        from dao.suivi_dao import SuiviDAO
        singleton_classes.append(SuiviDAO)
    except ImportError:
        pass
    
    try:
        from dao.utilisateur_dao import UtilisateurDAO
        singleton_classes.append(UtilisateurDAO)
    except ImportError:
        pass
    
    try:
        from dao.commentaire_dao import CommentaireDAO
        singleton_classes.append(CommentaireDAO)
    except ImportError:
        pass
    
    # Réinitialisation de l'état interne de chaque classe Singleton
    for cls in singleton_classes:
        if hasattr(cls, '_instances'):
            cls._instances.clear()


# --- Fixtures pour les tests API ---

@pytest.fixture(scope="module")
def username():
    """Fixture pour fournir le nom d'utilisateur de test"""
    return "alice"


@pytest.fixture(scope="module")
def password():
    """Fixture pour fournir le mot de passe de test"""
    return "password123"
