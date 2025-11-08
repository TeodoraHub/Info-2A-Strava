import importlib
import sys
from pathlib import Path


def _ensure_real_module(module_name: str):
    """Charge le module réel même s'il a été remplacé par un MagicMock."""

    module = sys.modules.get(module_name)
    if module and module.__class__.__module__.startswith("unittest.mock"):
        sys.modules.pop(module_name, None)
        try:
            module = importlib.import_module(module_name)
        except ImportError:
            module = None
    else:
        try:
            module = importlib.import_module(module_name)
        except ImportError:
            module = None
    return module


def _propagate_real_attribute(attribute: str, real_value) -> None:
    if real_value is None:
        return
    for module in list(sys.modules.values()):
        if hasattr(module, attribute):
            attr_value = getattr(module, attribute)
            if attr_value.__class__.__module__.startswith("unittest.mock"):
                setattr(module, attribute, real_value)

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

    # Restaure les modules potentiellement remplacés par des mocks
    mocked_modules = [
        ("dao.activite_dao", "ActivityDAO"),
        ("dao.utilisateur_dao", "UtilisateurDAO"),
        ("dao.suivi_dao", "SuiviDAO"),
        ("dao.like_dao", "LikeDAO"),
        ("dao.commentaire_dao", "CommentaireDAO"),
        ("business_object.like_comment_object.like", "Like"),
        ("business_object.like_comment_object.commentaire", "Commentaire"),
    ]

    for module_name, attribute in mocked_modules:
        module = _ensure_real_module(module_name)
        if module is not None:
            real_value = getattr(module, attribute, None)
            _propagate_real_attribute(attribute, real_value)


@pytest.fixture(autouse=True)
def ensure_real_dependencies():
    """Garantit que les modules réels sont utilisés entre les tests."""

    critical_modules = [
        ("dao.activite_dao", "ActivityDAO"),
        ("dao.utilisateur_dao", "UtilisateurDAO"),
        ("dao.suivi_dao", "SuiviDAO"),
    ]

    for module_name, attribute in critical_modules:
        module = _ensure_real_module(module_name)
        if module is not None:
            real_value = getattr(module, attribute, None)
            _propagate_real_attribute(attribute, real_value)