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
        +suivre_user(user: User) void
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
        -user: id_user
        +modifier() void
        +supprimer() void
        +ajouter_like(user: id_user) void
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
        -user: id_user
        -activite: id
    }

    class Like{
        -id_activite: int
        -user: id_user
        -activite: id
        -date_like: Date
    }

    class FilActualite{
        -activites: List~Activite~
        +obtenir_activites_users_suivis(user: User) List~Activite~
        +appliquer_filtres(filtres: Map~string, Object~) List~Activite~
    }

    class Suivi{
        -suiveur: id_user
        -suivi: id_user
        -date_suivi: Date
    }

    class Statistiques{
        -user: id_user
        -nombre_activites_semaine: int
        -nombre_activites_sport: Map~Sport, int~
        -kilometres_semaine: float
        -heures_activite_semaine: float
        +calculer_statistiques(id_user) void
        +obtenir_statistiques_periode(dateDebut: Date, dateFin: Date) Statistiques
    }
}

%% Relations
User "1" --> "*" Activite : crée
User "1" --> "*" Comment : écrit
User "1" --> "*" Like : donne
User "1" <-- "*" Statistiques : utilise
Activite "*" --> "1" Sport : appartient à
Activite "1" <-- "*" Comment : reçoit
Activite "1" <-- "*" Like : reçoit
FilActualite "*" --> "*" Activite : contient
Suivi "*" --> "1" User : suiveur
Suivi "*" --> "1" User : suivi
```
