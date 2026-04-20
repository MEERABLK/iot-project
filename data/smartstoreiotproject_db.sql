-- phpMyAdmin SQL Dump
-- version 5.2.2deb1+deb13u1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Apr 20, 2026 at 02:35 PM
-- Server version: 11.8.6-MariaDB-0+deb13u1 from Debian
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
CREATE DATABASE IF NOT EXISTS `smartstoreiotproject_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci;
USE `smartstoreiotproject_db`;

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

DROP TABLE IF EXISTS `admins`;
CREATE TABLE IF NOT EXISTS `admins` (
  `admin_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`admin_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
CREATE TABLE IF NOT EXISTS `customers` (
  `customer_id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `address` varchar(150) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `province` varchar(50) DEFAULT NULL,
  `postal_code` varchar(10) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `membership_number` varchar(20) DEFAULT NULL,
  `points` int(11) DEFAULT 0,
  `password` varchar(255) NOT NULL,
  `username` text DEFAULT NULL,
  PRIMARY KEY (`customer_id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `membership_number` (`membership_number`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `customers`
--

INSERT INTO `customers` (`customer_id`, `first_name`, `last_name`, `email`, `phone`, `address`, `city`, `province`, `postal_code`, `created_at`, `membership_number`, `points`, `password`, `username`) VALUES
(1, 'Alex', 'Smith', 'alex.smith@email.com', '514-123-4567', '123 Cali St', 'Montreal', 'QC', 'H4N497', '2026-02-23 22:35:14', NULL, 0, '', ''),
(17, 'Meerab', 'Khan', 'tera@gmail.com', '514-456-9870', '123 St-Marie', 'Quebec', 'Montreal', 'H4R27U', '2026-02-26 04:37:56', NULL, 0, '', ''),
(18, 'gd', 'dg', 'juko@gmail.com', 'das', 'asd', 'asd', 'ads', 'das', '2026-02-26 04:47:55', NULL, 0, '', ''),
(19, 'df', 'sdf', 'meerab@gmai.com', '5146789900', '456 Boulevard Nac', 'Manitoba', 'dsf', 'H5N2O9', '2026-02-26 05:19:10', NULL, 0, '', ''),
(26, 'Test', 'Testington', 'testington5242@gmail.com', '5141231234', 'Test street', 'Tester', 'Tested', 'H2G3F4', '2026-04-15 23:30:11', '123456789011', 2573, 'Test123!', ''),
(27, '', '', 'jonathan.markovic@outlook.com', NULL, NULL, NULL, NULL, NULL, '2026-04-16 01:20:26', NULL, 410, '1234', ''),
(28, NULL, NULL, 'test2@gmail.com', NULL, NULL, NULL, NULL, NULL, '2026-04-16 02:02:36', NULL, 0, '1234', 'test');

-- --------------------------------------------------------

--
-- Table structure for table `inventory`
--

DROP TABLE IF EXISTS `inventory`;
CREATE TABLE IF NOT EXISTS `inventory` (
  `inventory_id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT 0,
  `last_updated` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`inventory_id`),
  UNIQUE KEY `unique_product` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
CREATE TABLE IF NOT EXISTS `products` (
  `product_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `category` varchar(50) DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `upc` varchar(13) DEFAULT NULL,
  `epc` varchar(24) DEFAULT NULL,
  `producer` varchar(100) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `quantity` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`product_id`),
  UNIQUE KEY `upc` (`upc`),
  UNIQUE KEY `epc` (`epc`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`product_id`, `name`, `category`, `price`, `upc`, `epc`, `producer`, `image`, `quantity`) VALUES
(1, 'Milk 1L', 'Dairy', 4.00, '9876543210123', 'A00000000000000000004938', 'Dairy', '', 0),
(2, 'Coke', 'sodas', 10.00, '9568947695', 'A00000000000000000004958', 'Coke', '', 150),
(3, 'Hat', 'Clothing', 15.00, '123456789012', 'A00000000000000000004956', 'Nike', '', 10),
(4, 'Pants', 'Clothing', 25.00, '495749574957', 'A00000000000000000004957', 'Adidas', '', 10),
(5, 'Shirt', 'Clothing', 25.00, '493049304930', 'A00000000000000000004930', 'Clothing co.', 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%2Fid%2FOIP.S6n6N2vjxrOqOxtUzjolHAHaHa%3Fpid%3DApi&f=1&ipt=9b5ad7ba08fdbdd2ab0e69df75df7734eb621372e89b74077f424d83f0307276&ipo=images', 20),
(6, 'Gloves', 'Clothing', 5.00, '123412341234', '123412341234', 'Glove co', '', 15);

-- --------------------------------------------------------

--
-- Table structure for table `receipts`
--

DROP TABLE IF EXISTS `receipts`;
CREATE TABLE IF NOT EXISTS `receipts` (
  `receipt_id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_id` int(11) DEFAULT NULL,
  `total` decimal(10,2) DEFAULT NULL,
  `points_earned` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `payment_method` varchar(50) DEFAULT 'SIMULATION',
  `status` varchar(20) DEFAULT 'completed',
  PRIMARY KEY (`receipt_id`),
  KEY `customer_id` (`customer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `receipts`
--

INSERT INTO `receipts` (`receipt_id`, `customer_id`, `total`, `points_earned`, `created_at`, `payment_method`, `status`) VALUES
(1, 1, 164.94, 164, '2026-04-15 20:11:51', 'SIMULATION', 'completed'),
(2, 1, 199.92, 199, '2026-04-15 20:13:47', 'SIMULATION', 'completed'),
(3, 1, 49.98, 49, '2026-04-15 20:14:11', 'SIMULATION', 'completed'),
(4, 1, 49.98, 49, '2026-04-15 20:14:30', 'SIMULATION', 'completed'),
(5, 1, 39.99, 39, '2026-04-15 20:16:50', 'SIMULATION', 'completed'),
(6, 1, 99.96, 99, '2026-04-15 20:20:17', 'SIMULATION', 'completed'),
(9, 26, 49.98, 49, '2026-04-15 21:14:19', 'SIMULATION', 'completed'),
(10, 26, 73.47, 73, '2026-04-15 21:20:53', 'SIMULATION', 'completed'),
(11, 27, 74.97, 74, '2026-04-15 21:21:16', 'SIMULATION', 'completed'),
(12, 27, 24.99, 24, '2026-04-15 21:49:48', 'SIMULATION', 'completed'),
(13, 27, 124.95, 124, '2026-04-15 21:58:10', 'SIMULATION', 'completed'),
(14, 27, 44.99, 44, '2026-04-16 07:52:53', 'SIMULATION', 'completed'),
(15, 27, 74.98, 74, '2026-04-16 07:59:40', 'SIMULATION', 'completed'),
(16, 27, 70.00, 70, '2026-04-16 09:03:10', 'SIMULATION', 'completed');

-- --------------------------------------------------------

--
-- Table structure for table `receipt_items`
--

DROP TABLE IF EXISTS `receipt_items`;
CREATE TABLE IF NOT EXISTS `receipt_items` (
  `item_id` int(11) NOT NULL AUTO_INCREMENT,
  `receipt_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `subtotal` decimal(10,2) GENERATED ALWAYS AS (`quantity` * `price`) STORED,
  PRIMARY KEY (`item_id`),
  KEY `receipt_id` (`receipt_id`),
  KEY `product_id` (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `receipt_items`
--

INSERT INTO `receipt_items` (`item_id`, `receipt_id`, `product_id`, `quantity`, `price`) VALUES
(1, 1, 4, 5, 24.99),
(2, 1, 5, 1, 24.99),
(3, 1, 3, 1, 15.00),
(4, 2, 4, 7, 24.99),
(5, 2, 5, 1, 24.99),
(6, 3, 4, 2, 24.99),
(7, 4, 4, 2, 24.99),
(8, 5, 4, 1, 24.99),
(9, 5, 3, 1, 15.00),
(10, 6, 4, 4, 24.99),
(17, 9, 5, 1, 24.99),
(18, 9, 4, 1, 24.99),
(19, 10, 5, 3, 24.99),
(20, 11, 4, 3, 24.99),
(21, 12, 4, 1, 24.99),
(22, 13, 4, 5, 24.99),
(23, 14, 6, 1, 5.00),
(24, 14, 5, 1, 24.99),
(25, 14, 3, 1, 15.00),
(26, 15, 6, 2, 5.00),
(27, 15, 3, 1, 15.00),
(28, 15, 5, 1, 24.99),
(29, 15, 4, 1, 24.99),
(30, 16, 4, 1, 25.00),
(31, 16, 6, 1, 5.00),
(32, 16, 3, 1, 15.00),
(33, 16, 5, 1, 25.00);

-- --------------------------------------------------------

--
-- Table structure for table `receptions`
--

DROP TABLE IF EXISTS `receptions`;
CREATE TABLE IF NOT EXISTS `receptions` (
  `reception_id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) DEFAULT NULL,
  `quantity_received` int(11) DEFAULT NULL,
  `date_received` datetime DEFAULT current_timestamp(),
  `supplier` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`reception_id`),
  KEY `product_id` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `rfid_tags`
--

DROP TABLE IF EXISTS `rfid_tags`;
CREATE TABLE IF NOT EXISTS `rfid_tags` (
  `upc` text NOT NULL,
  `epc` text NOT NULL,
  UNIQUE KEY `rfid_unique` (`epc`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `thresholds`
--

DROP TABLE IF EXISTS `thresholds`;
CREATE TABLE IF NOT EXISTS `thresholds` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fridge_name` varchar(50) DEFAULT NULL,
  `temperature_threshold` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `thresholds`
--

INSERT INTO `thresholds` (`id`, `fridge_name`, `temperature_threshold`) VALUES
(1, 'fridge1', 7),
(2, 'fridge2', 5),
(3, 'fridge1', 9),
(4, 'fridge1', 9),
(5, 'fridge1', 9),
(6, 'fridge1', 9),
(7, 'fridge1', 8),
(8, 'fridge2', 6),
(9, 'fridge1', 9),
(10, 'fridge2', 10),
(11, 'fridge1', 9),
(12, 'fridge1', 9),
(13, 'fridge1', 19);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `inventory`
--
ALTER TABLE `inventory`
  ADD CONSTRAINT `inventory_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`);

--
-- Constraints for table `receipts`
--
ALTER TABLE `receipts`
  ADD CONSTRAINT `receipts_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`);

--
-- Constraints for table `receipt_items`
--
ALTER TABLE `receipt_items`
  ADD CONSTRAINT `receipt_items_ibfk_1` FOREIGN KEY (`receipt_id`) REFERENCES `receipts` (`receipt_id`),
  ADD CONSTRAINT `receipt_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`);

--
-- Constraints for table `receptions`
--
ALTER TABLE `receptions`
  ADD CONSTRAINT `receptions_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
