à utiliser avec **https://hackmd.io/**

# :clipboard:  Présentation du sujet

* **Sujet** : Création application de sport
* **Tuteur** : Samuel GOUTIN
* [Dépôt GitHub](https://github.com/TeodoraHub/Info-2A-Strava)

# :dart: Échéances

---
Dossier d'Analyse :  :clock1: <iframe src="https://free.timeanddate.com/countdown/i83zdl7u/n1264/cf11/cm0/cu2/ct4/cs0/ca0/co0/cr0/ss0/cac009/cpcf00/pcfff/tcfff/fs100/szw256/szh108/iso2025-11-22T20:00:00" allowtransparency="true" frameborder="0" width="130" height="16"></iframe>

---

```mermaid
gantt
    %% doc : https://mermaid-js.github.io/mermaid/#/./gantt
    dateFormat  YYYY-MM-DD
    axisFormat  %d %b
    title       Diagramme de Gantt
    %%excludes  YYYY-MM-DD and/or sunday and/or weekends 
     
    section Suivi
    TP1 et Suivi 1               :milestone, 2025-08-29,
    TP2 et Suivi 2               :milestone, 2025-09-05,
    TP3 et Suivi 3               :milestone, 2025-09-12,
    TP4                          :milestone, 2025-09-19,
    Suivi 4                      :milestone, 2025-10-03,
    3j immersion                 :active,    2025-11-04, 3d
    Suivi 7                      :milestone, 2025-11-14,
    
    section Rendu
    Dossier Analyse              :milestone, 2025-09-27,
    Rapport + Code               :milestone, 2025-11-22,
    Soutenance                   :milestone, 2025-12-10,
    
    section Vacances
    Toussaint                    :crit,    2025-10-25, 2025-11-02
    
    section Analyse
    analyse sujet                :done,    2025-08-29, 15d
    modélisation                 :active,  2025-09-05, 12d
    
    section Rédaction
    rédaction dossier analyse    :active,  2025-09-12, 2025-09-27
    relecture                    :active,  dossier,    2025-09-24, 3d
    rédaction rapport            :active,  2025-10-30, 2025-11-22
    relecture                    :active,  rapport,    2025-11-19, 3d
    
    section Code
    lister classes à coder       :active,    2025-09-05, 10d
    coder une v0                 :active,    2025-09-12, 15d
    coder VF                     :active,    2025-10-13, 2025-11-18

```

# :calendar: Livrables

| Date     | Livrables                                                    |
| -------- | ------------------------------------------------------------ |
| 27 sept. | [Dossier d'Analyse](https://www.overleaf.com/)               |
| 22 nov.  | Rapport final + code (:hammer_and_wrench:  [correcteur orthographe et grammaire](https://www.scribens.fr/))|
| 10 déc.  | Soutenance                                                   |

# :construction: Todo List

## Dossier Analyse

* [ ] Diagramme de Gantt
* [ ] Diagramme de cas d'utilisation
* [ ] Diagramme de classe
* [ ] Répartition des parties à rédiger

## Code

* [x] Créer dépôt Git commun
  * [x] vérifier que tout le monde peut **push** et **pull**
* [ ] Version 0 de l'application
  * coder une et une seule fonctionnalité simple de A à Z, et faire tourner l'appli
  * cela permettra à toute l'équipe d'avoir une bonne base de départ
* [ ] Lister classes et méthodes à coder

---

* [ ] appel WS
* [ ] création WS
* [ ] Vue inscription
* [ ] hacher mdp

---

<style>h1 {
    color: darkblue;
    font-family: "Calibri";
    font-weight: bold;
    background-color: seagreen;
    padding-left: 10px;
}

h2 {
    color: darkblue;
    background-color: darkseagreen;
    margin-right: 10%;
    padding-left: 10px;
}

h3 {
    color: darkblue;
    background-color: lightseagreen;
    margin-right: 20%;
    padding-left: 10px;
}

h4 {
    color: darkblue;
    background-color: aquamarine;
    margin-right: 30%;
    padding-left: 10px;
}

</style>
