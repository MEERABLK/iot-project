-- phpMyAdmin SQL Dump
-- version 5.2.2deb1+deb13u1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Apr 16, 2026 at 02:02 AM
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
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `admin_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

CREATE TABLE `customers` (
  `customer_id` int(11) NOT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `address` varchar(150) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `province` varchar(50) DEFAULT NULL,
  `postal_code` varchar(10) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `points` int(11) DEFAULT 0,
  `password` varchar(255) NOT NULL,
  `username` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `customers`
--

INSERT INTO `customers` (`customer_id`, `first_name`, `last_name`, `email`, `phone`, `address`, `city`, `province`, `postal_code`, `created_at`, `points`, `password`, `username`) VALUES
(1, 'Alex', 'Smith', 'alex.smith@email.com', '514-123-4567', '123 Cali St', 'Montreal', 'QC', 'H4N497', '2026-02-23 22:35:14', 0, 'pokemone1', NULL),
(17, 'Meerab', 'Khan', 'tera@gmail.com', '514-456-9870', '123 St-Marie', 'Quebec', 'Montreal', 'H4R27U', '2026-02-26 04:37:56', 0, '', NULL),
(18, 'gd', 'dg', 'juko@gmail.com', 'das', 'asd', 'asd', 'ads', 'das', '2026-02-26 04:47:55', 0, '', NULL),
(19, 'df', 'sdf', 'meerab@gmai.com', '5146789900', '456 Boulevard Nac', 'Manitoba', 'dsf', 'H5N2O9', '2026-02-26 05:19:10', 0, '', NULL),
(26, NULL, NULL, 'lowkeymischievous@gmail.com', NULL, NULL, NULL, NULL, NULL, '2026-04-16 01:21:17', 4, 'pokemone1', '2388387');

-- --------------------------------------------------------

--
-- Table structure for table `inventory`
--

CREATE TABLE `inventory` (
  `inventory_id` int(11) NOT NULL,
  `product_id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT 0,
  `last_updated` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `product_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `category` varchar(50) DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `upc` varchar(13) DEFAULT NULL,
  `epc` varchar(24) DEFAULT NULL,
  `producer` varchar(100) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `quantity` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`product_id`, `name`, `category`, `price`, `upc`, `epc`, `producer`, `image`, `quantity`) VALUES
(1, 'Milk 1L', 'Dairy', 4.00, '9876543210123', 'A00000000000000000004938', 'Dairy Farm', NULL, 0),
(2, 'Coke', 'sodas', 10.00, '9568947695', 'A00000000000000000004958', 'Coke', NULL, 0),
(3, 'Hat', 'Clothing', 15.00, '123456789012', 'A00000000000000000004956', 'Nike', NULL, 0),
(4, 'Pants', NULL, 24.99, '495749574957', 'A00000000000000000004957', 'Adidas', NULL, 0),
(5, 'Shirt', 'Clothing', 24.99, '493049304930', 'A00000000000000000004930', 'Clothing co.', NULL, 0),
(6, 'KitKat', 'chocolates', 7.00, '789012456556', 'A00000000000000000004963', 'forgot', 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Feditorial.designtaxi.com%2Fimages%2FKitKat-US-Logo-1-1723703502.jpeg&f=1&nofb=1&ipt=d7a2ee5dbcc8404c80e032572e963d6e2f18f87b923becd4b2f370de051bf318', 7);

-- --------------------------------------------------------

--
-- Table structure for table `receipts`
--

CREATE TABLE `receipts` (
  `receipt_id` int(11) NOT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `total` decimal(10,2) DEFAULT NULL,
  `points_earned` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `payment_method` varchar(50) DEFAULT 'SIMULATION',
  `status` varchar(20) DEFAULT 'completed'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `receipts`
--

INSERT INTO `receipts` (`receipt_id`, `customer_id`, `total`, `points_earned`, `created_at`, `payment_method`, `status`) VALUES
(1, 1, 4.00, 4, '2026-04-15 21:34:23', 'SIMULATION', 'completed'),
(2, 1, 4.00, 4, '2026-04-15 21:35:47', 'SIMULATION', 'completed'),
(3, 26, 4.00, 4, '2026-04-15 21:54:45', 'SIMULATION', 'completed');

-- --------------------------------------------------------

--
-- Table structure for table `receipt_items`
--

CREATE TABLE `receipt_items` (
  `item_id` int(11) NOT NULL,
  `receipt_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `subtotal` decimal(10,2) GENERATED ALWAYS AS (`quantity` * `price`) STORED
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `receipt_items`
--

INSERT INTO `receipt_items` (`item_id`, `receipt_id`, `product_id`, `quantity`, `price`) VALUES
(1, 1, 1, 1, 4.00),
(2, 2, 1, 1, 4.00),
(3, 3, 1, 1, 4.00);

-- --------------------------------------------------------

--
-- Table structure for table `receptions`
--

CREATE TABLE `receptions` (
  `reception_id` int(11) NOT NULL,
  `product_id` int(11) DEFAULT NULL,
  `quantity_received` int(11) DEFAULT NULL,
  `date_received` datetime DEFAULT current_timestamp(),
  `supplier` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

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
-- Indexes for dumped tables
--

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`admin_id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`customer_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `inventory`
--
ALTER TABLE `inventory`
  ADD PRIMARY KEY (`inventory_id`),
  ADD UNIQUE KEY `unique_product` (`product_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`product_id`),
  ADD UNIQUE KEY `upc` (`upc`),
  ADD UNIQUE KEY `epc` (`epc`);

--
-- Indexes for table `receipts`
--
ALTER TABLE `receipts`
  ADD PRIMARY KEY (`receipt_id`),
  ADD KEY `customer_id` (`customer_id`);

--
-- Indexes for table `receipt_items`
--
ALTER TABLE `receipt_items`
  ADD PRIMARY KEY (`item_id`),
  ADD KEY `receipt_id` (`receipt_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `receptions`
--
ALTER TABLE `receptions`
  ADD PRIMARY KEY (`reception_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `thresholds`
--
ALTER TABLE `thresholds`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admins`
--
ALTER TABLE `admins`
  MODIFY `admin_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `customer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `inventory`
--
ALTER TABLE `inventory`
  MODIFY `inventory_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `receipts`
--
ALTER TABLE `receipts`
  MODIFY `receipt_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `receipt_items`
--
ALTER TABLE `receipt_items`
  MODIFY `item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `receptions`
--
ALTER TABLE `receptions`
  MODIFY `reception_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `thresholds`
--
ALTER TABLE `thresholds`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

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
