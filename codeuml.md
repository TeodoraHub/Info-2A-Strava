<!-- code à excécuter sur https://mermaid.js.org/syntax/classDiagram.html#syntax -->
<!--  pour mettre un commentaire dans un fichier .md-->
<!-- installer extension Markdown Preview Mermaid Support pour prévisualisation sur Vscode -->

```mermaid
---
title: APPLICATION SPORTIVE
---
classDiagram
namespace Main {
    class Utilisateur{
        -id_user: int
        -nom_user: string
        -email_user: string
        -motDePasse: string
        +creerActivite(fichierGpx: File) Activite
        +consulterActivites() List~Activite~
        +modifierActivite(activite: Activite) void
        +supprimerActivite(activite: Activite) void
        +suivreUtilisateur(utilisateur: Utilisateur) void
        +likerActivite(activite: Activite) void
        +commenterActivite(activite: Activite, commentaire: string) void
        +obtenirStatistiques() Statistiques
    }

    class Activite {
        -id: int
        -titre: string
        -description: string
        -dateActivite: Date
        -duree: int
        -distance: float
        -sport: Sport
        -fichierGpx: string
        -utilisateur: Utilisateur
        +modifier() void
        +supprimer() void
        +ajouterLike(utilisateur: Utilisateur) void
        +ajouterCommentaire(commentaire: Commentaire) void
    }

    class Sport{
        <<enumeration>>
        COURSE_A_PIED
        CYCLISME
        NATATION
        RANDONNEE
    }

    class Commentaire{
        -id: int
        -contenu: string
        -dateCommentaire: Date
        -utilisateur: Utilisateur
        -activite: Activite
    }

    class Like{
        -id: int
        -utilisateur: Utilisateur
        -activite: Activite
        -dateLike: Date
    }

    class FilActualite{
        -activites: List~Activite~
        +obtenirActivitesUtilisateursSuivis(utilisateur: Utilisateur) List~Activite~
        +appliquerFiltres(filtres: Map~string, Object~) List~Activite~
    }

    class Suivi{
        -suiveur: Utilisateur
        -suivi: Utilisateur
        -dateSuivi: Date
    }

    class Statistiques{
        -utilisateur: Utilisateur
        -nombreActivitesParSemaine: int
        -nombreActivitesParSport: Map~Sport, int~
        -kilometresParSemaine: float
        -heuresActiviteParSemaine: float
        +calculerStatistiques() void
        +obtenirStatistiquesPeriode(dateDebut: Date, dateFin: Date) Statistiques
    }
}

%% Relations
Utilisateur "1" --> "*" Activite : crée
Utilisateur "1" --> "*" Commentaire : écrit
Utilisateur "1" --> "*" Like : donne
Utilisateur "1" --> "*" Suivi : suit/est suivi
Utilisateur "1" --> "1" Statistiques : possède
Activite "1" --> "1" Sport : appartient à
Activite "1" <-- "*" Commentaire : reçoit
Activite "1" <-- "*" Like : reçoit
FilActualite "*" --> "*" Activite : contient
Suivi "*" --> "1" Utilisateur : suiveur
Suivi "*" --> "1" Utilisateur : suivi
```
