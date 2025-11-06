import streamlit as st
import requests
from datetime import date
import pandas as pd

# Configuration de la page
st.set_page_config(
    page_title="Striv - Application de sport",
    page_icon="🏃",
    layout="wide"
)

# URL de base de l'API
API_URL = "http://localhost:8001"

# Initialisation de la session
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None
if "password" not in st.session_state:
    st.session_state.password = None
if "user_info" not in st.session_state:
    st.session_state.user_info = None
if "gpx_data" not in st.session_state:
    st.session_state.gpx_data = None

# Fonction d'authentification
def get_auth():
    if st.session_state.authenticated:
        return (st.session_state.username, st.session_state.password)
    return None

# Interface de connexion/inscription
if not st.session_state.authenticated:
    st.title("🏃 Striv - Application de sport connectée")
    
    tab1, tab2 = st.tabs(["Connexion", "Inscription"])
    
    with tab1:
        st.subheader("Connexion")
        with st.form("login_form"):
            username = st.text_input("Nom d'utilisateur")
            password = st.text_input("Mot de passe", type="password")
            submit = st.form_submit_button("Se connecter")
            
            if submit:
                try:
                    response = requests.post(
                        f"{API_URL}/login",
                        params={"username": username, "password": password}
                    )
                    if response.status_code == 200:
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.session_state.password = password
                        st.session_state.user_info = response.json()["user"]
                        st.success("Connexion réussie!")
                        st.rerun()
                    else:
                        st.error("Identifiants incorrects")
                except Exception as e:
                    st.error(f"Erreur de connexion: {str(e)}")
    
    with tab2:
        st.subheader("Créer un compte")
        with st.form("signup_form"):
            new_username = st.text_input("Nom d'utilisateur")
            new_email = st.text_input("Email")
            new_password = st.text_input("Mot de passe", type="password")
            confirm_password = st.text_input("Confirmer le mot de passe", type="password")
            submit_signup = st.form_submit_button("S'inscrire")
            
            if submit_signup:
                if new_password != confirm_password:
                    st.error("Les mots de passe ne correspondent pas")
                elif len(new_password) < 4:
                    st.error("Le mot de passe doit contenir au moins 4 caractères")
                else:
                    try:
                        response = requests.post(
                            f"{API_URL}/users",
                            params={
                                "nom_user": new_username,
                                "mail_user": new_email,
                                "mdp": new_password
                            }
                        )
                        if response.status_code == 200:
                            st.success("Compte créé avec succès! Vous pouvez maintenant vous connecter.")
                        else:
                            st.error(f"Erreur: {response.json().get('detail', 'Erreur inconnue')}")
                    except Exception as e:
                        st.error(f"Erreur lors de la création: {str(e)}")

# Interface principale (après connexion)
else:
    # Sidebar
    with st.sidebar:
        st.title("🏃 Striv")
        st.write(f"Bienvenue, **{st.session_state.user_info['username']}**")
        st.write(f"📧 {st.session_state.user_info['email']}")
        
        if st.button("Se déconnecter"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.password = None
            st.session_state.user_info = None
            st.session_state.gpx_data = None
            st.rerun()
        
        st.divider()
        
        menu = st.radio(
            "Navigation",
            ["📊 Tableau de bord", "➕ Nouvelle activité", "🔍 Mes activités"]
        )
    
    # Contenu principal
    if menu == "📊 Tableau de bord":
        st.title("Tableau de bord")
        st.info("Fonctionnalité à venir: statistiques et graphiques de vos activités")
    
    elif menu == "➕ Nouvelle activité":
        st.title("Créer une nouvelle activité")
        
        # Section d'import GPX
        st.subheader("📁 Importer un fichier GPX (optionnel)")
        uploaded_file = st.file_uploader("Choisir un fichier GPX pour pré-remplir le formulaire", type=["gpx"])
        
        if uploaded_file is not None:
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/gpx+xml")}
                response = requests.post(f"{API_URL}/upload-gpx", files=files)
                
                if response.status_code == 200:
                    st.session_state.gpx_data = response.json()
                    st.success("✅ Fichier GPX analysé! Les données ont été chargées dans le formulaire ci-dessous.")
                else:
                    st.error("Erreur lors de l'analyse du fichier GPX")
                    st.session_state.gpx_data = None
            except Exception as e:
                st.error(f"Erreur: {str(e)}")
                st.session_state.gpx_data = None
        
        if st.session_state.gpx_data and st.button("🗑️ Effacer les données GPX"):
            st.session_state.gpx_data = None
            st.rerun()
        
        st.divider()
        
        # Pré-remplir les valeurs avec les données GPX si disponibles
        gpx = st.session_state.gpx_data or {}
        
        # Mapping du type GPX vers les types de sport
        type_mapping = {
            "running": "course",
            "cycling": "cyclisme",
            "swimming": "natation",
            "hiking": "randonnee"
        }
        
        default_titre = gpx.get("nom") or ""
        default_sport_gpx = gpx.get("type", "").lower()
        default_sport = type_mapping.get(default_sport_gpx, "course")
        default_distance = gpx.get("distance totale (km)", 0.1)
        default_duree = gpx.get("temps en mouvement (min)", 0.0)
        
        with st.form("activity_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                titre = st.text_input(
                    "Titre de l'activité*", 
                    value=default_titre,
                    placeholder="Ex: Course matinale"
                )
                
                # Index du sport par défaut
                sports_list = ["course", "cyclisme", "natation", "randonnee"]
                sport_index = sports_list.index(default_sport) if default_sport in sports_list else 0
                sport = st.selectbox("Type de sport*", sports_list, index=sport_index)
                
                date_activite = st.date_input("Date*", value=date.today())
                
                distance = st.number_input(
                    "Distance (km)*", 
                    min_value=0.1, 
                    step=0.1,
                    value=float(default_distance) if default_distance > 0 else 0.1
                )
            
            with col2:
                lieu = st.text_input("Lieu*", placeholder="Ex: Parc de la ville")
                
                duree = st.number_input(
                    "Durée (minutes)", 
                    min_value=0.0, 
                    step=1.0,
                    value=float(default_duree) if default_duree > 0 else 0.0
                )
                
                description = st.text_area("Description", placeholder="Décrivez votre activité...")
            
            # Afficher un résumé des données GPX si disponibles
            if st.session_state.gpx_data:
                st.info(f"""
                📊 **Données du fichier GPX:**
                - Vitesse moyenne: {gpx.get('vitesse moyenne (km/h)', 0):.2f} km/h
                - Vitesse max: {gpx.get('vitesse max (km/h)', 0):.2f} km/h
                - Distance en mouvement: {gpx.get('distance en mouvement (km)', 0):.2f} km
                """)
            
            submit = st.form_submit_button("Créer l'activité", type="primary")
            
            if submit:
                if not titre or not lieu:
                    st.error("Veuillez remplir tous les champs obligatoires (*)")
                else:
                    try:
                        # Préparer les paramètres
                        params = {
                            "titre": titre,
                            "description": description or "",
                            "sport": sport,
                            "date_activite": date_activite.strftime("%Y-%m-%d"),
                            "lieu": lieu,
                            "distance": distance,
                        }
                        
                        # Ajouter la durée seulement si elle est définie
                        if duree and duree > 0:
                            params["duree"] = duree
                        
                        response = requests.post(
                            f"{API_URL}/activities",
                            params=params,
                            auth=get_auth()
                        )
                        
                        if response.status_code == 200:
                            st.success("✅ Activité créée avec succès!")
                            st.balloons()
                            # Réinitialiser les données GPX après création
                            st.session_state.gpx_data = None
                        else:
                            st.error(f"Erreur: {response.json().get('detail', 'Erreur inconnue')}")
                    except Exception as e:
                        st.error(f"Erreur lors de la création: {str(e)}")
    
    elif menu == "🔍 Mes activités":
        st.title("Mes activités")
        st.info("Fonctionnalité à venir: liste et recherche de vos activités")
        
        # Exemple d'affichage d'une activité
        st.subheader("Rechercher une activité par ID")
        activity_id = st.number_input("ID de l'activité", min_value=1, step=1)
        
        if st.button("Rechercher"):
            try:
                response = requests.get(
                    f"{API_URL}/activities/{activity_id}",
                    auth=get_auth()
                )
                if response.status_code == 200:
                    activity = response.json()
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Titre:** {activity.get('titre')}")
                        st.write(f"**Sport:** {activity.get('sport')}")
                        st.write(f"**Date:** {activity.get('date_activite')}")
                        st.write(f"**Lieu:** {activity.get('lieu')}")
                    
                    with col2:
                        st.write(f"**Distance:** {activity.get('distance')} km")
                        st.write(f"**Durée:** {activity.get('duree')} min")
                        st.write(f"**Description:** {activity.get('description')}")
                    
                    if st.button("🗑️ Supprimer cette activité", type="secondary"):
                        try:
                            del_response = requests.delete(
                                f"{API_URL}/activities/{activity_id}",
                                auth=get_auth()
                            )
                            if del_response.status_code == 200:
                                st.success("Activité supprimée avec succès!")
                            else:
                                st.error(f"Erreur: {del_response.json().get('detail')}")
                        except Exception as e:
                            st.error(f"Erreur: {str(e)}")
                elif response.status_code == 404:
                    st.warning("Activité non trouvée")
                else:
                    st.error("Erreur lors de la récupération de l'activité")
            except Exception as e:
                st.error(f"Erreur: {str(e)}")