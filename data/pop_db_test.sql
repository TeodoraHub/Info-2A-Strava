INSERT INTO utilisateur (nom_user, mail_user, mdp) VALUES
('alice', 'alice@example.com', '1bf52fdbcef590cedf5cd8f250ea6c32f41d9e8901b396cdfa35076a6f054b47'),
('bob', 'bob@example.com', '0e4ab4bf1898f84e75990143a01b3919d42b81ffa0e82921f16eb4c984f871c5');

INSERT INTO activite (titre, description, date_activite, lieu, duree, distance, sport, id_user) VALUES
('Footing de test', 'Course de test pour verification DAO', '2025-01-01 08:00:00', 'Parc A', 0.5, 5.0, 'course', 1),
('Cyclisme de test', 'Vélo de test pour verification DAO', '2025-01-02 10:00:00', 'Route B', 1.5, 30.0, 'cyclisme', 2);

INSERT INTO suivi (id_suiveur, id_suivi) VALUES
(1, 2),
(2, 1);

INSERT INTO commentaire (contenu, id_user, id_activite) VALUES
('Super test !', 2, 1);

INSERT INTO liker (id_user, id_activite) VALUES
(2, 1),
(1, 2);