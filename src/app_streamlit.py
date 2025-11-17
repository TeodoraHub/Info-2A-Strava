# streamlit run src/app_streamlit.py --server.port=5501 --server.address=0.0.0.0
from datetime import date, datetime

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

from utils.format import format_h_m

color_map = {
    "Course": "#EF476F",
    "Cyclisme": "#FFD166",
    "Natation": "#118AB2",
    "Randonnee": "#06D6A0",
}

# Configuration de la page
st.set_page_config(page_title="Striv - Application de sport", page_icon="🏃", layout="wide")

# URL de base de l'API
API_URL = "http://localhost:5000"

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
if "route_data" not in st.session_state:
    st.session_state.route_data = None
if "start_coords" not in st.session_state:
    st.session_state.start_coords = None
if "end_coords" not in st.session_state:
    st.session_state.end_coords = None
if "start_address" not in st.session_state:
    st.session_state.start_address = None
if "end_address" not in st.session_state:
    st.session_state.end_address = None


# Fonction d'authentification
def get_auth():
    if st.session_state.authenticated:
        return (st.session_state.username, st.session_state.password)
    return None


# Interface de connexion/inscription
if not st.session_state.authenticated:
    st.title("🏃 Striv - Application de sport connectée")
    st.markdown(
        "### Alternative gratuite et sans abonnement pour le suivi de vos activités sportives"
    )

    tab1, tab2 = st.tabs(["Connexion", "Inscription"])

    with tab1:
        st.subheader("Connexion")
        with st.form("login_form"):
            username = st.text_input("Nom d'utilisateur")
            password = st.text_input("Mot de passe", type="password")
            submit = st.form_submit_button("Se connecter", width="stretch")

            if submit:
                try:
                    response = requests.post(
                        f"{API_URL}/login", params={"username": username, "password": password}
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
            submit_signup = st.form_submit_button("S'inscrire", width="stretch")

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
                                "mdp": new_password,
                            },
                        )
                        if response.status_code == 200:
                            st.success(
                                "Compte créé avec succès! Vous pouvez maintenant vous connecter."
                            )
                        else:
                            st.error(f"Erreur: {response.json().get('detail', 'Erreur inconnue')}")
                    except Exception as e:
                        st.error(f"Erreur lors de la création: {str(e)}")

# Interface principale (après connexion)
else:
    # Sidebar
    with st.sidebar:
        st.title("🏃 Striv")
        st.write(f"**{st.session_state.user_info['username']}**")
        st.write(f"📧 {st.session_state.user_info['email']}")

        if st.button("🚪 Se déconnecter", width="stretch"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.password = None
            st.session_state.user_info = None
            st.session_state.gpx_data = None
            st.rerun()

        st.divider()

        menu = st.radio(
            "Navigation",
            [
                "📊 Tableau de bord",
                "🌐 Fil d'actualité",
                "➕ Nouvelle activité",
                "🗺️ Créer un parcours",
                "🔍 Mes activités",
                "👥 Communauté",
                "📈 Statistiques",
            ],
        )

    # ============================================================================
    # TABLEAU DE BORD
    # ============================================================================
    if menu == "📊 Tableau de bord":
        st.title("📊 Tableau de bord")

        try:
            # En-tête avec profil utilisateur
            col1, col2, col3 = st.columns([1, 3, 1])

            with col1:
                # Avatar avec initiales
                initials = "".join(
                    [word[0].upper() for word in st.session_state.user_info["username"].split()]
                )
                avatar_color = "#FF6B6B"
                st.markdown(
                    f"""
                <div style="
                    width: 80px;
                    height: 80px;
                    background: {avatar_color};
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 32px;
                    color: white;
                    font-weight: bold;
                    margin: 0 auto;
                ">
                    {initials}
                </div>
                """,
                    unsafe_allow_html=True,
                )

            with col2:
                st.markdown(f"### Bienvenue, **{st.session_state.user_info['username']}**! 👋")
                st.caption(f"📧 {st.session_state.user_info['email']}")
                st.caption(f"📅 Aujourd'hui: {datetime.now().strftime('%d %B %Y')}")

            with col3:
                pass

            st.divider()

            # Statistiques globales
            response_global = requests.get(f"{API_URL}/stats/global", auth=get_auth())

            if response_global.status_code == 200:
                stats = response_global.json()

                # Cartes de statistiques
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(label="🏃 Activités totales", value=stats.get("total_activites", 0))

                with col2:
                    st.metric(
                        label="📏 Distance totale",
                        value=f"{stats.get('distance_totale', 0):.1f} km",
                    )

                with col3:
                    st.metric(
                        label="⏱️ Durée totale", value=f"{format_h_m(stats.get('duree_totale'))}"
                    )

                with col4:
                    st.metric(
                        label="🏅 Sport favori",
                        value=stats.get("sport_favori", "Aucun").capitalize(),
                    )

                st.divider()

                # Conteneur principal avec 3 colonnes
                col_left, col_middle, col_right = st.columns([1.5, 1, 1])

                # ===== COLONNE GAUCHE: Dernière activité =====
                with col_left:
                    st.subheader("🎯 Dernière activité")

                    try:
                        response_activities = requests.get(
                            f"{API_URL}/stats/user/{st.session_state.user_info['id']}/monthly",
                            auth=get_auth(),
                        )

                        if response_activities.status_code == 200:
                            activities = response_activities.json()

                            if activities:
                                last_activity = activities[0]

                                st.markdown(
                                    f"""
                                <div style="
                                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                    padding: 20px;
                                    border-radius: 10px;
                                    color: white;
                                ">
                                    <h4 style="margin: 0 0 10px 0;">🏃 {last_activity.get("titre", "Sans titre")}</h4>
                                    <p style="margin: 5px 0;"><b>Sport:</b> {last_activity.get("sport", "N/A").capitalize()}</p>
                                    <p style="margin: 5px 0;"><b>Distance:</b> {last_activity.get("distance", 0):.2f} km</p>
                                    <p style="margin: 5px 0;"><b>Durée:</b> {format_h_m(last_activity.get("duree_heures", 0))}</p>
                                    <p style="margin: 5px 0;"><b>Date:</b> {last_activity.get("date_activite", "N/A")}</p>
                                    <p style="margin: 5px 0;"><b>Lieu:</b> {last_activity.get("lieu", "N/A")}</p>
                                </div>
                                """,
                                    unsafe_allow_html=True,
                                )
                            else:
                                st.info("Aucune activité créée. Commencez par en créer une!")
                    except Exception as e:
                        st.warning(f"Erreur: {str(e)}")

                # ===== COLONNE MIDDLE: Abonnements =====
                with col_middle:
                    st.subheader("📲 Abonnements")

                    try:
                        response_following = requests.get(
                            f"{API_URL}/users/{st.session_state.user_info['id']}/following",
                            auth=get_auth(),
                        )

                        if response_following.status_code == 200:
                            following = response_following.json()
                            count_following = len(following)

                            st.markdown(
                                f"""
                            <div style="
                                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                                padding: 20px;
                                border-radius: 10px;
                                color: white;
                                text-align: center;
                            ">
                                <h2 style="margin: 0;">{count_following}</h2>
                                <p style="margin: 5px 0;">Utilisateurs suivis</p>
                            </div>
                            """,
                                unsafe_allow_html=True,
                            )

                            if following:
                                st.markdown("**Vos suivis:**")
                                for user in following[:5]:
                                    st.caption(f"👤 {user['nom_user']}")
                                if count_following > 5:
                                    st.caption(f"... et {count_following - 5} autres")
                    except Exception as e:
                        st.warning(f"Erreur: {str(e)}")

                # ===== COLONNE DROITE: Abonnés =====
                with col_right:
                    st.subheader("🔔 Abonnés")

                    try:
                        response_followers = requests.get(
                            f"{API_URL}/users/{st.session_state.user_info['id']}/followers",
                            auth=get_auth(),
                        )

                        if response_followers.status_code == 200:
                            followers = response_followers.json()
                            count_followers = len(followers)

                            st.markdown(
                                f"""
                            <div style="
                                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                                padding: 20px;
                                border-radius: 10px;
                                color: white;
                                text-align: center;
                            ">
                                <h2 style="margin: 0;">{count_followers}</h2>
                                <p style="margin: 5px 0;">Vous suivent</p>
                            </div>
                            """,
                                unsafe_allow_html=True,
                            )

                            if followers:
                                st.markdown("**Vos abonnés:**")
                                for user in followers[:5]:
                                    st.caption(f"👤 {user['nom_user']}")
                                if count_followers > 5:
                                    st.caption(f"... et {count_followers - 5} autres")
                    except Exception as e:
                        st.warning(f"Erreur: {str(e)}")

                st.divider()

                # Graphiques par sport
                if stats.get("par_sport"):
                    st.subheader("📊 Répartition par sport")

                    sports_data = stats["par_sport"]
                    df_sports = pd.DataFrame(
                        [
                            {
                                "Sport": sport.capitalize(),
                                "Activités": data.get("count", 0),
                                "Distance (km)": data.get("distance", 0),
                                "Durée (h)": data.get("duree", 0),
                            }
                            for sport, data in sports_data.items()
                        ]
                    )
                    df_sports = df_sports.sort_values("Distance (km)", ascending=False)

                    col1, col2 = st.columns(2)

                    with col1:
                        fig_activites_dashboard = px.pie(
                            df_sports,
                            names="Sport",
                            values="Activités",
                            title="Nombre d'activités par sport",
                            color="Sport",
                            color_discrete_map=color_map
                        )
                        st.plotly_chart(fig_activites_dashboard, width="stretch")

                    with col2:
                        fig_distance_dashboard = px.bar(
                            df_sports,
                            y="Distance (km)",
                            x="Sport",
                            title="Répartition des distances par sport",
                            color="Sport",
                            color_discrete_map=color_map
                        )
                        st.plotly_chart(fig_distance_dashboard, width="stretch")

            else:
                st.info(
                    "ℹ️ Aucune statistique disponible pour le moment. Commencez par créer une activité !"
                )

        except Exception as e:
            st.error(f"Erreur lors de la récupération des statistiques: {str(e)}")

    # ============================================================================
    # FIL D'ACTUALITÉ (F2)
    # ============================================================================
    elif menu == "🌐 Fil d'actualité":
        st.title("🌐 Fil d'actualité")
        st.markdown("*Activités des utilisateurs que vous suivez*")

        try:
            response = requests.get(f"{API_URL}/feed", auth=get_auth())

            if response.status_code == 200:
                activities = response.json()

                if not activities:
                    st.info(
                        "Votre fil d'actualité est vide. Suivez d'autres utilisateurs pour voir leurs activités !"
                    )
                else:
                    for activity in activities:
                        with st.container():
                            col1, col2 = st.columns([3, 1])

                            with col1:
                                st.subheader(f"🏃 {activity.get('titre', 'Sans titre')}")
                                st.caption(
                                    f"📝 Publié par Utilisateur **{activity.get('id_user')}**"
                                )
                                st.write(f"**Sport:** {activity.get('sport', 'N/A').capitalize()}")
                                st.write(f"**Distance:** {activity.get('distance', 0):.2f} km")
                                if activity.get("duree_heures"):
                                    st.write(
                                        f"**Durée:** {format_h_m(activity.get('duree_heures'))}"
                                    )
                                st.write(f"**Date:** {activity.get('date_activite', 'N/A')}")
                                if activity.get("lieu"):
                                    st.write(f"**Lieu:** {activity.get('lieu')}")

                            with col2:
                                activity_id = activity.get("id")

                                # Récupérer les likes
                                likes_response = requests.get(
                                    f"{API_URL}/activities/{activity_id}/likes", auth=get_auth()
                                )
                                likes_count = 0
                                user_liked = False
                                if likes_response.status_code == 200:
                                    likes_data = likes_response.json()
                                    likes_count = likes_data.get("likes_count", 0)
                                    user_liked = any(
                                        like["id_user"] == st.session_state.user_info["id"]
                                        for like in likes_data.get("likes", [])
                                    )

                                # Bouton like/unlike
                                if user_liked:
                                    if st.button(f"💙 {likes_count}", key=f"unlike_{activity_id}"):
                                        requests.delete(
                                            f"{API_URL}/activities/{activity_id}/like",
                                            auth=get_auth(),
                                        )
                                        st.rerun()
                                else:
                                    if st.button(f"🤍 {likes_count}", key=f"like_{activity_id}"):
                                        requests.post(
                                            f"{API_URL}/activities/{activity_id}/like",
                                            auth=get_auth(),
                                        )
                                        st.rerun()

                            # Section commentaires (F3)
                            with st.expander("💬 Commentaires"):
                                # Récupérer les commentaires
                                comments_response = requests.get(
                                    f"{API_URL}/activities/{activity_id}/comments", auth=get_auth()
                                )

                                if comments_response.status_code == 200:
                                    comments_data = comments_response.json()
                                    comments = comments_data.get("comments", [])

                                    if comments:
                                        for comment in comments:
                                            st.write(
                                                f"**Utilisateur {comment['id_user']}:** {comment['contenu']}"
                                            )
                                            st.caption(f"Le {comment['date_comment']}")
                                    else:
                                        st.write("Aucun commentaire pour le moment")

                                # Formulaire pour ajouter un commentaire
                                with st.form(key=f"comment_form_{activity_id}"):
                                    new_comment = st.text_area(
                                        "Ajouter un commentaire", key=f"comment_text_{activity_id}"
                                    )
                                    submit_comment = st.form_submit_button("Envoyer")

                                    if submit_comment and new_comment:
                                        comment_response = requests.post(
                                            f"{API_URL}/activities/{activity_id}/comments",
                                            params={"contenu": new_comment},
                                            auth=get_auth(),
                                        )
                                        if comment_response.status_code == 200:
                                            st.success("Commentaire ajouté!")
                                            st.rerun()

                            st.divider()
            else:
                st.error("Erreur lors de la récupération du fil d'actualité")

        except Exception as e:
            st.error(f"Erreur: {str(e)}")

    # ============================================================================
    # NOUVELLE ACTIVITÉ (F1)
    # ============================================================================
    elif menu == "➕ Nouvelle activité":
        st.title("➕ Créer une nouvelle activité")

        # Section d'import GPX
        st.subheader("📁 Importer un fichier GPX (optionnel)")
        uploaded_file = st.file_uploader(
            "Choisir un fichier GPX pour pré-remplir le formulaire", type=["gpx"]
        )

        # ========== SECTION 1: Télécharger GPX (ligne ~430) ==========
        if uploaded_file is not None:
            try:
                files = {
                    "file": (uploaded_file.name, uploaded_file.getvalue(), "application/gpx+xml")
                }
                response = requests.post(
                    f"{API_URL}/activities/upload-gpx", files=files
                )  # ✅ CHANGÉ

                if response.status_code == 200:
                    st.session_state.gpx_data = response.json()
                    st.success(
                        "✅ Fichier GPX analysé! Les données ont été chargées dans le formulaire ci-dessous."
                    )
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
            "hiking": "randonnee",
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
                    "Titre de l'activité*", value=default_titre, placeholder="Ex: Course matinale"
                )

                # Index du sport par défaut
                sports_list = ["course", "cyclisme", "natation", "randonnee"]
                sport_index = (
                    sports_list.index(default_sport) if default_sport in sports_list else 0
                )
                sport = st.selectbox("Type de sport*", sports_list, index=sport_index)

                date_activite = st.date_input("Date*", value=date.today())

                distance = st.number_input(
                    "Distance (km)*",
                    min_value=0.1,
                    step=0.1,
                    value=float(default_distance) if default_distance > 0 else 0.1,
                )

            with col2:
                lieu = st.text_input("Lieu*", placeholder="Ex: Parc de la ville")

                duree = st.number_input(
                    "Durée (heures)",
                    min_value=0.0,
                    step=0.1,
                    value=float(default_duree / 60) if default_duree > 0 else 0.0,
                )

                description = st.text_area("Description", placeholder="Décrivez votre activité...")

            # Afficher un résumé des données GPX si disponibles
            if st.session_state.gpx_data:
                st.info(f"""
                📊 **Données du fichier GPX:**
                - Vitesse moyenne: {gpx.get("vitesse moyenne (km/h)", 0):.2f} km/h
                - Vitesse max: {gpx.get("vitesse max (km/h)", 0):.2f} km/h
                - Distance en mouvement: {gpx.get("distance en mouvement (km)", 0):.2f} km
                """)

            submit = st.form_submit_button("Créer l'activité", type="primary", width="stretch")

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
                            f"{API_URL}/activities", params=params, auth=get_auth()
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

    # ============================================================================
    # MES ACTIVITÉS (F1)
    # ============================================================================
    elif menu == "🔍 Mes activités":
        st.title("🔍 Mes activités")

        # Filtres
        col1, col2 = st.columns(2)
        with col1:
            filtre_sport = st.selectbox(
                "Filtrer par sport", ["Tous", "course", "cyclisme", "natation", "randonnee"]
            )

        try:
            # Récupérer les activités
            params = {}
            if filtre_sport != "Tous":
                params["sport"] = filtre_sport

            response = requests.get(
                f"{API_URL}/stats/user/{st.session_state.user_info['id']}/monthly",  # ✅ CHANGÉ
                params=params,
                auth=get_auth(),
            )

            if response.status_code == 200:
                activities = response.json()

                if not activities:
                    st.info("Vous n'avez pas encore d'activités. Créez-en une !")
                else:
                    st.write(f"**{len(activities)} activité(s) trouvée(s)**")

                    for activity in activities:
                        with st.expander(
                            f"🏃 {activity.get('titre', 'Sans titre')} - {activity.get('date_activite', 'N/A')}"
                        ):
                            col1, col2, col3 = st.columns([2, 2, 1])

                            with col1:
                                st.write(f"**Sport:** {activity.get('sport', 'N/A').capitalize()}")
                                st.write(f"**Distance:** {activity.get('distance', 0):.2f} km")
                                if activity.get("duree_heures"):
                                    st.write(
                                        f"**Durée:** {format_h_m(activity.get('duree_heures'))}"
                                    )

                            with col2:
                                st.write(f"**Date:** {activity.get('date_activite', 'N/A')}")
                                if activity.get("lieu"):
                                    st.write(f"**Lieu:** {activity.get('lieu')}")

                            with col3:
                                activity_id = activity.get("id")

                                # Bouton modifier
                                if st.button("✏️ Modifier", key=f"edit_{activity_id}"):
                                    st.session_state[f"editing_{activity_id}"] = True
                                    st.rerun()

                                # Bouton supprimer
                                if st.button("🗑️ Supprimer", key=f"delete_{activity_id}"):
                                    if st.session_state.get(f"confirm_delete_{activity_id}"):
                                        response_del = requests.delete(
                                            f"{API_URL}/activities/{activity_id}", auth=get_auth()
                                        )
                                        if response_del.status_code == 200:
                                            st.success("Activité supprimée!")
                                            del st.session_state[f"confirm_delete_{activity_id}"]
                                            st.rerun()
                                    else:
                                        st.session_state[f"confirm_delete_{activity_id}"] = True
                                        st.warning("Cliquez à nouveau pour confirmer")

                            # Formulaire de modification
                            if st.session_state.get(f"editing_{activity_id}"):
                                st.divider()
                                st.subheader("Modifier l'activité")

                                with st.form(key=f"edit_form_{activity_id}"):
                                    new_titre = st.text_input(
                                        "Titre", value=activity.get("titre", "")
                                    )
                                    new_lieu = st.text_input("Lieu", value=activity.get("lieu", ""))
                                    new_distance = st.number_input(
                                        "Distance (km)",
                                        value=float(activity.get("distance", 0)),
                                        min_value=0.1,
                                        step=0.1,
                                    )
                                    new_duree = st.number_input(
                                        "Durée (heures)",
                                        value=float(activity.get("duree_heures", 0)),
                                        min_value=0.0,
                                        step=0.1,
                                    )

                                    col1, col2 = st.columns(2)
                                    with col1:
                                        submit_edit = st.form_submit_button(
                                            "✅ Enregistrer", width="stretch"
                                        )
                                    with col2:
                                        cancel_edit = st.form_submit_button(
                                            "❌ Annuler", width="stretch"
                                        )

                                    if submit_edit:
                                        response_update = requests.put(
                                            f"{API_URL}/activities/{activity_id}",
                                            params={
                                                "titre": new_titre,
                                                "lieu": new_lieu,
                                                "distance": new_distance,
                                                "duree": new_duree,
                                            },
                                            auth=get_auth(),
                                        )
                                        if response_update.status_code == 200:
                                            st.success("Activité modifiée!")
                                            del st.session_state[f"editing_{activity_id}"]
                                            st.rerun()
                                        else:
                                            st.error("Erreur lors de la modification")

                                    if cancel_edit:
                                        del st.session_state[f"editing_{activity_id}"]
                                        st.rerun()
            else:
                st.error("Erreur lors de la récupération des activités")

        except Exception as e:
            st.error(f"Erreur: {str(e)}")

    # ============================================================================
    # CRÉER UN PARCOURS (NOUVEAU)
    # ============================================================================
    elif menu == "🗺️ Créer un parcours":
        st.title("🗺️ Créer un parcours")
        st.markdown("*Créez un parcours en saisissant une adresse de départ et d'arrivée*")

        import folium
        from streamlit_folium import st_folium

        from utils.geolocation import get_coordinates, get_route

        col1, col2 = st.columns(2)

        with col1:
            start_address = st.text_input(
                "Adresse de départ*", placeholder="Ex: 123 Rue de Paris, 75000 Paris"
            )

        with col2:
            end_address = st.text_input(
                "Adresse d'arrivée*", placeholder="Ex: 456 Avenue de Lyon, 75012 Paris"
            )

        if st.button("🔍 Calculer l'itinéraire", type="primary", width="stretch"):
            if not start_address or not end_address:
                st.error("Veuillez remplir les deux adresses")
            else:
                with st.spinner("Calcul de l'itinéraire..."):
                    # Récupérer les coordonnées
                    start_coords = get_coordinates(start_address)
                    end_coords = get_coordinates(end_address)

                    if not start_coords or not end_coords:
                        st.error("❌ Une ou plusieurs adresses sont invalides. Veuillez vérifier.")
                    else:
                        # Récupérer l'itinéraire
                        route_data = get_route(start_coords, end_coords)

                        if route_data:
                            st.session_state.route_data = route_data
                            st.session_state.start_coords = start_coords
                            st.session_state.end_coords = end_coords
                            st.session_state.start_address = start_address
                            st.session_state.end_address = end_address
                            st.success("✅ Itinéraire calculé!")
                        else:
                            st.error("❌ Erreur lors du calcul de l'itinéraire")

        st.divider()

        # Afficher la carte si un itinéraire est calculé
        if st.session_state.get("route_data"):
            route_data = st.session_state.route_data
            start_coords = st.session_state.start_coords
            end_coords = st.session_state.end_coords

            # Créer la carte
            center_lat = (start_coords[0] + end_coords[0]) / 2
            center_lon = (start_coords[1] + end_coords[1]) / 2

            m = folium.Map(location=[center_lat, center_lon], zoom_start=13, tiles="OpenStreetMap")

            # Ajouter les points de départ et d'arrivée
            folium.Marker(
                location=start_coords,
                popup="🟢 Départ",
                tooltip="Point de départ",
                icon=folium.Icon(color="green", icon="play"),
            ).add_to(m)

            folium.Marker(
                location=end_coords,
                popup="🔴 Arrivée",
                tooltip="Point d'arrivée",
                icon=folium.Icon(color="red", icon="stop"),
            ).add_to(m)

            # Ajouter la route
            folium.PolyLine(
                locations=route_data["coordinates"], color="#667eea", weight=4, opacity=0.8
            ).add_to(m)

            # Afficher la carte
            st_folium(m, width=1400, height=500)

            st.divider()

            # Afficher les statistiques du parcours
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(label="📏 Distance", value=f"{route_data['distance']:.2f} km")

            with col2:
                st.metric(label="⏱️ Durée estimée", value=f"{route_data['duration']:.1f}h")

            with col3:
                st.metric(
                    label="📍 Vitesse moyenne",
                    value=f"{route_data['distance'] / route_data['duration']:.1f} km/h",
                )

            st.divider()

            # Formulaire pour sauvegarder comme activité
            st.subheader("💾 Sauvegarder ce parcours comme activité")

            with st.form("route_to_activity"):
                col1, col2 = st.columns(2)

                with col1:
                    titre = st.text_input("Titre du parcours*", placeholder="Ex: Parcours matinal")
                    sport = st.selectbox("Type de sport*", ["course", "cyclisme", "randonnee"])

                with col2:
                    date_parcours = st.date_input("Date*", value=date.today())
                    description = st.text_area("Description", placeholder="Décrivez ce parcours...")

                col1, col2 = st.columns(2)
                with col1:
                    start_addr_display = st.text_input(
                        "Lieu de départ", value=st.session_state.start_address, disabled=True
                    )

                with col2:
                    end_addr_display = st.text_input(
                        "Lieu d'arrivée", value=st.session_state.end_address, disabled=True
                    )

                submit_route = st.form_submit_button(
                    "💾 Sauvegarder comme activité", type="primary", width="stretch"
                )

                if submit_route:
                    if not titre:
                        st.error("Veuillez entrer un titre")
                    else:
                        try:
                            params = {
                                "titre": titre,
                                "description": description,
                                "sport": sport,
                                "date_activite": date_parcours.strftime("%Y-%m-%d"),
                                "lieu": f"De {st.session_state.start_address} à {st.session_state.end_address}",
                                "distance": route_data["distance"],
                                "duree": route_data["duration"],
                            }

                            response = requests.post(
                                f"{API_URL}/activities", params=params, auth=get_auth()
                            )

                            if response.status_code == 200:
                                st.success("✅ Parcours sauvegardé comme activité!")
                                st.balloons()
                                # Réinitialiser
                                del st.session_state.route_data
                                del st.session_state.start_coords
                                del st.session_state.end_coords
                                st.rerun()
                            else:
                                st.error("Erreur lors de la sauvegarde")
                        except Exception as e:
                            st.error(f"Erreur: {str(e)}")

    # ============================================================================
    # COMMUNAUTÉ
    # ============================================================================
    elif menu == "👥 Communauté":
        st.title("👥 Communauté")

        tab1, tab2, tab3 = st.tabs(["Tous les utilisateurs", "Mes abonnements", "Mes abonnés"])

        with tab1:
            st.subheader("Utilisateurs disponibles")
            try:
                response = requests.get(f"{API_URL}/users", auth=get_auth())

                if response.status_code == 200:
                    users = response.json()

                    if not users:
                        st.info("Aucun autre utilisateur pour le moment")
                    else:
                        for user in users:
                            col1, col2 = st.columns([3, 1])

                            with col1:
                                st.write(f"**{user['nom_user']}**")
                                st.caption(user["mail_user"])

                            with col2:
                                # Vérifier si on suit déjà cet utilisateur
                                is_following_response = requests.get(
                                    f"{API_URL}/users/{st.session_state.user_info['id']}/is-following/{user['id_user']}",
                                    auth=get_auth(),
                                )

                                is_following = False
                                if is_following_response.status_code == 200:
                                    is_following = is_following_response.json().get(
                                        "is_following", False
                                    )

                                if is_following:
                                    if st.button(
                                        "❌ Ne plus suivre", key=f"unfollow_{user['id_user']}"
                                    ):
                                        requests.delete(
                                            f"{API_URL}/users/{user['id_user']}/follow",
                                            auth=get_auth(),
                                        )
                                        st.rerun()
                                else:
                                    if st.button("➕ Suivre", key=f"follow_{user['id_user']}"):
                                        requests.post(
                                            f"{API_URL}/users/{user['id_user']}/follow",
                                            auth=get_auth(),
                                        )
                                        st.rerun()

                            st.divider()
                else:
                    st.error("Erreur lors de la récupération des utilisateurs")

            except Exception as e:
                st.error(f"Erreur: {str(e)}")

        with tab2:
            st.subheader("Utilisateurs que vous suivez")
            try:
                response = requests.get(
                    f"{API_URL}/users/{st.session_state.user_info['id']}/following", auth=get_auth()
                )

                if response.status_code == 200:
                    following = response.json()

                    if not following:
                        st.info("Vous ne suivez personne pour le moment")
                    else:
                        for user in following:
                            st.write(f"**{user['nom_user']}** - {user['mail_user']}")

            except Exception as e:
                st.error(f"Erreur: {str(e)}")

        with tab3:
            st.subheader("Vos abonnés")
            try:
                response = requests.get(
                    f"{API_URL}/users/{st.session_state.user_info['id']}/followers", auth=get_auth()
                )

                if response.status_code == 200:
                    followers = response.json()

                    if not followers:
                        st.info("Personne ne vous suit pour le moment")
                    else:
                        for user in followers:
                            st.write(f"**{user['nom_user']}** - {user['mail_user']}")

            except Exception as e:
                st.error(f"Erreur: {str(e)}")

    # ============================================================================
    # STATISTIQUES (F4)
    # ============================================================================
    elif menu == "📈 Statistiques":
        st.title("📈 Statistiques détaillées")

        tab1, tab2, tab3 = st.tabs(["Moyennes hebdomadaires", "Mensuel", "Annuel"])

        with tab1:
            st.subheader("Moyennes sur les dernières semaines")

            nb_semaines = st.slider("Nombre de semaines", min_value=1, max_value=12, value=4)

            try:
                response = requests.get(
                    f"{API_URL}/stats/weekly-average",
                    params={"nb_semaines": nb_semaines},
                    auth=get_auth(),
                )

                if response.status_code == 200:
                    stats = response.json()

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(
                            "Activités / semaine", f"{stats.get('activites_par_semaine', 0):.1f}"
                        )

                    with col2:
                        st.metric(
                            "Distance / semaine", f"{stats.get('distance_par_semaine', 0):.1f} km"
                        )

                    with col3:
                        st.metric("Heures / semaine", f"{stats.get('duree_par_semaine', 0):.1f} h")

                    # Détails par sport
                    if stats.get("par_sport"):
                        st.subheader("Moyennes par sport")

                        for sport, sport_stats in stats["par_sport"].items():
                            with st.expander(f"{sport.capitalize()}"):
                                col1, col2, col3 = st.columns(3)

                                with col1:
                                    st.write(
                                        f"**Activités / semaine:** {sport_stats.get('activites_par_semaine', 0):.1f}"
                                    )

                                with col2:
                                    st.write(
                                        f"**Distance / semaine:** {sport_stats.get('distance_par_semaine', 0):.1f} km"
                                    )

                                with col3:
                                    st.write(
                                        f"**Durée / semaine:** {sport_stats.get('duree_par_semaine', 0):.1f} h"
                                    )
                else:
                    st.info("Pas assez de données pour calculer les moyennes")

            except Exception as e:
                st.error(f"Erreur: {str(e)}")

        with tab2:
            st.subheader("Statistiques mensuelles")

            col1, col2 = st.columns(2)
            with col1:
                year = st.number_input(
                    "Année", min_value=2020, max_value=2030, value=datetime.now().year
                )
            with col2:
                month = st.selectbox("Mois", list(range(1, 13)), index=datetime.now().month - 1)

            try:
                response = requests.get(
                    f"{API_URL}/stats/monthly",
                    params={"year": year, "month": month},
                    auth=get_auth(),
                )

                if response.status_code == 200:
                    stats = response.json()

                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.metric("Activités", stats.get("total_activites", 0))

                    with col2:
                        st.metric("Distance", f"{stats.get('distance_totale', 0):.1f} km")

                    with col3:
                        st.metric("Durée", f"{stats.get('duree_totale', 0):.1f} h")

                    with col4:
                        st.metric("Sport favori", stats.get("sport_favori", "Aucun").capitalize())

                    # Graphiques
                    if stats.get("par_sport"):
                        st.divider()

                        sports_data = []
                        for sport, data in stats["par_sport"].items():
                            sports_data.append(
                                {
                                    "Sport": sport.capitalize(),
                                    "Activités": data.get("count", 0),
                                    "Distance (km)": data.get("distance", 0),
                                }
                            )

                        df = pd.DataFrame(sports_data)
                        df = df.sort_values("Distance (km)", ascending=False)

                        col1, col2 = st.columns(2)
                        with col1:
                            fig_activites_mensuel = px.pie(
                                df,
                                names="Sport",
                                values="Activités",
                                title="Nombre d'activités par sport",
                                color="Sport",
                                color_discrete_map=color_map
                            )
                            st.plotly_chart(
                                fig_activites_mensuel, width="stretch", key="fig_ctivites_mensuel"
                            )

                        with col2:
                            fig_distance_mensuel = px.bar(
                                df,
                                y="Distance (km)",
                                x="Sport",
                                title="Répartition des distances par sport",
                                color="Sport",
                                color_discrete_map=color_map
                            )
                            st.plotly_chart(
                                fig_distance_mensuel, width="stretch", key="fig_distance_mensuel"
                            )
                else:
                    st.info("Aucune donnée pour cette période")

            except Exception as e:
                st.error(f"Erreur: {str(e)}")

        with tab3:
            st.subheader("Statistiques annuelles")

            year = st.number_input(
                "Année",
                min_value=2020,
                max_value=2030,
                value=datetime.now().year,
                key="year_annual",
            )

            try:
                response = requests.get(
                    f"{API_URL}/stats/annual", params={"year": year}, auth=get_auth()
                )

                if response.status_code == 200:
                    stats = response.json()

                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.metric("Activités", stats.get("total_activites", 0))

                    with col2:
                        st.metric("Distance", f"{stats.get('distance_totale', 0):.1f} km")

                    with col3:
                        st.metric("Durée", f"{stats.get('duree_totale', 0):.1f} h")

                    with col4:
                        st.metric("Sport favori", stats.get("sport_favori", "Aucun").capitalize())

                    # Graphiques
                    if stats.get("par_sport"):
                        st.divider()

                        sports_data = []
                        for sport, data in stats["par_sport"].items():
                            sports_data.append(
                                {
                                    "Sport": sport.capitalize(),
                                    "Activités": data.get("count", 0),
                                    "Distance (km)": data.get("distance", 0),
                                    "Durée (h)": data.get("duree", 0),
                                }
                            )

                        df = pd.DataFrame(sports_data)
                        df = df.sort_values("Distance (km)", ascending=False)

                        col1, col2 = st.columns(2)
                        with col1:
                            fig_activites_annuel = px.pie(
                                df,
                                names="Sport",
                                values="Activités",
                                title="Nombre d'activités par sport",
                                color="Sport",
                                color_discrete_map=color_map
                            )
                            st.plotly_chart(
                                fig_activites_annuel, width="stretch", key="fig_activites_annuel"
                            )

                        with col2:
                            fig_distance_annuel = px.bar(
                                df,
                                y="Distance (km)",
                                x="Sport",
                                title="Répartition des distances par sport",
                                color="Sport",
                                color_discrete_map=color_map
                            )
                            st.plotly_chart(
                                fig_distance_annuel, width="stretch", key="fig_distance_annuel"
                            )
                else:
                    st.info("Aucune donnée pour cette année")

            except Exception as e:
                st.error(f"Erreur: {str(e)}")
