<!-- code à excécuter sur https://mermaid.js.org/syntax/classDiagram.html#syntax -->
<!--  pour mettre un commentaire dans un fichier .md-->
<!-- installer extension Markdown Preview Mermaid Support pour prévisualisation sur Vscode -->

```mermaid
---
title: APPLICATION SPORTIVE
---

classDiagram
    class Utilisateur {
        +int id_user
        +string nom_user
        +string email_user
        +string mot_de_passe
        +creer_activite(fichier_gpx: File) Activite
        +consulter_activites() List~Activite~
        +modifier_activite(activite: Activite) void
        +supprimer_activite(activite: Activite) void
        +suivre_user(user: Utilisateur) void
        +liker_activite(activite: Activite) void
        +commenter_activite(activite: Activite, commentaire: string) void
        +obtenir_statistiques() Statistiques
    }

    class Suivi {
        +id_user suiveur
        +id_user suivi
        +Date date_suivi
    }

    class FilActualite {
        +List~Activite~ activites
        +obtenir_activites_users_suivis(user: Utilisateur) List~Activite~
        +appliquer_filtres(filtres: Map~String, Object~) List~Activite~
    }

    class Activite {
        +int id_activite
        +string titre
        +string description
        +Date date_activite
        +int duree
        +float distance
        +int id_user
    }

    class Statistiques {
        +calculer_statistiques(id_user : int) void
        +nombre_activites(id_user : int, periode : str, sport : str) int
        +kilometres(id_user : int, periode : str, sport : str)
        +heures_activite(id_user : int, periode : str, sport : str)
    }

    class Like {
        +int id_activite
        +int id_user
        +Date date_like
    }

    class Commentaire {
        +int id_activite
        +string contenu
        +Date date_commentaire
        +int id_user
    }

    class Cyclisme {
        +str type_velo
        +vitesse() float
    }

    class Randonnee {
        +str type_terrain
        +vitesse() float
    }

    class Natation {
        + str type_nage
        +vitesse() float
    }

    class CourseAPied {
        +vitesse() float
    }

    %% Relations
    Utilisateur "1" --> "*" Activite : crée
    Utilisateur "1" --> "*" Commentaire : écrit
    Utilisateur "1" --> "*" Like : donne
    Utilisateur "1" --> "*" Statistiques : utilise
    Activite "1" <-- "*" Commentaire : reçoit
    Activite "1" <-- "*" Like : reçoit
    FilActualite "*" --> "*" Activite : contient
    Suivi "*" --> "1" Utilisateur : suiveur
    Suivi "*" --> "1" Utilisateur : suivi
    
    %% Héritage
    Activite <|-- Cyclisme
    Activite <|-- Randonnee
    Activite <|-- Natation
    Activite <|-- CourseAPied
```
