<!-- code à excécuter sur https://mermaid.js.org/syntax/classDiagram.html#syntax -->
<!--  pour mettre un commentaire dans un fichier .md-->
<!-- installer extension Markdown Preview Mermaid Support pour prévisualisation sur Vscode -->

```mermaid
---
title: APPLICATION SPORTIVE
---
classDiagram
namespace Main {
    class User{
        -id_user: int
        -nom_user: string
        -email_user: string
        -mot_de_passe: string
        +creer_activite(fichier_gpx: File) Activite
        +consulter_activites() List~Activite~
        +modifier_activite(activite: Activite) void
        +supprimer_activite(activite: Activite) void
        +suivre_utilisateur(utilisateur: Utilisateur) void
        +liker_activite(activite: Activite) void
        +commenter_activite(activite: Activite, commentaire: string) void
        +obtenir_statistiques() Statistiques
    }

    class Activite {
        -id_activite: int
        -titre: string
        -description: string
        -date_activite: Date
        -duree: int
        -distance: float
        -sport: Sport
        -fichier_gpx: string
        -utilisateur: id_user
        +modifier() void
        +supprimer() void
        +ajouter_like(utilisateur: id_user) void
        +ajouter_commentaire(commentaire: Commentaire) void
        +vitesse(fichierGpx) float
    }

    class Sport{
        <<enumeration>>
        COURSE_A_PIED
        CYCLISME
        NATATION
        RANDONNEE
    }

    class Comment{
        -id_activite: int
        -contenu: string
        -date_commentaire: Date
        -utilisateur: id_user
        -activite: id
    }

    class Like{
        -id_activite: int
        -utilisateur: id_user
        -activite: id
        -date_like: Date
    }

    class FilActualite{
        -activites: List~Activite~
        +obtenir_activites_utilisateurs_suivis(utilisateur: Utilisateur) List~Activite~
        +appliquer_filtres(filtres: Map~string, Object~) List~Activite~
    }

    class Suivi{
        -suiveur: id_user
        -suivi: id_user
        -date_suivi: Date
    }

    class Statistiques{
        -utilisateur: id_user
        -nombre_activites_semaine: int
        -nombre_activites_sport: Map~Sport, int~
        -kilometres_semaine: float
        -heures_activite_semaine: float
        +calculer_statistiques(id_user) void
        +obtenir_statistiques_periode(dateDebut: Date, dateFin: Date) Statistiques
    }
}

%% Relations
Utilisateur "1" --> "*" Activite : crée
Utilisateur "1" --> "*" Commentaire : écrit
Utilisateur "1" --> "*" Like : donne
Utilisateur "1" --> "*" Suivi : suit/est suivi
Utilisateur "1" <-- "*" Statistiques : utilise
Activite "*" --> "1" Sport : appartient à
Activite "1" <-- "*" Commentaire : reçoit
Activite "1" <-- "*" Like : reçoit
FilActualite "*" --> "*" Activite : contient
Suivi "*" --> "1" Utilisateur : suiveur
Suivi "*" --> "1" Utilisateur : suivi
```
