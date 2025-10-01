
CREATE TABLE Utilisateur (
    id_user INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_user TEXT NOT NULL,
    email_user TEXT NOT NULL UNIQUE,
    mot_de_passe TEXT NOT NULL
);

CREATE TABLE Activite (
    id_activite INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    description TEXT,
    date_activite DATE NOT NULL,
    duree INTEGER,
    distance REAL,
    fichier_gpx TEXT,
    sport TEXT,
    detail_sport TEXT,
    id_user INTEGER NOT NULL,
    FOREIGN KEY (id_user) REFERENCES User(id_user),
);


CREATE TABLE Commentaire (
    id_comment INTEGER PRIMARY KEY AUTOINCREMENT,
    contenu TEXT NOT NULL,
    date_comment DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_user INTEGER NOT NULL,
    id_activite INTEGER NOT NULL,
    FOREIGN KEY (id_user) REFERENCES User(id_user),
    FOREIGN KEY (id_activite) REFERENCES Activite(id_activite)
);


CREATE TABLE Like (
    id_like INTEGER PRIMARY KEY AUTOINCREMENT,
    date_like DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_user INTEGER NOT NULL,
    id_activite INTEGER NOT NULL,
    FOREIGN KEY (id_user) REFERENCES User(id_user),
    FOREIGN KEY (id_activite) REFERENCES Activite(id_activite)
);


CREATE TABLE Suivi (
    id_suiveur INTEGER NOT NULL,
    id_suivi INTEGER NOT NULL,
    date_suivi DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_suiveur, id_suivi),
    FOREIGN KEY (id_suiveur) REFERENCES User(id_user),
    FOREIGN KEY (id_suivi) REFERENCES User(id_user)
);
