import hashlib
import logging
import secrets


def hash_password(password, sel=""):
    """Hachage du mot de passe avec SHA256 (ancienne version)

    NOTE: Cette fonction est conservée pour compatibilité mais il est recommandé
    d'utiliser hash_password_bcrypt pour plus de sécurité

    Parameters
    ----------
    password : str
        Le mot de passe en clair
    sel : str
        Sel optionnel

    Returns
    -------
    str
        Le hash du mot de passe
    """
    password_bytes = password.encode("utf-8") + sel.encode("utf-8")
    hash_object = hashlib.sha256(password_bytes)
    return hash_object.hexdigest()


def hash_password_bcrypt(password: str) -> str:
    """Hachage du mot de passe avec bcrypt (recommandé)

    Parameters
    ----------
    password : str
        Le mot de passe en clair

    Returns
    -------
    str
        Le hash bcrypt du mot de passe
    """
    try:
        import bcrypt

        password_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode("utf-8")
    except ImportError:
        logging.warning("bcrypt n'est pas installé, utilisation de SHA256 à la place")
        return hash_password(password)


def verify_password_bcrypt(password: str, hashed_password: str) -> bool:
    """Vérifie un mot de passe contre son hash bcrypt

    Parameters
    ----------
    password : str
        Le mot de passe en clair à vérifier
    hashed_password : str
        Le hash bcrypt du mot de passe

    Returns
    -------
    bool
        True si le mot de passe correspond
    """
    try:
        import bcrypt

        password_bytes = password.encode("utf-8")
        hashed_bytes = hashed_password.encode("utf-8")
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except ImportError:
        logging.warning("bcrypt n'est pas installé, comparaison simple")
        return hash_password(password) == hashed_password
    except Exception as e:
        logging.error(f"Erreur lors de la vérification du mot de passe: {e}")
        return False


def generate_secure_token(length: int = 32) -> str:
    """Génère un token sécurisé aléatoire

    Parameters
    ----------
    length : int
        Longueur du token (par défaut: 32)

    Returns
    -------
    str
        Token hexadécimal
    """
    return secrets.token_hex(length)


def valider_force_mot_de_passe(password: str) -> dict:
    """Valide la force d'un mot de passe

    Parameters
    ----------
    password : str
        Le mot de passe à valider

    Returns
    -------
    dict
        {
            'valide': bool,
            'score': int (0-4),
            'messages': list[str]
        }
    """
    messages = []
    score = 0

    # Longueur minimale
    if len(password) < 8:
        messages.append("Le mot de passe doit contenir au moins 8 caractères")
    else:
        score += 1

    # Contient des minuscules
    if any(c.islower() for c in password):
        score += 1
    else:
        messages.append("Le mot de passe doit contenir au moins une minuscule")

    # Contient des majuscules
    if any(c.isupper() for c in password):
        score += 1
    else:
        messages.append("Le mot de passe doit contenir au moins une majuscule")

    # Contient des chiffres
    if any(c.isdigit() for c in password):
        score += 1
    else:
        messages.append("Le mot de passe doit contenir au moins un chiffre")

    # Contient des caractères spéciaux
    if any(not c.isalnum() for c in password):
        score += 1

    return {
        "valide": score >= 3 and len(password) >= 8,
        "score": min(score, 5),
        "messages": messages,
    }


def sanitize_input(input_str: str) -> str:
    """Nettoie une chaîne d'entrée pour éviter les injections

    Parameters
    ----------
    input_str : str
        La chaîne à nettoyer

    Returns
    -------
    str
        La chaîne nettoyée
    """
    if not input_str:
        return ""

    # Supprimer les caractères dangereux
    dangerous_chars = ["<", ">", '"', "'", "\\", ";", "--", "/*", "*/"]
    cleaned = input_str
    for char in dangerous_chars:
        cleaned = cleaned.replace(char, "")

    return cleaned.strip()
