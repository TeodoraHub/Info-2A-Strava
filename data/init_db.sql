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
    id_activite          SERIAL PRIMARY KEY,
    titre       VARCHAR(256) NOT NULL,
    description VARCHAR(256),
    date_activite DATE NOT NULL,
    lieu        VARCHAR(256),
    duree       TIME,
    distance    FLOAT,
    sport       VARCHAR(256),
    detail_sport VARCHAR(256),
    id_user     INTEGER NOT NULL,
    FOREIGN KEY (id_user) REFERENCES utilisateur(id_user)
);


-----------------------------------------------------
-- Commentaire
-----------------------------------------------------
DROP TABLE IF EXISTS commentaire CASCADE ;
CREATE TABLE commentaire (
    id_comment  INTEGER PRIMARY KEY,
    contenu     VARCHAR(256) NOT NULL,
    date_comment TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_user     INTEGER NOT NULL,
    id_activite      INTEGER NOT NULL,
    FOREIGN KEY (id_user) REFERENCES utilisateur(id_user),
    FOREIGN KEY (id_activite) REFERENCES activite(id_activite)
);


-----------------------------------------------------
-- Like
-----------------------------------------------------
DROP TABLE IF EXISTS liker CASCADE ;
CREATE TABLE liker (
    id_like     INTEGER PRIMARY KEY,
    date_like   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_user     INTEGER NOT NULL,
    id_activite         INTEGER NOT NULL,
    FOREIGN KEY (id_user) REFERENCES utilisateur(id_user),
    FOREIGN KEY (id_activite) REFERENCES activite(id_activite)
);


-----------------------------------------------------
-- Suivi
-----------------------------------------------------
DROP TABLE IF EXISTS suivi CASCADE ;
CREATE TABLE suivi (
    id_suiveur  INTEGER NOT NULL,
    id_suivi    INTEGER NOT NULL,
    date_suivi  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_suiveur, id_suivi),
    FOREIGN KEY (id_suiveur) REFERENCES utilisateur(id_user),
    FOREIGN KEY (id_suivi) REFERENCES utilisateur(id_user)
);