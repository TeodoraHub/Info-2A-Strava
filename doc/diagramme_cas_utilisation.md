@startuml
' à coller ici pour visualiser : https://www.plantuml.com/plantuml/uml/SyfFKj2rKt3CoKnELR1Io4ZDoSa70000
' doc : https://plantuml.com/fr/use-case-diagram

  
left to right direction

actor "Utilisateur" as user

rectangle {
  usecase "S'inscrire"          as inscription
  usecase "Se connecter"        as connexion
  usecase "Quitter"             as quitter

  usecase "Consulter fil d'actualités"        as consulter_fil
  usecase "Filtrer fil d'actualités"          as filtrer_fil #lightblue
  usecase "Liker activité"       as liker
  usecase "Commenter activité"   as commenter
  usecase "Suivre utilisateur"   as suivre

  usecase "Créer activité"       as creer_activite
  usecase "Consulter profil"     as consulter_profil
  usecase "Consulter activités"  as consulter_activites
  usecase "Consulter statistiques" as consulter_statistiques
  usecase "Consulter followers"  as consulter_followers
  usecase "Modifier activité"    as modifier_activite
  usecase "Supprimer activité"   as supprimer_activite
  usecase "Visualiser le tracé"  as visualiser_trace #lightblue
  usecase "Prédire distance"     as predire_distance #lightblue

  usecase "Créer un parcours"    as creer_parcours #lightblue
  usecase "Visualiser parcours"  as visualiser_parcours #lightblue
  usecase "Télécharger la trace GPS du parcours" as telecharger_trace_parcours #lightblue
}

' Arrivée
user --> inscription
user --> connexion
user --> quitter

' Après connexion
connexion --> consulter_fil
connexion --> creer_activite
connexion --> supprimer_activite
connexion --> consulter_profil
connexion --> predire_distance
connexion --> creer_parcours

' Actions liées au fil d'activité
consulter_fil --> liker
consulter_fil --> commenter
consulter_fil --> suivre
consulter_fil --> filtrer_fil

' Actions liées au profil
consulter_profil --> consulter_activites
consulter_profil --> consulter_statistiques
consulter_profil --> consulter_followers

' Actions liées aux activités du profil
consulter_activites --> modifier_activite
consulter_activites --> visualiser_trace

' Actions liées aux parcours
creer_parcours --> visualiser_parcours
creer_parcours --> telecharger_trace_parcours

@enduml
