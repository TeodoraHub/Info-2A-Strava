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
            st.rerun()
        
        st.divider()
        
        menu = st.radio(
            "Navigation",
            ["📊 Tableau de bord", "➕ Nouvelle activité", "📁 Upload GPX", "🔍 Mes activités"]
        )
    
    # Contenu principal
    if menu == "📊 Tableau de bord":
        st.title("Tableau de bord")
        st.info("Fonctionnalité à venir: statistiques et graphiques de vos activités")
    
    elif menu == "➕ Nouvelle activité":
        st.title("Créer une nouvelle activité")
        
        with st.form("activity_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                titre = st.text_input("Titre de l'activité*", placeholder="Ex: Course matinale")
                sport = st.selectbox("Type de sport*", ["course", "cyclisme", "natation", "randonnee"])
                date_activite = st.date_input("Date*", value=date.today())
                distance = st.number_input("Distance (km)*", min_value=0.1, step=0.1)
            
            with col2:
                lieu = st.text_input("Lieu*", placeholder="Ex: Parc de la ville")
                duree = st.number_input("Durée (minutes)", min_value=0.0, step=1.0, value=None)
                description = st.text_area("Description", placeholder="Décrivez votre activité...")
            
            submit = st.form_submit_button("Créer l'activité")
            
            if submit:
                if not titre or not lieu:
                    st.error("Veuillez remplir tous les champs obligatoires (*)")
                else:
                    try:
                        response = requests.post(
                            f"{API_URL}/activities",
                            params={
                                "titre": titre,
                                "description": description or "",
                                "sport": sport,
                                "date_activite": date_activite.strftime("%Y-%m-%d"),
                                "lieu": lieu,
                                "distance": distance,
                                "duree": duree if duree and duree > 0 else None
                            },
                            auth=get_auth()
                        )
                        if response.status_code == 200:
                            st.success("✅ Activité créée avec succès!")
                            st.balloons()
                        else:
                            st.error(f"Erreur: {response.json().get('detail', 'Erreur inconnue')}")
                    except Exception as e:
                        st.error(f"Erreur lors de la création: {str(e)}")
    
    elif menu == "📁 Upload GPX":
        st.title("Importer un fichier GPX")
        st.write("Uploadez un fichier GPX pour extraire automatiquement les données de votre activité")
        
        uploaded_file = st.file_uploader("Choisir un fichier GPX", type=["gpx"])
        
        if uploaded_file is not None:
            try:
                files = {"file": (uploaded_file.name, uploaded_file, "application/gpx+xml")}
                response = requests.post(f"{API_URL}/upload-gpx", files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    st.success("Fichier GPX analysé avec succès!")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Nom", data.get("nom", "N/A"))
                        st.metric("Type", data.get("type", "N/A"))
                        st.metric("Distance totale", f"{data.get('distance totale (km)', 0):.2f} km")
                        st.metric("Durée totale", f"{data.get('durée totale (min)', 0):.1f} min")
                    
                    with col2:
                        st.metric("Temps en mouvement", f"{data.get('temps en mouvement (min)', 0):.1f} min")
                        st.metric("Distance en mouvement", f"{data.get('distance en mouvement (km)', 0):.2f} km")
                        st.metric("Vitesse moyenne", f"{data.get('vitesse moyenne (km/h)', 0):.2f} km/h")
                        st.metric("Vitesse max", f"{data.get('vitesse max (km/h)', 0):.2f} km/h")
                    
                    st.info("💡 Vous pouvez maintenant créer une activité avec ces données dans l'onglet 'Nouvelle activité'")
                else:
                    st.error("Erreur lors de l'analyse du fichier GPX")
            except Exception as e:
                st.error(f"Erreur: {str(e)}")
    
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