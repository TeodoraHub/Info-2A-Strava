```mermaid
---
title: MODELE PHYSIQUE DE DONNEES - APPLICATION SPORTIVE
---
erDiagram
    Utilisateur {
        int id_user PK
        string nom_user
        string email_user UK
        string mot_de_passe
    }

    Sport {
        int id_sport PK
        string nom_sport UK
    }

    Activite {
        int id PK
        string titre
        string description
        date date_activite
        int duree
        float distance
        string fichier_gpx
        int id_user FK
        int id_sport FK
    }

    Commentaire {
        int id PK
        string contenu
        datetime date_commentaire
        int id_user FK
        int id_activite FK
    }

    Like {
        int id PK
        datetime date_like
        int id_user FK
        int id_activite FK
        -- contrainte : UNIQUE(id_user, id_activite)
    }

    Suivi {
        int id_suiveur FK
        int id_suivi FK
        datetime date_suivi
        PK { id_suiveur, id_suivi }
    }

    Statistiques {
        int id_user PK, FK
        int nombre_activites_semaine
        float kilometres_semaine
        float heures_activite_semaine
    }

    %% Relations
    Utilisateur ||--o{ Activite : "crée"
    Utilisateur ||--o{ Commentaire : "écrit"
    Utilisateur ||--o{ Like : "donne"
    Utilisateur ||--o{ Suivi : "suit"
    Utilisateur ||--o{ Statistiques : "utilise"

    Activite }o--|| Sport : "appartient à"
    Activite ||--o{ Commentaire : "reçoit"
    Activite ||--o{ Like : "reçoit"

    Suivi }o--|| Utilisateur : "suiveur"
    Suivi }o--|| Utilisateur : "suivi"
mermaid'''
