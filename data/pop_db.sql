-----------------------------------------------------
-- Utilisateur
-----------------------------------------------------
INSERT INTO utilisateur VALUES
(1, 'Alice Dupont', 'alice@example.com', 'mdpAlice123'),
(2, 'Bob Martin', 'bob@example.com', 'mdpBob123'),
(3, 'Claire Leroy', 'claire@example.com', 'mdpClaire123'),
(4, 'David Lopez', 'david@example.com', 'mdpDavid123');

-----------------------------------------------------
-- Activité
-----------------------------------------------------
INSERT INTO activite VALUES
(1, 'Footing matin', 'Course dans le parc', '2025-01-15', 'Parc Montsouris', '00:45:00', 8.5, 'Course', 'Footing léger', 1),
(2, 'Match de foot', 'Foot entre amis', '2025-01-20', 'Stade local', '01:30:00', 5.0, 'Football', 'Amical', 2),
(3, 'Natation piscine', 'Entraînement crawl', '2025-01-22', 'Piscine municipale', '00:50:00', 2.0, 'Natation', 'Crawl', 3);

-----------------------------------------------------
-- Commentaire
-----------------------------------------------------
INSERT INTO commentaire (id_comment, contenu, id_user, id) VALUES
(1, 'Bravo pour ton footing !', 2, 1),
(2, 'Super match, à refaire !', 3, 2),
(3, 'Bonne nage, tu progresses !', 4, 3);

-----------------------------------------------------
-- Like
-----------------------------------------------------
INSERT INTO liker (id_like, id_user, id) VALUES
(1, 2, 1),  -- Bob like footing d'Alice
(2, 3, 1),  -- Claire like footing d'Alice
(3, 1, 2);  -- Alice like match de Bob

-----------------------------------------------------
-- Suivi
-----------------------------------------------------
INSERT INTO suivi (id_suiveur, id_suivi) VALUES
(1, 2),  -- Alice suit Bob
(2, 3),  -- Bob suit Claire
(3, 1),  -- Claire suit Alice
(4, 1);  -- David suit Alice