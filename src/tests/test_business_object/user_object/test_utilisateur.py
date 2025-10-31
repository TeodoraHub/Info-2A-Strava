"""
Tests unitaires pour la classe Utilisateur
"""

import pytest
from unittest.mock import Mock, MagicMock, mock_open, patch
from datetime import datetime
import sys

# Mock des modules AVANT l'import pour éviter les importations circulaires
sys.modules['dao.activite_dao'] = MagicMock()
sys.modules['dao.utilisateur_dao'] = MagicMock()
sys.modules['dao.suivi_dao'] = MagicMock()
sys.modules['dao.like_dao'] = MagicMock()
sys.modules['dao.commentaire_dao'] = MagicMock()
sys.modules['service.session_service'] = MagicMock()
sys.modules['business_object.statistiques'] = MagicMock()
sys.modules['business_object.like'] = MagicMock()
sys.modules['business_object.commentaire'] = MagicMock()

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

    @patch("builtins.open", new_callable=mock_open, read_data="<gpx></gpx>")
    @patch("gpxpy.parse")
    def test_creer_activite_course_pied(self, mock_gpx_parse, mock_file):
        # GIVEN - Un utilisateur et des données de course à pied
        user = Utilisateur(1, "Runner", "runner@test.fr", "pass")
        mock_gpx = Mock()
        mock_gpx.length_3d.return_value = 5000.0
        mock_gpx.get_duration.return_value = 1800
        mock_gpx_parse.return_value = mock_gpx

        # WHEN - On crée une activité de course
        activite = user.creer_activite(
            type_activite="course",
            titre="Morning Run",
            description="Course matinale",
            lieu="Parc",
            fichier_gpx="test.gpx"
        )

        # THEN - Une activité est créée et le fichier GPX a été lu
        assert activite is not None
        mock_file.assert_called_once_with("test.gpx", "r", encoding="utf-8")
        mock_gpx.length_3d.assert_called_once()
        mock_gpx.get_duration.assert_called_once()

    @patch("builtins.open", new_callable=mock_open, read_data="<gpx></gpx>")
    @patch("gpxpy.parse")
    def test_creer_activite_cyclisme(self, mock_gpx_parse, mock_file):
        # GIVEN - Un utilisateur et des données de cyclisme
        user = Utilisateur(2, "Cyclist", "cyclist@test.fr", "pass")
        mock_gpx = Mock()
        mock_gpx.length_3d.return_value = 30000.0
        mock_gpx.get_duration.return_value = 3600
        mock_gpx_parse.return_value = mock_gpx

        # WHEN - On crée une activité de cyclisme avec type de vélo
        activite = user.creer_activite(
            type_activite="cyclisme",
            titre="Sortie vélo",
            description="Route de campagne",
            lieu="Campagne",
            fichier_gpx="velo.gpx",
            type_velo="route"
        )

        # THEN - Une activité est créée et le fichier GPX a été lu
        assert activite is not None
        mock_file.assert_called_once_with("velo.gpx", "r", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open, read_data="<gpx></gpx>")
    @patch("gpxpy.parse")
    def test_creer_activite_natation(self, mock_gpx_parse, mock_file):
        # GIVEN - Un utilisateur et des données de natation
        user = Utilisateur(3, "Swimmer", "swim@test.fr", "pass")
        mock_gpx = Mock()
        mock_gpx.length_3d.return_value = 1000.0
        mock_gpx.get_duration.return_value = 1200
        mock_gpx_parse.return_value = mock_gpx

        # WHEN - On crée une activité de natation
        activite = user.creer_activite(
            type_activite="natation",
            titre="Piscine",
            description="Entraînement natation",
            lieu="Piscine municipale",
            fichier_gpx="natation.gpx",
            type_nage="crawl"
        )

        # THEN - Une activité est créée et le fichier GPX a été lu
        assert activite is not None
        mock_file.assert_called_once_with("natation.gpx", "r", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open, read_data="<gpx></gpx>")
    @patch("gpxpy.parse")
    def test_creer_activite_randonnee(self, mock_gpx_parse, mock_file):
        # GIVEN - Un utilisateur et des données de randonnée
        user = Utilisateur(4, "Hiker", "hiker@test.fr", "pass")
        mock_gpx = Mock()
        mock_gpx.length_3d.return_value = 10000.0
        mock_gpx.get_duration.return_value = 7200
        mock_gpx_parse.return_value = mock_gpx

        # WHEN - On crée une activité de randonnée
        activite = user.creer_activite(
            type_activite="randonnee",
            titre="Montagne",
            description="Randonnée en altitude",
            lieu="Alpes",
            fichier_gpx="rando.gpx",
            type_terrain="montagne"
        )

        # THEN - Une activité est créée et le fichier GPX a été lu
        assert activite is not None
        mock_file.assert_called_once_with("rando.gpx", "r", encoding="utf-8")

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
        with pytest.raises(ValueError) as exc_info:
            user.creer_activite(
                type_activite="invalid",
                titre="Test",
                description="Test",
                lieu="Test",
                fichier_gpx="test.gpx"
            )
        # L'exception contient le type invalide dans le message
        assert "invalid" in str(exc_info.value)


class TestConsulterActivites:
    """Tests de la méthode consulter_activites"""

    def test_consulter_activites_succes(self):
        # GIVEN - Un utilisateur connecté avec une session DB
        with patch("business_object.User_object.utilisateur.Session") as mock_session_class, \
             patch("business_object.User_object.utilisateur.ActivityDAO") as mock_dao_class:
            
            user = Utilisateur(1, "Test", "test@test.fr", "pass")
            
            # Mock de Session
            mock_utilisateur = Mock()
            mock_utilisateur.db_session = Mock()
            mock_session_instance = Mock()
            mock_session_instance.utilisateur = mock_utilisateur
            mock_session_class.return_value = mock_session_instance
            
            # Mock de DAO
            mock_activites = [Mock(titre="Activité 1"), Mock(titre="Activité 2")]
            mock_dao = Mock()
            mock_dao.get_by_user.return_value = mock_activites
            mock_dao_class.return_value = mock_dao

            # WHEN - On consulte les activités
            activites = user.consulter_activites()

            # THEN - Les activités sont récupérées via le DAO
            assert activites == mock_activites
            assert len(activites) == 2
            mock_dao.get_by_user.assert_called_once_with(1)

    def test_consulter_activites_pas_de_session(self):
        # GIVEN - Aucun utilisateur connecté
        with patch("business_object.User_object.utilisateur.Session") as mock_session_class:
            user = Utilisateur(1, "Test", "test@test.fr", "pass")
            mock_session_instance = Mock()
            mock_session_instance.utilisateur = None
            mock_session_class.return_value = mock_session_instance

            # WHEN / THEN - Une exception est levée
            with pytest.raises(RuntimeError, match="Aucun utilisateur connecté"):
                user.consulter_activites()


class TestModifierActivite:
    """Tests de la méthode modifier_activite"""

    def test_modifier_activite_succes(self):
        # GIVEN - Un utilisateur avec une activité existante
        with patch("business_object.User_object.utilisateur.Session") as mock_session_class, \
             patch("business_object.User_object.utilisateur.ActivityDAO") as mock_dao_class, \
             patch("builtins.input") as mock_input, \
             patch("builtins.print") as mock_print:
            
            user = Utilisateur(1, "Test", "test@test.fr", "pass")
            user.db_session = Mock()
            
            # Mock de Session
            mock_utilisateur = Mock()
            mock_utilisateur.db_session = user.db_session
            mock_session_instance = Mock()
            mock_session_instance.utilisateur = mock_utilisateur
            mock_session_class.return_value = mock_session_instance
            
            # Mock d'activité
            mock_activite = Mock()
            mock_activite.id = 100
            mock_activite.titre = "Ancien titre"
            mock_activite.description = "Ancienne description"
            
            # Mock de DAO
            mock_dao = Mock()
            mock_dao.get_by_user.return_value = [mock_activite]
            mock_dao_class.return_value = mock_dao
            
            mock_input.side_effect = ["100", "Nouveau titre", "Nouvelle description"]

            # WHEN - On modifie l'activité
            user.modifier_activite()

            # THEN - L'activité est modifiée et sauvegardée
            assert mock_activite.titre == "Nouveau titre"
            assert mock_activite.description == "Nouvelle description"
            user.db_session.commit.assert_called_once()

    def test_modifier_activite_aucune_activite(self):
        # GIVEN - Un utilisateur sans activités
        with patch("business_object.User_object.utilisateur.Session") as mock_session_class, \
             patch("business_object.User_object.utilisateur.ActivityDAO") as mock_dao_class, \
             patch("builtins.print") as mock_print:
            
            user = Utilisateur(1, "Test", "test@test.fr", "pass")
            user.db_session = Mock()
            
            # Mock de Session
            mock_utilisateur = Mock()
            mock_utilisateur.db_session = user.db_session
            mock_session_instance = Mock()
            mock_session_instance.utilisateur = mock_utilisateur
            mock_session_class.return_value = mock_session_instance
            
            # Mock de DAO
            mock_dao = Mock()
            mock_dao.get_by_user.return_value = []
            mock_dao_class.return_value = mock_dao

            # WHEN - On tente de modifier une activité
            user.modifier_activite()

            # THEN - Un message indique qu'il n'y a aucune activité
            mock_print.assert_any_call("Aucune activité à modifier.")

    def test_modifier_activite_id_invalide(self):
        # GIVEN - Un utilisateur avec une activité mais un ID invalide saisi
        with patch("business_object.User_object.utilisateur.Session") as mock_session_class, \
             patch("business_object.User_object.utilisateur.ActivityDAO") as mock_dao_class, \
             patch("builtins.input") as mock_input, \
             patch("builtins.print") as mock_print:
            
            user = Utilisateur(1, "Test", "test@test.fr", "pass")
            user.db_session = Mock()
            
            # Mock de Session
            mock_utilisateur = Mock()
            mock_utilisateur.db_session = user.db_session
            mock_session_instance = Mock()
            mock_session_instance.utilisateur = mock_utilisateur
            mock_session_class.return_value = mock_session_instance
            
            # Mock d'activité
            mock_activite = Mock()
            mock_activite.id = 100
            mock_activite.titre = "Test"
            
            # Mock de DAO
            mock_dao = Mock()
            mock_dao.get_by_user.return_value = [mock_activite]
            mock_dao_class.return_value = mock_dao
            
            mock_input.return_value = "999"

            # WHEN - On tente de modifier avec un ID invalide
            user.modifier_activite()

            # THEN - Un message d'erreur est affiché
            mock_print.assert_any_call("ID invalide.")


class TestSupprimerActivite:
    """Tests de la méthode supprimer_activite"""

    def test_supprimer_activite_succes(self):
        # GIVEN - Un utilisateur avec une activité à supprimer
        with patch("business_object.User_object.utilisateur.Session") as mock_session_class, \
             patch("business_object.User_object.utilisateur.ActivityDAO") as mock_dao_class, \
             patch("builtins.input") as mock_input, \
             patch("builtins.print") as mock_print:
            
            user = Utilisateur(1, "Test", "test@test.fr", "pass")
            user.db_session = Mock()
            
            # Mock de Session
            mock_utilisateur = Mock()
            mock_utilisateur.db_session = user.db_session
            mock_session_instance = Mock()
            mock_session_instance.utilisateur = mock_utilisateur
            mock_session_class.return_value = mock_session_instance
            
            # Mock d'activité
            mock_activite = Mock()
            mock_activite.id = 100
            mock_activite.titre = "Activité à supprimer"
            
            # Mock de DAO
            mock_dao = Mock()
            mock_dao.get_by_user.return_value = [mock_activite]
            mock_dao_class.return_value = mock_dao
            
            mock_input.return_value = "100"

            # WHEN - On supprime l'activité
            user.supprimer_activite()

            # THEN - L'activité est supprimée de la base
            user.db_session.delete.assert_called_once_with(mock_activite)
            user.db_session.commit.assert_called_once()

    def test_supprimer_activite_id_invalide(self):
        # GIVEN - Un utilisateur avec une activité mais un ID invalide
        with patch("business_object.User_object.utilisateur.Session") as mock_session_class, \
             patch("business_object.User_object.utilisateur.ActivityDAO") as mock_dao_class, \
             patch("builtins.input") as mock_input:
            
            user = Utilisateur(1, "Test", "test@test.fr", "pass")
            user.db_session = Mock()
            
            # Mock de Session
            mock_utilisateur = Mock()
            mock_utilisateur.db_session = user.db_session
            mock_session_instance = Mock()
            mock_session_instance.utilisateur = mock_utilisateur
            mock_session_class.return_value = mock_session_instance
            
            # Mock d'activité
            mock_activite = Mock()
            mock_activite.id = 100
            
            # Mock de DAO
            mock_dao = Mock()
            mock_dao.get_by_user.return_value = [mock_activite]
            mock_dao_class.return_value = mock_dao
            
            mock_input.return_value = "999"

            # WHEN / THEN - Une exception est levée pour ID invalide
            with pytest.raises(ValueError, match="ID invalide"):
                user.supprimer_activite()

    def test_supprimer_activite_aucune_activite(self):
        # GIVEN - Un utilisateur sans activités
        with patch("business_object.User_object.utilisateur.Session") as mock_session_class, \
             patch("business_object.User_object.utilisateur.ActivityDAO") as mock_dao_class, \
             patch("builtins.print") as mock_print:
            
            user = Utilisateur(1, "Test", "test@test.fr", "pass")
            user.db_session = Mock()
            
            # Mock de Session
            mock_utilisateur = Mock()
            mock_utilisateur.db_session = user.db_session
            mock_session_instance = Mock()
            mock_session_instance.utilisateur = mock_utilisateur
            mock_session_class.return_value = mock_session_instance
            
            # Mock de DAO
            mock_dao = Mock()
            mock_dao.get_by_user.return_value = []
            mock_dao_class.return_value = mock_dao

            # WHEN - On tente de supprimer une activité
            user.supprimer_activite()

            # THEN - Un message indique qu'il n'y a aucune activité
            mock_print.assert_any_call("Aucune activité à supprimer.")


class TestSuivreUtilisateur:
    """Tests de la méthode suivre_utilisateur"""

    def test_suivre_utilisateur_succes(self):
        # GIVEN - Deux utilisateurs différents
        with patch("business_object.User_object.utilisateur.Session") as mock_session_class, \
             patch("business_object.User_object.utilisateur.SuiviDAO") as mock_dao_class:
            
            user1 = Utilisateur(1, "User1", "user1@test.fr", "pass")
            user2 = Utilisateur(2, "User2", "user2@test.fr", "pass")
            
            # Mock de Session
            mock_utilisateur = Mock()
            mock_utilisateur.id_user = 1
            mock_utilisateur.db_session = Mock()
            mock_session_instance = Mock()
            mock_session_instance.utilisateur = mock_utilisateur
            mock_session_class.return_value = mock_session_instance
            
            # Mock de DAO
            mock_dao = Mock()
            mock_dao.existe_suivi.return_value = False
            mock_dao_class.return_value = mock_dao

            # WHEN - User1 suit User2
            user1.suivre_utilisateur(user2)

            # THEN - Le suivi est vérifié puis ajouté
            mock_dao.existe_suivi.assert_called_once_with(1, 2)
            mock_dao.ajouter_suivi.assert_called_once_with(1, 2)

    def test_suivre_utilisateur_soi_meme(self):
        # GIVEN - Un utilisateur qui tente de se suivre lui-même
        with patch("business_object.User_object.utilisateur.Session") as mock_session_class:
            user = Utilisateur(1, "User", "user@test.fr", "pass")
            
            # Mock de Session
            mock_utilisateur = Mock()
            mock_utilisateur.id_user = 1
            mock_session_instance = Mock()
            mock_session_instance.utilisateur = mock_utilisateur
            mock_session_class.return_value = mock_session_instance

            # WHEN / THEN - Une exception est levée
            with pytest.raises(ValueError, match="Impossible de se suivre soi-même"):
                user.suivre_utilisateur(user)

    def test_suivre_utilisateur_deja_suivi(self):
        # GIVEN - Deux utilisateurs avec un suivi existant
        with patch("business_object.User_object.utilisateur.Session") as mock_session_class, \
             patch("business_object.User_object.utilisateur.SuiviDAO") as mock_dao_class:
            
            user1 = Utilisateur(1, "User1", "user1@test.fr", "pass")
            user2 = Utilisateur(2, "User2", "user2@test.fr", "pass")
            
            # Mock de Session
            mock_utilisateur = Mock()
            mock_utilisateur.id_user = 1
            mock_utilisateur.db_session = Mock()
            mock_session_instance = Mock()
            mock_session_instance.utilisateur = mock_utilisateur
            mock_session_class.return_value = mock_session_instance
            
            # Mock de DAO
            mock_dao = Mock()
            mock_dao.existe_suivi.return_value = True
            mock_dao_class.return_value = mock_dao

            # WHEN / THEN - Une exception est levée car déjà suivi
            with pytest.raises(ValueError, match="Utilisateur déjà suivi"):
                user1.suivre_utilisateur(user2)


class TestLikerActivite:
    """Tests de la méthode liker_activite"""

    def test_liker_activite_succes(self):
        # GIVEN - Un utilisateur et une activité à liker
        with patch("business_object.User_object.utilisateur.Session") as mock_session_class, \
             patch("business_object.User_object.utilisateur.LikeDAO") as mock_dao_class, \
             patch("business_object.User_object.utilisateur.Like") as mock_like_class:
            
            user = Utilisateur(1, "User", "user@test.fr", "pass")
            mock_activite = Mock()
            mock_activite.id = 100
            
            # Mock de Session
            mock_utilisateur = Mock()
            mock_utilisateur.id_user = 1
            mock_utilisateur.db_session = Mock()
            mock_session_instance = Mock()
            mock_session_instance.utilisateur = mock_utilisateur
            mock_session_class.return_value = mock_session_instance
            
            # Mock de DAO
            mock_dao = Mock()
            mock_dao.existe_like.return_value = False
            mock_dao_class.return_value = mock_dao
            
            # Mock de Like
            mock_like = Mock()
            mock_like_class.return_value = mock_like

            # WHEN - On like l'activité
            result = user.liker_activite(mock_activite)

            # THEN - Le like est créé et ajouté
            assert result == mock_like
            mock_dao.existe_like.assert_called_once_with(1, 100)
            mock_dao.ajouter_like.assert_called_once_with(mock_like)

    def test_liker_activite_deja_like(self):
        # GIVEN - Un utilisateur qui a déjà liké une activité
        with patch("business_object.User_object.utilisateur.Session") as mock_session_class, \
             patch("business_object.User_object.utilisateur.LikeDAO") as mock_dao_class, \
             patch("builtins.print") as mock_print:
            
            user = Utilisateur(1, "User", "user@test.fr", "pass")
            mock_activite = Mock()
            mock_activite.id = 100
            
            # Mock de Session
            mock_utilisateur = Mock()
            mock_utilisateur.id_user = 1
            mock_utilisateur.db_session = Mock()
            mock_session_instance = Mock()
            mock_session_instance.utilisateur = mock_utilisateur
            mock_session_class.return_value = mock_session_instance
            
            # Mock de DAO
            mock_dao = Mock()
            mock_dao.existe_like.return_value = True
            mock_dao_class.return_value = mock_dao

            # WHEN - On tente de liker à nouveau
            result = user.liker_activite(mock_activite)

            # THEN - Aucun like n'est créé et un message s'affiche
            assert result is None
            mock_print.assert_called_with("Vous avez déjà liké cette activité.")


class TestCommenterActivite:
    """Tests de la méthode commenter_activite"""

    def test_commenter_activite_succes(self):
        # GIVEN - Un utilisateur et une activité à commenter
        with patch("business_object.User_object.utilisateur.Session") as mock_session_class, \
             patch("business_object.User_object.utilisateur.CommentaireDAO") as mock_dao_class, \
             patch("business_object.User_object.utilisateur.Commentaire") as mock_comm_class:
            
            user = Utilisateur(1, "User", "user@test.fr", "pass")
            mock_activite = Mock()
            mock_activite.id = 100
            contenu = "Super activité !"
            
            # Mock de Session
            mock_utilisateur = Mock()
            mock_utilisateur.id_user = 1
            mock_utilisateur.db_session = Mock()
            mock_session_instance = Mock()
            mock_session_instance.utilisateur = mock_utilisateur
            mock_session_class.return_value = mock_session_instance
            
            # Mock de DAO
            mock_dao = Mock()
            mock_dao_class.return_value = mock_dao
            
            # Mock de Commentaire
            mock_commentaire = Mock()
            mock_comm_class.return_value = mock_commentaire

            # WHEN - On commente l'activité
            result = user.commenter_activite(mock_activite, contenu)

            # THEN - Le commentaire est créé et ajouté
            assert result == mock_commentaire
            mock_dao.ajouter_commentaire.assert_called_once_with(mock_commentaire)


class TestObtenirStatistiques:
    """Tests de la méthode obtenir_statistiques"""

    def test_obtenir_statistiques_sans_filtre(self):
        # GIVEN - Un utilisateur connecté
        with patch("business_object.User_object.utilisateur.Session") as mock_session_class, \
             patch("business_object.User_object.utilisateur.Statistiques") as mock_stats_class:

            user = Utilisateur(1, "User", "user@test.fr", "pass")

            # Mock de Session
            mock_utilisateur = Mock()
            mock_session_instance = Mock()
            mock_session_instance.utilisateur = mock_utilisateur
            mock_session_class.return_value = mock_session_instance

            # Mock des statistiques
            mock_stats_class.nombre_activites.return_value = 10
            mock_stats_class.kilometres.return_value = 50.5
            mock_stats_class.heures_activite.return_value = 8.5

            # WHEN - On obtient les statistiques sans filtre
            stats = user.obtenir_statistiques()

            # THEN - Les statistiques sont calculées et retournées
            assert stats["nombre_activites"] == 10
            assert stats["kilometres"] == 50.5
            assert stats["heures"] == 8.5
            mock_stats_class.nombre_activites.assert_called_once_with(mock_utilisateur, None, None)
            mock_stats_class.kilometres.assert_called_once_with(mock_utilisateur, None, None)
            mock_stats_class.heures_activite.assert_called_once_with(mock_utilisateur, None, None)

    def test_obtenir_statistiques_avec_periode(self):
        # GIVEN - Un utilisateur et un filtre de période 30 jours
        with patch("business_object.User_object.utilisateur.Session") as mock_session_class, \
             patch("business_object.User_object.utilisateur.Statistiques") as mock_stats_class:

            user = Utilisateur(1, "User", "user@test.fr", "pass")

            # Mock de Session
            mock_utilisateur = Mock()
            mock_session_instance = Mock()
            mock_session_instance.utilisateur = mock_utilisateur
            mock_session_class.return_value = mock_session_instance

            # Mock des statistiques
            mock_stats_class.nombre_activites.return_value = 20
            mock_stats_class.kilometres.return_value = 150.0
            mock_stats_class.heures_activite.return_value = 15.0

            # WHEN - On obtient les statistiques sur 30 jours
            stats = user.obtenir_statistiques(periode="30j")

            # THEN - Les statistiques sont filtrées par période
            assert stats["nombre_activites"] == 20
            assert stats["kilometres"] == 150.0
            assert stats["heures"] == 15.0
            mock_stats_class.nombre_activites.assert_called_once_with(mock_utilisateur, "30j", None)
            mock_stats_class.kilometres.assert_called_once_with(mock_utilisateur, "30j", None)
            mock_stats_class.heures_activite.assert_called_once_with(mock_utilisateur, "30j", None)

    def test_obtenir_statistiques_avec_sport(self):
        # GIVEN - Un utilisateur et un filtre par sport
        with patch("business_object.User_object.utilisateur.Session") as mock_session_class, \
             patch("business_object.User_object.utilisateur.Statistiques") as mock_stats_class:

            user = Utilisateur(1, "User", "user@test.fr", "pass")

            # Mock de Session
            mock_utilisateur = Mock()
            mock_session_instance = Mock()
            mock_session_instance.utilisateur = mock_utilisateur
            mock_session_class.return_value = mock_session_instance

            # Mock des statistiques
            mock_stats_class.nombre_activites.return_value = 5
            mock_stats_class.kilometres.return_value = 25.0
            mock_stats_class.heures_activite.return_value = 4.0

            # WHEN - On obtient les statistiques avec filtre sport
            stats = user.obtenir_statistiques(sport="course")

            # THEN - Les statistiques sont filtrées par sport
            assert stats["nombre_activites"] == 5
            assert stats["kilometres"] == 25.0
            assert stats["heures"] == 4.0
            mock_stats_class.nombre_activites.assert_called_once_with(mock_utilisateur, None, "course")
            mock_stats_class.kilometres.assert_called_once_with(mock_utilisateur, None, "course")
            mock_stats_class.heures_activite.assert_called_once_with(mock_utilisateur, None, "course")
