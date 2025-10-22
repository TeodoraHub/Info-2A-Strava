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
(2, 'Course à pied du soir', 'Entraînement fractionné', '2025-02-05', 'Quais de Seine', '00:40:00', 9.2, 'Course à pied', 'Fractionné 30/30', 1),
(3, 'Natation piscine', 'Entraînement crawl', '2025-01-22', 'Piscine municipale', '00:50:00', 2.0, 'Natation', 'Crawl', 3),
(4, 'Natation endurance', 'Longue séance en piscine', '2025-02-07', 'Piscine Georges Vallerey', '01:10:00', 3.0, 'Natation', 'Endurance crawl/dos', 3),
(5, 'Sortie cyclisme', 'Balade avec dénivelé', '2025-02-09', 'Bois de Vincennes', '02:20:00', 55.0, 'Cyclisme', 'Route - endurance', 2),
(6, 'Randonnée montagne', 'Randonnée en forêt de Fontainebleau', '2025-02-15', 'Fontainebleau', '04:00:00', 12.5, 'Randonnée', 'Marche en groupe', 4);;


-----------------------------------------------------
-- Commentaire
-----------------------------------------------------
INSERT INTO commentaire (id_comment, contenu, id_user, id) VALUES
(1, 'Bravo pour ton footing !', 2, 1),
(2, 'Super rythme sur ta course, bravo !', 2, 4),
(3, 'Bonne nage, tu progresses !', 4, 3),
(4, 'Belle séance, ça donne envie !', 1, 4),
(5, '55 km, impressionnant !', 4, 5),
(6, 'Fontainebleau c’est magnifique, j’aimerais venir la prochaine fois.', 3, 6);
-----------------------------------------------------
-- Like
-----------------------------------------------------
INSERT INTO liker (id_like, id_user, id) VALUES
(1, 2, 1),  -- Bob like footing d'Alice
(2, 3, 2),  -- Claire like la course d'Alice
(3, 2, 3),  -- Bob like la natation de Claire
(4, 1, 4),  -- Alice like la sortie vélo de Bob
(5, 2, 5);  -- Bob like la randonnée de David
-----------------------------------------------------
-- Suivi
-----------------------------------------------------
INSERT INTO suivi (id_suiveur, id_suivi) VALUES
(1, 2),  -- Alice suit Bob
(2, 3),  -- Bob suit Claire
(3, 1),  -- Claire suit Alice
(4, 1),  -- David suit Alice
(1, 3),  -- Alice suit Claire
(2, 1),  -- Bob suit Alice
(3, 4),  -- Claire suit David
(4, 2);  -- David suit Bob