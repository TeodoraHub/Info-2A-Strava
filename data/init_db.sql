-----------------------------------------------------
-- Utilisateur
-----------------------------------------------------
DROP TABLE IF EXISTS utilisateur CASCADE ;
CREATE TABLE utilisateur (
    id_user     INTEGER PRIMARY KEY,
    nom_user    VARCHAR(256) NOT NULL,
    mail_user   VARCHAR(50) NOT NULL UNIQUE,
    mdp         VARCHAR(256) NOT NULL
);


-----------------------------------------------------
-- Activité
-----------------------------------------------------
DROP TABLE IF EXISTS activite CASCADE ;
CREATE TABLE activite (
    id          INTEGER PRIMARY KEY,
    titre       VARCHAR(256) NOT NULL,
    description VARCHAR(256),
    date_activite DATE NOT NULL,
    lieu        VARCHAR(256),
    duree       TIME,
    distance    FLOAT,
    fichier_gpx TEXT,
    sport       VARCHAR(256),
    detail_sport VARCHAR(256),
    id_user     INTEGER NOT NULL,
    FOREIGN KEY (id_user) REFERENCES utilisateur(id_user),
);


-----------------------------------------------------
-- Commentaire
-----------------------------------------------------
DROP TABLE IF EXISTS commentaire CASCADE ;
CREATE TABLE commentaire (
    id_comment  INTEGER PRIMARY KEY,
    contenu     VARCHAR(256) NOT NULL,
    date_comment DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_user     INTEGER NOT NULL,
    id          INTEGER NOT NULL,
    FOREIGN KEY (id_user) REFERENCES utilisateur(id_user),
    FOREIGN KEY (id) REFERENCES activite(id)
);


-----------------------------------------------------
-- Like
-----------------------------------------------------
DROP TABLE IF EXISTS liker CASCADE ;
CREATE TABLE liker (
    id_like     INTEGER PRIMARY KEY,
    date_like   DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_user     INTEGER NOT NULL,
    id          INTEGER NOT NULL,
    FOREIGN KEY (id_user) REFERENCES utilisateur(id_user),
    FOREIGN KEY (id) REFERENCES activite(id)
);


-----------------------------------------------------
-- Suivi
-----------------------------------------------------
DROP TABLE IF EXISTS suivi CASCADE ;
CREATE TABLE suivi (
    id_suiveur  INTEGER PRIMARY KEY,
    id_suivi    INTEGER PRIMARY KEY,
    date_suivi  DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_suiveur) REFERENCES utilisateur(id_user),
    FOREIGN KEY (id_suivi) REFERENCES utilisateur(id_user)
);
