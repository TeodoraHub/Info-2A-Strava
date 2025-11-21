import os
import pytest
import uuid 

from unittest.mock import patch

from utils.securite import hash_password # Gardé pour référence si besoin
# Les imports de ResetDatabase et des fixtures ont été supprimés

from dao.utilisateur_dao import UtilisateurDAO
from business_object.user_object.utilisateur import Utilisateur

# --- Données de test ---

ID_USER_EXISTANT = 1
NOM_USER_EXISTANT = "alice"
MAIL_USER_EXISTANT = "alice@example.com"
MDP_USER_CLAIRE_EXISTANT = "password123"
# Hash de "password123" stocké dans pop_db_test.sql pour l'utilisateur "alice"
MDP_HASH_EXISTANT = '1bf52fdbcef590cedf5cd8f250ea6c32f41d9e8901b396cdfa35076a6f054b47'

# --- Tests de la méthode trouver_par_id ---

def test_trouver_par_id_existant():
    # GIVEN
    id_user = ID_USER_EXISTANT

    # WHEN
    utilisateur = UtilisateurDAO().trouver_par_id(id_user)

    # THEN
    assert utilisateur is not None
    assert isinstance(utilisateur, Utilisateur)
    assert utilisateur.id_user == id_user
    assert utilisateur.nom_user == NOM_USER_EXISTANT


def test_trouver_par_id_non_existant():
    # GIVEN
    id_user = 9999999999999

    # WHEN
    utilisateur = UtilisateurDAO().trouver_par_id(id_user)

    # THEN
    assert utilisateur is None

# --- Tests de la méthode lister_tous ---

def test_lister_tous():
    # GIVEN

    # WHEN
    utilisateurs = UtilisateurDAO().lister_tous()

    # THEN
    assert isinstance(utilisateurs, list)
    # Note : Le test vérifie juste qu'il y a au moins un utilisateur (alice)
    assert len(utilisateurs) >= 1
    if utilisateurs:
        for u in utilisateurs:
            assert isinstance(u, Utilisateur)

# --- Tests de la méthode creer ---

# Utilise la fixture déplacée 'base_user_name_prefix'
def test_creer_ok(base_user_name_prefix):
    # GIVEN
    nom_unique = base_user_name_prefix + "_creer_ok"
    utilisateur_a_creer = Utilisateur(
        id_user=None,
        nom_user=nom_unique,
        mail_user=f"{nom_unique}@test.io",
        mdp="motdepasse"
    )

    # WHEN
    creation_ok = UtilisateurDAO().creer(utilisateur_a_creer)

    utilisateur_recupere = UtilisateurDAO().trouver_par_id(utilisateur_a_creer.id_user)

    # THEN
    assert creation_ok
    assert utilisateur_a_creer.id_user is not None
    assert utilisateur_recupere is not None
    assert utilisateur_recupere.nom_user == nom_unique

    # NETTOYAGE
    UtilisateurDAO().supprimer(utilisateur_a_creer)


def test_creer_ko_champs_manquants_ou_invalides():
    # GIVEN
    utilisateur_a_creer = Utilisateur(
        id_user=None,
        nom_user=NOM_USER_EXISTANT, 
        mail_user="nouveau_mail@test.io", 
        mdp="motdepasse"
    )

    # WHEN
    creation_ok = UtilisateurDAO().creer(utilisateur_a_creer)

    # THEN
    assert not creation_ok

# --- Tests de la méthode modifier ---

def test_modifier_ok(base_user_name_prefix):
    # GIVEN
    nom_a_modifier = base_user_name_prefix + "_mod_ok"
    utilisateur_original = Utilisateur(
        id_user=None,
        nom_user=nom_a_modifier, 
        mail_user=f"{nom_a_modifier}@avant.fr", 
        mdp="old_mdp"
    )
    UtilisateurDAO().creer(utilisateur_original)
    
    new_mail = f"{nom_a_modifier}@apres.fr"
    new_mdp = "new_mdp_hash"
    
    utilisateur_modifie = Utilisateur(
        id_user=utilisateur_original.id_user,
        nom_user=nom_a_modifier,
        mail_user=new_mail,
        mdp=new_mdp
    )

    # WHEN
    modification_ok = UtilisateurDAO().modifier(utilisateur_modifie)
    
    utilisateur_verif = UtilisateurDAO().trouver_par_id(utilisateur_original.id_user)

    # THEN
    assert modification_ok
    assert utilisateur_verif is not None
    assert utilisateur_verif.mail_user == new_mail
    assert utilisateur_verif.mdp == new_mdp

    # NETTOYAGE
    UtilisateurDAO().supprimer(utilisateur_original)


def test_modifier_ko_id_inconnu():
    # GIVEN
    id_inconnu = 8888888888
    utilisateur_a_modifier = Utilisateur(
        id_user=id_inconnu, 
        nom_user="id_inconnu", 
        mail_user="no@mail.com",
        mdp="dummy"
    )

    # WHEN
    modification_ok = UtilisateurDAO().modifier(utilisateur_a_modifier)

    # THEN
    assert not modification_ok

# --- Tests de la méthode supprimer ---

def test_supprimer_ok(base_user_name_prefix):
    # GIVEN
    nom_a_supprimer = base_user_name_prefix + "_supp_ok"
    utilisateur_a_supprimer = Utilisateur(
        id_user=None,
        nom_user=nom_a_supprimer, 
        mail_user=f"{nom_a_supprimer}@supp.fr", 
        mdp="to_be_deleted"
    )
    UtilisateurDAO().creer(utilisateur_a_supprimer)
    id_supprime = utilisateur_a_supprimer.id_user

    assert UtilisateurDAO().trouver_par_id(id_supprime) is not None

    # WHEN
    suppression_ok = UtilisateurDAO().supprimer(utilisateur_a_supprimer)
    
    utilisateur_apres = UtilisateurDAO().trouver_par_id(id_supprime)

    # THEN
    assert suppression_ok
    assert utilisateur_apres is None


def test_supprimer_ko_id_inconnu():
    # GIVEN
    id_inconnu = 8888888888
    utilisateur_a_supprimer = Utilisateur(
        id_user=id_inconnu, 
        nom_user="id_inconnu", 
        mail_user="no@mail.com",
        mdp="dummy"
    )

    # WHEN
    suppression_ok = UtilisateurDAO().supprimer(utilisateur_a_supprimer)

    # THEN
    assert not suppression_ok

# --- Tests de la méthode se_connecter ---

def test_se_connecter_ok():
    # GIVEN
    pseudo = NOM_USER_EXISTANT
    mdp_hache = MDP_HASH_EXISTANT 

    # WHEN
    utilisateur = UtilisateurDAO().se_connecter(pseudo, mdp_hache)

    # THEN
    assert isinstance(utilisateur, Utilisateur)
    assert utilisateur.nom_user == pseudo


def test_se_connecter_ko_faux_mdp():
    # GIVEN
    pseudo = NOM_USER_EXISTANT
    mdp_hache_incorrect = "ceci_nest_pas_le_bon_hash"

    # WHEN
    utilisateur = UtilisateurDAO().se_connecter(pseudo, mdp_hache_incorrect)

    # THEN
    assert utilisateur is None


def test_se_connecter_ko_faux_nom_user():
    # GIVEN
    pseudo_incorrect = "utilisateur_inconnu_toto"
    mdp_hache = MDP_HASH_EXISTANT

    # WHEN
    utilisateur = UtilisateurDAO().se_connecter(pseudo_incorrect, mdp_hache)

    # THEN
    assert utilisateur is None
