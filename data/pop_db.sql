-----------------------------------------------------
-- Utilisateurs
-- Note: Les mots de passe seront hashés par l'application lors de la création via l'API
-- Pour tester, utilisez ces credentials après avoir créé les utilisateurs via l'API
-----------------------------------------------------
-- Ces utilisateurs doivent être créés via l'API pour que les mots de passe soient correctement hashés
-- Exemples de création via l'API:
-- POST /users?nom_user=alice&mail_user=alice@example.com&mdp=password123
-- POST /users?nom_user=bob&mail_user=bob@example.com&mdp=password123
-- POST /users?nom_user=claire&mail_user=claire@example.com&mdp=password123
-- POST /users?nom_user=david&mail_user=david@example.com&mdp=password123
-- POST /users?nom_user=emma&mail_user=emma@example.com&mdp=password123

-- Pour les tests directs en base (sans passer par l'API), hashes de 'password123':
INSERT INTO utilisateur (nom_user, mail_user, mdp) VALUES
('alice', 'alice@example.com', '1bf52fdbcef590cedf5cd8f250ea6c32f41d9e8901b396cdfa35076a6f054b47'),
('bob', 'bob@example.com', '0e4ab4bf1898f84e75990143a01b3919d42b81ffa0e82921f16eb4c984f871c5'),
('claire', 'claire@example.com', '495038a7ca6a49e2028fee5c49bdd4e8119e59f083b25125dd22233ea25b6161'),
('david', 'david@example.com', '512019875b8784e5f428f6ea666f06d4ee6225dcfa255fec6a49a9ca361a16e5'),
('emma', 'emma@example.com', 'f61f78d30111910aed172503eef6f962b2b3a534a8d26595de9cbc0b138aba12');



-----------------------------------------------------
-- Activités
-----------------------------------------------------
INSERT INTO activite (titre, description, date_activite, lieu, duree, distance, sport, id_user) VALUES
-- Activités d'Alice (id_user=1)
('Footing matinal', 'Course dans le parc au lever du soleil', '2025-01-15 07:00:00', 'Parc Montsouris', 0.75, 8.5, 'course', 1),
('Course du soir', 'Entraînement fractionné intense', '2025-01-20 19:30:00', 'Quais de Seine', 0.67, 9.2, 'course', 1),
('Sortie vélo week-end', 'Balade vélo avec les amis', '2025-01-25 10:00:00', 'Bois de Vincennes', 2.5, 45.0, 'cyclisme', 1),
('Course longue', 'Préparation semi-marathon', '2025-02-05 08:00:00', 'Bois de Boulogne', 1.5, 15.0, 'course', 1),

-- Activités de Bob (id_user=2)
('Natation technique', 'Travail technique crawl', '2025-01-18 12:00:00', 'Piscine municipale', 1.0, 2.0, 'natation', 2),
('Sortie cyclisme longue', 'Grande sortie avec dénivelé', '2025-02-09 09:00:00', 'Vallée de Chevreuse', 3.0, 65.0, 'cyclisme', 2),
('Natation endurance', 'Séance longue distance', '2025-02-12 18:00:00', 'Piscine Georges Vallerey', 1.25, 3.0, 'natation', 2),
('Course récupération', 'Footing léger de récupération', '2025-02-15 19:00:00', 'Parc Monceau', 0.5, 6.0, 'course', 2),

-- Activités de Claire (id_user=3)
('Randonnée forêt', 'Randonnée familiale en forêt', '2025-01-22 10:00:00', 'Forêt de Fontainebleau', 3.5, 12.0, 'randonnee', 3),
('Natation piscine', 'Entraînement natation', '2025-01-28 17:30:00', 'Piscine Keller', 0.83, 2.5, 'natation', 3),
('Randonnée montagne', 'Montée au sommet', '2025-02-08 08:00:00', 'Les Vosges', 5.0, 18.0, 'randonnee', 3),
('Course urbaine', 'Découverte de Paris en courant', '2025-02-14 07:30:00', 'Centre de Paris', 0.9, 10.0, 'course', 3),

-- Activités de David (id_user=4)
('Vélo route', 'Entraînement route vallonné', '2025-01-19 14:00:00', 'Vallée de Chevreuse', 2.0, 50.0, 'cyclisme', 4),
('Randonnée groupe', 'Sortie avec le club de randonnée', '2025-02-02 09:00:00', 'Fontainebleau', 4.0, 15.0, 'randonnee', 4),
('Course trail', 'Trail en forêt', '2025-02-10 08:30:00', 'Forêt de Rambouillet', 1.75, 12.0, 'course', 4),
('Natation libre', 'Nage libre tranquille', '2025-02-16 12:30:00', 'Piscine Pontoise', 0.67, 1.5, 'natation', 4),

-- Activités d'Emma (id_user=5)
('Course débutant', 'Ma première vraie course', '2025-01-21 18:00:00', 'Parc des Buttes Chaumont', 0.5, 5.0, 'course', 5),
('Randonnée découverte', 'Découverte de la randonnée', '2025-01-29 11:00:00', 'Forêt de Saint-Germain', 2.5, 8.0, 'randonnee', 5),
('Vélo débutant', 'Sortie vélo tranquille', '2025-02-06 15:00:00', 'Canal de l''Ourcq', 1.5, 20.0, 'cyclisme', 5),
('Natation apprentissage', 'Cours de natation', '2025-02-13 16:00:00', 'Piscine Jean Taris', 0.75, 1.0, 'natation', 5);


-----------------------------------------------------
-- Commentaires
-----------------------------------------------------
INSERT INTO commentaire (contenu, id_user, id_activite) VALUES
-- Commentaires sur les activités d'Alice
('Bravo pour ton footing ! Belle régularité 👏', 2, 1),
('Super rythme, tu t''améliores vraiment !', 3, 2),
('45 km à vélo, impressionnant ! J''aimerais te suivre.', 4, 3),
('Bon courage pour le semi-marathon !', 5, 4),

-- Commentaires sur les activités de Bob
('Belle technique sur cette nage !', 1, 5),
('65 km avec du dénivelé, respect ! 🚴', 3, 6),
('3 km de nage, tu es un vrai poisson 🐟', 4, 7),

-- Commentaires sur les activités de Claire
('Fontainebleau est magnifique, j''adore cet endroit !', 1, 9),
('Les Vosges doivent être superbes en cette saison', 2, 11),
('10 km dans Paris, tu dois connaître plein de coins sympa !', 5, 12),

-- Commentaires sur les activités de David
('50 km en vallée de Chevreuse, ça donne envie !', 2, 13),
('Le trail en forêt doit être magnifique', 1, 15),

-- Commentaires sur les activités d'Emma
('Félicitations pour ta première course ! Continue comme ça 💪', 1, 17),
('Bienvenue dans le monde de la randonnée !', 3, 18),
('Le canal de l''Ourcq est parfait pour débuter le vélo', 2, 19),
('Bon courage pour l''apprentissage de la natation !', 4, 20);


-----------------------------------------------------
-- Likes
-----------------------------------------------------
INSERT INTO liker (id_user, id_activite) VALUES
-- Likes sur les activités d'Alice (id 1-4)
(2, 1), (3, 1), (4, 1),  -- 3 likes sur le footing matinal
(2, 2), (5, 2),           -- 2 likes sur course du soir
(3, 3), (4, 3),           -- 2 likes sur sortie vélo
(2, 4), (3, 4), (5, 4),   -- 3 likes sur course longue

-- Likes sur les activités de Bob (id 5-8)
(1, 5), (3, 5),           -- 2 likes natation technique
(1, 6), (4, 6), (5, 6),   -- 3 likes sortie cyclisme longue
(1, 7), (3, 7),           -- 2 likes natation endurance
(1, 8),                   -- 1 like course récupération

-- Likes sur les activités de Claire (id 9-12)
(1, 9), (2, 9), (4, 9),   -- 3 likes randonnée forêt
(2, 10),                  -- 1 like natation piscine
(1, 11), (2, 11),         -- 2 likes randonnée montagne
(5, 12),                  -- 1 like course urbaine

-- Likes sur les activités de David (id 13-16)
(2, 13), (3, 13),         -- 2 likes vélo route
(1, 14), (3, 14),         -- 2 likes randonnée groupe
(1, 15), (2, 15),         -- 2 likes course trail
(2, 16),                  -- 1 like natation libre

-- Likes sur les activités d'Emma (id 17-20)
(1, 17), (2, 17), (3, 17), (4, 17),  -- 4 likes course débutant (encouragements)
(1, 18), (3, 18),                     -- 2 likes randonnée découverte
(2, 19), (4, 19),                     -- 2 likes vélo débutant
(1, 20), (4, 20);                     -- 2 likes natation apprentissage


-----------------------------------------------------
-- Relations de suivi
-----------------------------------------------------
INSERT INTO suivi (id_suiveur, id_suivi) VALUES
-- Alice (1) suit Bob, Claire et David
(1, 2), (1, 3), (1, 4),

-- Bob (2) suit Alice, Claire, David et Emma
(2, 1), (2, 3), (2, 4), (2, 5),

-- Claire (3) suit Alice, Bob et Emma
(3, 1), (3, 2), (3, 5),

-- David (4) suit Alice, Bob et Claire
(4, 1), (4, 2), (4, 3),

-- Emma (5) suit tout le monde (débutante qui suit les autres pour apprendre)
(5, 1), (5, 2), (5, 3), (5, 4);


-----------------------------------------------------
-- Vérification des données insérées
-----------------------------------------------------
-- Vous pouvez décommenter ces requêtes pour vérifier les données
-- SELECT COUNT(*) as nb_utilisateurs FROM utilisateur;
-- SELECT COUNT(*) as nb_activites FROM activite;
-- SELECT COUNT(*) as nb_commentaires FROM commentaire;
-- SELECT COUNT(*) as nb_likes FROM liker;
-- SELECT COUNT(*) as nb_suivis FROM suivi;
