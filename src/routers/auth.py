from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from service.utilisateur_service import UtilisateurService

router = APIRouter(tags=["Authentication"])
security = HTTPBasic()


@router.post("/login")
def login(username: str, password: str):
    """Authentifie un utilisateur"""
    user_service = UtilisateurService()
    user = user_service.se_connecter(nom_user=username, mdp=password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur ou mot de passe incorrect",
        )

    return {
        "message": "Connexion reussie",
        "user": {
            "id": user.id_user,
            "username": user.nom_user,
            "email": user.mail_user,
        },
    }


@router.post("/users")
def create_user(nom_user: str, mail_user: str, mdp: str):
    """Creer un nouvel utilisateur"""
    try:
        utilisateur_service = UtilisateurService()

        if utilisateur_service.nom_user_deja_utilise(nom_user):
            raise HTTPException(status_code=400, detail="Ce nom d'utilisateur est deja utilise")

        if not nom_user or len(nom_user.strip()) == 0:
            raise HTTPException(
                status_code=400, detail="Le nom d'utilisateur ne peut pas etre vide"
            )

        if not mail_user or "@" not in mail_user:
            raise HTTPException(status_code=400, detail="Email invalide")

        if not mdp or len(mdp) < 4:
            raise HTTPException(
                status_code=400, detail="Le mot de passe doit contenir au moins 4 caracteres"
            )

        nouvel_utilisateur = utilisateur_service.creer(
            nom_user=nom_user, mail_user=mail_user, mdp=mdp
        )

        if not nouvel_utilisateur:
            raise HTTPException(
                status_code=500, detail="Erreur lors de la creation de l'utilisateur"
            )

        return {"message": "Utilisateur cree avec succes", "user": nouvel_utilisateur}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la creation: {str(e)}")


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    """Authentifie un utilisateur via Authorization: Basic"""
    user_service = UtilisateurService()
    user = user_service.se_connecter(nom_user=credentials.username, mdp=credentials.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides",
            headers={"WWW-Authenticate": "Basic"},
        )

    return {"id": user.id_user, "username": user.nom_user, "email": user.mail_user}


@router.get("/me")
def me(current_user: dict = Depends(get_current_user)):
    """Recupere les infos de l'utilisateur courant"""
    return current_user
