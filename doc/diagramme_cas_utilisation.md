' Ce code est à exécuter sur PlantUml Editor afin d'en visualiser le graphique
@startuml

' Configuration
left to right direction
skinparam packageStyle rectangle

' Acteurs
actor "Utilisateur\nNon-connecté" as UtilisateurNonConnecte
actor "Utilisateur\nConnecté" as UtilisateurConnecte

' Frontière du système
rectangle "Application Sportive" {
  
  ' Cas d'utilisation - Authentification
  usecase "Se connecter" as SeConnecter
  usecase "Créer un compte" as CreerCompte
  
  ' Cas d'utilisation - Gestion des activités
  usecase "Créer une activité" as CreerActivite
  usecase "Charger fichier GPX" as ChargerFichierGPX
  usecase "Consulter ses activités" as ConsulterActivites
  usecase "Modifier une activité" as ModifierActivite
  usecase "Supprimer une activité" as SupprimerActivite
  usecase "Consulter les activités\npubliques" as ConsulterActivitesPubliques
  
  ' Cas d'utilisation - Fonctionnalités sociales
  usecase "Suivre un utilisateur" as SuivreUtilisateur
  usecase "Arrêter de suivre" as ArreterSuivre
  usecase "Liker une activité" as LikerActivite
  usecase "Commenter une activité" as CommenterActivite
  usecase "Consulter fil d'actualité" as ConsulterFilActualite
  usecase "Appliquer des filtres" as AppliquerFiltres
  
  ' Cas d'utilisation - Statistiques et visualisation
  usecase "Consulter ses statistiques" as ConsulterStatistiques
  usecase "Visualiser le tracé\nsur carte" as VisualiserTrace
  usecase "Visualiser statistiques\ngraphiques" as VisualiserStatistiques
  
  ' Cas d'utilisation - Fonctionnalités avancées
  usecase "Créer un parcours" as CreerParcours
  usecase "Télécharger trace GPS" as TelechargerTraceGPS
  usecase "Accéder aux prédictions\nde distance" as PredictionsDistance
  

' Relations Utilisateur Non-connecté
UtilisateurNonConnecte --> SeConnecter
UtilisateurNonConnecte --> CreerCompte
UtilisateurNonConnecte --> ConsulterActivitesPubliques

' Relations Utilisateur Connecté - Gestion activités
UtilisateurConnecte --> CreerActivite
UtilisateurConnecte --> ConsulterActivites
UtilisateurConnecte --> ModifierActivite
UtilisateurConnecte --> SupprimerActivite

' Relations Utilisateur Connecté - Social
UtilisateurConnecte --> SuivreUtilisateur
UtilisateurConnecte --> ArreterSuivre
UtilisateurConnecte --> LikerActivite
UtilisateurConnecte --> CommenterActivite
UtilisateurConnecte --> ConsulterFilActualite

' Relations Utilisateur Connecté - Statistiques
UtilisateurConnecte --> ConsulterStatistiques
UtilisateurConnecte --> VisualiserTrace

' Relations Utilisateur Connecté - Fonctionnalités avancées
UtilisateurConnecte --> CreerParcours
UtilisateurConnecte --> TelechargerTraceGPS
UtilisateurConnecte --> PredictionsDistance


' Relations d'inclusion (include)
CreerActivite ..> ChargerFichierGPX : <<include>>
ConsulterFilActualite ..> AppliquerFiltres : <<include>>
CreerParcours ..> TelechargerTraceGPS : <<include>>

' Relations d'extension (extend)
VisualiserStatistiques ..> ConsulterStatistiques : <<extend>>
VisualiserTrace ..> ConsulterActivites : <<extend>>

' Héritage d'acteur (généralisation)
UtilisateurConnecte --|> UtilisateurNonConnecte

@enduml

