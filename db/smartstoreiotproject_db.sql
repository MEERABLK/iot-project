-- phpMyAdmin SQL Dump
-- version 5.2.2deb1+deb13u1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Mar 25, 2026 at 01:28 AM
-- Server version: 11.8.3-MariaDB-0+deb13u1 from Debian
-- PHP Version: 8.4.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `smartstoreiotproject_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

CREATE TABLE `customers` (
  `customer_id` int(11) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `address` varchar(150) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `province` varchar(50) DEFAULT NULL,
  `postal_code` varchar(10) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `customers`
--

INSERT INTO `customers` (`customer_id`, `first_name`, `last_name`, `email`, `phone`, `address`, `city`, `province`, `postal_code`, `created_at`) VALUES
(1, 'Alex', 'Smith', 'alex.smith@email.com', '514-123-4567', '123 Cali St', 'Montreal', 'QC', 'H4N497', '2026-02-23 22:35:14'),
(17, 'Meerab', 'Khan', 'tera@gmail.com', '514-456-9870', '123 St-Marie', 'Quebec', 'Montreal', 'H4R27U', '2026-02-26 04:37:56'),
(18, 'gd', 'dg', 'juko@gmail.com', 'das', 'asd', 'asd', 'ads', 'das', '2026-02-26 04:47:55'),
(19, 'df', 'sdf', 'meerab@gmai.com', '5146789900', '456 Boulevard Nac', 'Manitoba', 'dsf', 'H5N2O9', '2026-02-26 05:19:10');

-- --------------------------------------------------------

--
-- Table structure for table `thresholds`
--

CREATE TABLE `thresholds` (
  `id` int(11) NOT NULL,
  `fridge_name` varchar(50) DEFAULT NULL,
  `temperature_threshold` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `thresholds`
--

INSERT INTO `thresholds` (`id`, `fridge_name`, `temperature_threshold`) VALUES
(1, 'fridge1', 8),
(2, 'fridge2', 5);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`customer_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `thresholds`
--
ALTER TABLE `thresholds`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `customer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `thresholds`
--
ALTER TABLE `thresholds`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
