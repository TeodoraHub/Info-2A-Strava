import sys
from pathlib import Path

# Ajouter src au PYTHONPATH pour que les imports fonctionnent
src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

import pytest


@pytest.fixture(scope="function", autouse=True)
def reset_singletons():
    """
    Reset tous les Singletons après chaque test pour éviter les conflits
    """
    yield
    
    # Reset Session
    try:
        from utils.session import Session
        Session.reset()
    except ImportError:
        pass
    
    # Reset des DAOs Singleton
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
    
    # Reset de chaque classe Singleton
    for cls in singleton_classes:
        if hasattr(cls, '_instances'):
            cls._instances.clear()