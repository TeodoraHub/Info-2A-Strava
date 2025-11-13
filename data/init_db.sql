-----------------------------------------------------
-- Utilisateur
-----------------------------------------------------
DROP TABLE IF EXISTS utilisateur CASCADE;
CREATE TABLE utilisateur (
    id_user     SERIAL PRIMARY KEY,
    nom_user    VARCHAR(256) NOT NULL UNIQUE,
    mail_user   VARCHAR(256) NOT NULL UNIQUE,
    mdp         VARCHAR(256) NOT NULL
);


-----------------------------------------------------
-- Activité
-----------------------------------------------------
DROP TABLE IF EXISTS activite CASCADE;
CREATE TABLE activite (
    id_activite     SERIAL PRIMARY KEY,
    titre           VARCHAR(256) NOT NULL,
    description     TEXT,
    date_activite   TIMESTAMP NOT NULL,
    lieu            VARCHAR(256),
    duree           FLOAT,
    distance        FLOAT NOT NULL,
    sport           VARCHAR(50) NOT NULL,
    detail_sport    VARCHAR(256),
    id_user         INTEGER NOT NULL,
    FOREIGN KEY (id_user) REFERENCES utilisateur(id_user) ON DELETE CASCADE
);


-----------------------------------------------------
-- Commentaire
-----------------------------------------------------
DROP TABLE IF EXISTS commentaire CASCADE;
CREATE TABLE commentaire (
    id_comment      SERIAL PRIMARY KEY,
    contenu         TEXT NOT NULL,
    date_comment    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_user         INTEGER NOT NULL,
    id_activite     INTEGER NOT NULL,
    FOREIGN KEY (id_user) REFERENCES utilisateur(id_user) ON DELETE CASCADE,
    FOREIGN KEY (id_activite) REFERENCES activite(id_activite) ON DELETE CASCADE
);


-----------------------------------------------------
-- Like
-----------------------------------------------------
DROP TABLE IF EXISTS liker CASCADE;
CREATE TABLE liker (
    id_like         SERIAL PRIMARY KEY,
    date_like       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_user         INTEGER NOT NULL,
    id_activite     INTEGER NOT NULL,
    FOREIGN KEY (id_user) REFERENCES utilisateur(id_user) ON DELETE CASCADE,
    FOREIGN KEY (id_activite) REFERENCES activite(id_activite) ON DELETE CASCADE,
    UNIQUE (id_user, id_activite)
);


-----------------------------------------------------
-- Suivi
-----------------------------------------------------
DROP TABLE IF EXISTS suivi CASCADE;
CREATE TABLE suivi (
    id_suiveur      INTEGER NOT NULL,
    id_suivi        INTEGER NOT NULL,
    date_suivi      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_suiveur, id_suivi),
    FOREIGN KEY (id_suiveur) REFERENCES utilisateur(id_user) ON DELETE CASCADE,
    FOREIGN KEY (id_suivi) REFERENCES utilisateur(id_user) ON DELETE CASCADE,
    CHECK (id_suiveur != id_suivi)
);


-----------------------------------------------------
-- Index pour améliorer les performances
-----------------------------------------------------
CREATE INDEX idx_activite_user ON activite(id_user);
CREATE INDEX idx_activite_date ON activite(date_activite DESC);
CREATE INDEX idx_activite_sport ON activite(sport);
CREATE INDEX idx_commentaire_activite ON commentaire(id_activite);
CREATE INDEX idx_liker_activite ON liker(id_activite);
CREATE INDEX idx_suivi_suiveur ON suivi(id_suiveur);
CREATE INDEX idx_suivi_suivi ON suivi(id_suivi);
