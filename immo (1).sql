-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : sam. 02 nov. 2024 à 20:21
-- Version du serveur : 10.4.24-MariaDB
-- Version de PHP : 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `immo`
--

-- --------------------------------------------------------

--
-- Structure de la table `bail`
--

CREATE TABLE `bail` (
  `id_bail` int(255) NOT NULL,
  `id_propriete` int(255) NOT NULL,
  `id_locataire` int(255) NOT NULL,
  `date_debut` date NOT NULL,
  `date_fin` date NOT NULL,
  `loyer_mensuel` decimal(65,0) NOT NULL,
  `depot_garantie` decimal(65,0) NOT NULL,
  `cond_special` varchar(255) NOT NULL,
  `prix_vente` decimal(65,0) NOT NULL,
  `date_vente` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `bail`
--

INSERT INTO `bail` (`id_bail`, `id_propriete`, `id_locataire`, `date_debut`, `date_fin`, `loyer_mensuel`, `depot_garantie`, `cond_special`, `prix_vente`, `date_vente`) VALUES
(1, 1, 3, '2024-09-13', '2025-09-13', '25000', '60000', 'payer avant le 05 de chaque mois', '123456789098765432', '2024-09-13'),
(2, 4, 3, '2024-09-13', '2025-09-13', '45000', '75000', 'payer avant le 02 de chaque mois', '0', '2024-09-13'),
(3, 1, 3, '2024-09-18', '2030-09-18', '35000', '75000', '', '0', '2024-09-18'),
(5, 9, 4, '2024-09-17', '2024-10-17', '450000', '250000', 'payer la moitie avant d\'entrer et respecter les regles de l\'hotel', '0', '2024-09-28');

-- --------------------------------------------------------

--
-- Structure de la table `entretien`
--

CREATE TABLE `entretien` (
  `id_entretien` int(255) NOT NULL,
  `id_propriete` int(255) NOT NULL,
  `nom_entretieneur` varchar(255) NOT NULL,
  `date_entretien` date NOT NULL,
  `type_entretien` varchar(255) NOT NULL,
  `cout` decimal(65,0) NOT NULL,
  `commentaire_entretien` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `entretien`
--

INSERT INTO `entretien` (`id_entretien`, `id_propriete`, `nom_entretieneur`, `date_entretien`, `type_entretien`, `cout`, `commentaire_entretien`) VALUES
(6, 1, 'Ba Pape Demba', '2024-09-19', 'peinture ', '25000', 'urgence pour la chambre 2'),
(8, 1, 'THIOYE Cheikh', '2024-10-01', 'reparer', '2400', 'urgence'),
(9, 7, 'THIOYE Cheikh', '2024-10-01', 'fluide d\'eau', '5500', 'urgence ');

-- --------------------------------------------------------

--
-- Structure de la table `locataire`
--

CREATE TABLE `locataire` (
  `id_locataire` int(255) NOT NULL,
  `nom` varchar(255) NOT NULL,
  `prenom` varchar(255) NOT NULL,
  `adresse` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `date_naissance` date NOT NULL,
  `telephone` varchar(255) NOT NULL,
  `profession` varchar(255) NOT NULL,
  `mot_de_passe_loc` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `locataire`
--

INSERT INTO `locataire` (`id_locataire`, `nom`, `prenom`, `adresse`, `email`, `date_naissance`, `telephone`, `profession`, `mot_de_passe_loc`) VALUES
(3, 'diouf', 'samba', 'fatick/peulgha', 'sambadiouf@gmail.com', '2002-01-02', '775394638', 'enseignant', '$2b$12$8v33XHpWQ8DzGezmaUKH8OgZ69vI3tjqG/jrUgqpK72rEQU.Hdm3a'),
(4, 'SARR', 'Oulymata Guidemelle', 'keur Mbaye Fall', 'oulymatasarr@gmail.com', '2001-01-06', '781399165', 'Electromecanicienne', '$2b$12$TiinWNtYDDCVixdiEIhFO.c69RixU14e1UQJO0/B2x03jpACHaVX6'),
(5, 'Samb', 'Mariama', 'Peulgha/Fatick', 'mariamasamb@gmail.com', '1967-09-24', '779407857', 'Enseignante', '$2b$12$.ZeAgwHn.LgEBwnMUTkUv.2uzOKQb4LMtfp1sHJAPGgQFQ0W22tiW'),
(6, 'Diallo', 'Souleymane', 'Kaolack', 'souleymane@gmail.com', '1996-11-05', '778063334', 'Agent de Police', '$2b$12$blWRw0StNphpFRa84jhJ7uXcAu/ci8Yif5dC8C/CYJ66/yMxX7feW'),
(9, 'Diallo', 'Kalidou', 'Thies', 'kalidoudiallo@gmail.com', '2024-09-30', '775678901', 'Etudiant', '$2b$12$xUxiWp.B6o/wfQck.FwNzOSJZuDFKNCwyuCrs4MUcp6O0ZgjBZwzS');

-- --------------------------------------------------------

--
-- Structure de la table `paiement`
--

CREATE TABLE `paiement` (
  `id_paiement` int(255) NOT NULL,
  `id_bail` int(255) NOT NULL,
  `date_paiement` date NOT NULL,
  `montant` decimal(65,0) NOT NULL,
  `mode` varchar(255) NOT NULL,
  `commentaire` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `paiement`
--

INSERT INTO `paiement` (`id_paiement`, `id_bail`, `date_paiement`, `montant`, `mode`, `commentaire`) VALUES
(1, 0, '2024-09-20', '40000', 'Wave', '1'),
(2, 0, '2024-09-20', '23000', 'Orange Money', '12'),
(8, 1, '2024-09-02', '25000', 'payer avec Wave', 'payer, reste 0 fr '),
(9, 5, '2024-01-02', '55000', 'Orange Money', 'aaa');

-- --------------------------------------------------------

--
-- Structure de la table `propriete`
--

CREATE TABLE `propriete` (
  `id_propriete` int(255) NOT NULL,
  `nom_propiete` varchar(255) NOT NULL,
  `adresse_propriete` varchar(255) NOT NULL,
  `nombres_chambres` int(255) NOT NULL,
  `nombre_de_cantine` int(11) NOT NULL,
  `nb_salle_bain` int(11) NOT NULL,
  `superficie` float NOT NULL,
  `date_dacquisition` date NOT NULL,
  `prix_louer` int(255) NOT NULL,
  `prix_achat` int(255) NOT NULL,
  `type` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `propriete`
--

INSERT INTO `propriete` (`id_propriete`, `nom_propiete`, `adresse_propriete`, `nombres_chambres`, `nombre_de_cantine`, `nb_salle_bain`, `superficie`, `date_dacquisition`, `prix_louer`, `prix_achat`, `type`) VALUES
(1, 'GNING Bulding', 'Fatick', 150, 43, 100, 50, '2025-01-04', 5470000, 945370000, 'Hotel'),
(3, 'facileImmo', 'Peulgha/Fatick', 25, 15, 10, 20, '2015-04-06', 1400000, 2147483647, 'Maison'),
(4, 'GImmo', 'Darel/Fatick', 12, 0, 5, 15, '2025-01-01', 150000, 30000000, 'Maison'),
(7, 'MSG-Immo', 'Fatick', 20, 0, 10, 20, '2010-01-01', 800000, 0, 'maison'),
(9, 'Mindiss Hotel', 'Fatick', 100, 0, 25, 50, '2008-11-11', 30000, 152000000, 'Hotel');

-- --------------------------------------------------------

--
-- Structure de la table `utilisateur`
--

CREATE TABLE `utilisateur` (
  `id_utilisateur` int(255) NOT NULL,
  `nom_utilisateur` varchar(255) NOT NULL,
  `prenom_utilisateur` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `mot_de_passe` varchar(255) NOT NULL,
  `role` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `utilisateur`
--

INSERT INTO `utilisateur` (`id_utilisateur`, `nom_utilisateur`, `prenom_utilisateur`, `email`, `mot_de_passe`, `role`) VALUES
(4, 'Faye', 'Ndeye Marie Dione', 'ndionrdeyemarie@gmail.com', '$2b$12$BYOw3AFfo8rUJArwt9Rw6Oabka6Tp5b.E39wc2T0/dhaivJ38G8Fu', 'Agent Immobilier'),
(5, 'Ba', 'Pape Demba', 'demba12@gmail.com', 'Locataire', 'Technicien d\'Entretien'),
(8, 'THIOYE', 'Cheikh', 'cheikhthioye@gmail.com', '$2b$12$BFM.OmfupVvSxlBt9snGEuIRZh2aed0WIUQCHmHNc0nFGXAmbuatC', 'Technicien d\'Entretien'),
(11, 'GNING', 'Mbery sene', 'mberysenegning@gmail.com', '$2b$12$R9fwG5FYp8Magbla7KCN/uNR4qRtPjYyucie2BMYkPlpevrmHcu9C', 'Administrateur'),
(13, 'GNING', 'Fatou', 'fatougning@gmail.com', '$2b$12$zEGAR21NvoOytEqsdFPMT.amJFn7rYUFGtf9Z.lOnvBxQ5.7cxdgi', 'Comptable'),
(31, 'GNING', 'Babacar', 'babacar23@gmail.com', '$2b$12$ztAIzgrJ1Oz8j5KDeYkJkefSvv1Q1k6b9G7GLVK3UhPTzZ6Uv/lX2', 'Administrateur'),
(32, 'faye', 'ramatoulaye', 'ramatoulaye@gmail.com', 'Administrateur', 'Gestionnaire de Propriétés'),
(33, 'gning', 'mbery', 'mberysene@gmail.com', '$2b$12$crkVbPesAY/8WIMeCSEqwuzJeektl78mPd7s1CNGgpqGGhhEtGDji', 'Administrateur'),
(47, 'faye', 'ibrahima', 'ibrahima@gmail.com', '$2b$12$ACnjy73ayaRTUi33s.W5JeMrkIHge0ShjAArU4Pb8avIbOoLJS.Ma', 'Comptable'),
(51, 'GNING', 'MARIE ', 'mariegning@gmail.com', '$2b$12$kwFWVagbYJpVys/gDG4vb.aYFRkt2uWc77XiL6A.RJAcc4Q7gKb4W', 'Agent Immobilier'),
(66, 'Tamboura', 'Fatou', 'tamboura@gmail.com', '$2b$12$X17rbZQbf8RY0fhe3CTSMuhlUHKhRgw54Eka/6MT/n0Qp8dGzLvpq', 'Agent Immobilier');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `bail`
--
ALTER TABLE `bail`
  ADD PRIMARY KEY (`id_bail`),
  ADD KEY `id_propriete` (`id_propriete`),
  ADD KEY `id_locataire` (`id_locataire`);

--
-- Index pour la table `entretien`
--
ALTER TABLE `entretien`
  ADD PRIMARY KEY (`id_entretien`),
  ADD KEY `id_propriete` (`id_propriete`) USING BTREE;

--
-- Index pour la table `locataire`
--
ALTER TABLE `locataire`
  ADD PRIMARY KEY (`id_locataire`);

--
-- Index pour la table `paiement`
--
ALTER TABLE `paiement`
  ADD PRIMARY KEY (`id_paiement`),
  ADD KEY `id_bail` (`id_bail`);

--
-- Index pour la table `propriete`
--
ALTER TABLE `propriete`
  ADD PRIMARY KEY (`id_propriete`);

--
-- Index pour la table `utilisateur`
--
ALTER TABLE `utilisateur`
  ADD PRIMARY KEY (`id_utilisateur`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `bail`
--
ALTER TABLE `bail`
  MODIFY `id_bail` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT pour la table `entretien`
--
ALTER TABLE `entretien`
  MODIFY `id_entretien` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT pour la table `locataire`
--
ALTER TABLE `locataire`
  MODIFY `id_locataire` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT pour la table `paiement`
--
ALTER TABLE `paiement`
  MODIFY `id_paiement` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT pour la table `propriete`
--
ALTER TABLE `propriete`
  MODIFY `id_propriete` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT pour la table `utilisateur`
--
ALTER TABLE `utilisateur`
  MODIFY `id_utilisateur` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=67;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `bail`
--
ALTER TABLE `bail`
  ADD CONSTRAINT `fk_locataire` FOREIGN KEY (`id_locataire`) REFERENCES `locataire` (`id_locataire`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_prpriete1` FOREIGN KEY (`id_propriete`) REFERENCES `propriete` (`id_propriete`) ON UPDATE CASCADE;

--
-- Contraintes pour la table `entretien`
--
ALTER TABLE `entretien`
  ADD CONSTRAINT `fk_propriete` FOREIGN KEY (`id_propriete`) REFERENCES `propriete` (`id_propriete`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
