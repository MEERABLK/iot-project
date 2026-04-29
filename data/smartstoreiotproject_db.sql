-- phpMyAdmin SQL Dump
-- version 5.2.2deb1+deb13u1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Apr 27, 2026 at 12:20 AM
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

CREATE TABLE IF NOT EXISTS `admins` (
  `admin_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ble_sensor_logs`
--

CREATE TABLE IF NOT EXISTS `ble_sensor_logs` (
  `log_id` int(11) NOT NULL,
  `sensor_name` varchar(50) DEFAULT NULL,
  `temperature` decimal(5,2) DEFAULT NULL,
  `humidity` decimal(5,2) DEFAULT NULL,
  `light_level` int(11) DEFAULT NULL,
  `motion_detected` tinyint(1) DEFAULT 0,
  `recorded_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

CREATE TABLE IF NOT EXISTS `customers` (
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
  `membership_number` varchar(20) DEFAULT NULL,
  `points` int(11) DEFAULT 0,
  `password` varchar(255) NOT NULL,
  `username` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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

CREATE TABLE IF NOT EXISTS `inventory` (
  `inventory_id` int(11) NOT NULL,
  `product_id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT 0,
  `last_updated` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE IF NOT EXISTS `products` (
  `product_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `category` varchar(50) DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `upc` varchar(13) DEFAULT NULL,
  `producer` varchar(100) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `quantity` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`product_id`, `name`, `category`, `price`, `upc`, `producer`, `image`, `quantity`) VALUES
(1, 'Milk 1L', 'Dairy', 4.00, '9876543210123', 'Dairy', '', 0),
(2, 'Coke', 'sodas', 10.00, '9568947695', 'Coke', '', 150),
(3, 'Hat', 'Clothing', 15.00, '123456789012', 'Nike', '', 10),
(4, 'Pants', 'Clothing', 25.00, '495749574957', 'Adidas', '', 10),
(5, 'Shirt', 'Clothing', 25.00, '493049304930', 'Clothing co.', 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%2Fid%2FOIP.S6n6N2vjxrOqOxtUzjolHAHaHa%3Fpid%3DApi&f=1&ipt=9b5ad7ba08fdbdd2ab0e69df75df7734eb621372e89b74077f424d83f0307276&ipo=images', 20),
(6, 'Gloves', 'Clothing', 5.00, '123412341234', 'Glove co', '', 15);

-- --------------------------------------------------------

--
-- Table structure for table `receipts`
--

CREATE TABLE IF NOT EXISTS `receipts` (
  `receipt_id` int(11) NOT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `total` decimal(10,2) DEFAULT NULL,
  `points_earned` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `payment_method` varchar(50) DEFAULT 'SIMULATION',
  `status` varchar(20) DEFAULT 'completed'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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

CREATE TABLE IF NOT EXISTS `receipt_items` (
  `item_id` int(11) NOT NULL,
  `receipt_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `subtotal` decimal(10,2) GENERATED ALWAYS AS (`quantity` * `price`) STORED
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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

CREATE TABLE IF NOT EXISTS `receptions` (
  `reception_id` int(11) NOT NULL,
  `product_id` int(11) DEFAULT NULL,
  `quantity_received` int(11) DEFAULT NULL,
  `date_received` datetime DEFAULT current_timestamp(),
  `supplier` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `report_exports`
--

CREATE TABLE IF NOT EXISTS `report_exports` (
  `export_id` int(11) NOT NULL,
  `report_type` varchar(50) DEFAULT NULL,
  `exported_by` varchar(50) DEFAULT NULL,
  `export_format` enum('PDF','CSV','PNG') DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `rfid_tags`
--

CREATE TABLE IF NOT EXISTS `rfid_tags` (
  `upc` varchar(12) NOT NULL,
  `epc` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `stock_thresholds`
--

CREATE TABLE IF NOT EXISTS `stock_thresholds` (
  `threshold_id` int(11) NOT NULL,
  `category` varchar(50) DEFAULT NULL,
  `min_quantity` int(11) NOT NULL DEFAULT 5
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `thresholds`
--

CREATE TABLE IF NOT EXISTS `thresholds` (
  `id` int(11) NOT NULL,
  `fridge_name` varchar(50) DEFAULT NULL,
  `temperature_threshold` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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
-- Indexes for table `ble_sensor_logs`
--
ALTER TABLE `ble_sensor_logs`
  ADD PRIMARY KEY (`log_id`);

--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`customer_id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `membership_number` (`membership_number`);

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
  ADD UNIQUE KEY `upc` (`upc`);

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
-- Indexes for table `report_exports`
--
ALTER TABLE `report_exports`
  ADD PRIMARY KEY (`export_id`);

--
-- Indexes for table `rfid_tags`
--
ALTER TABLE `rfid_tags`
  ADD UNIQUE KEY `rfid_unique` (`epc`);

--
-- Indexes for table `stock_thresholds`
--
ALTER TABLE `stock_thresholds`
  ADD PRIMARY KEY (`threshold_id`),
  ADD UNIQUE KEY `category` (`category`);

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
-- AUTO_INCREMENT for table `ble_sensor_logs`
--
ALTER TABLE `ble_sensor_logs`
  MODIFY `log_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `customer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `inventory`
--
ALTER TABLE `inventory`
  MODIFY `inventory_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `receipts`
--
ALTER TABLE `receipts`
  MODIFY `receipt_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `receipt_items`
--
ALTER TABLE `receipt_items`
  MODIFY `item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT for table `receptions`
--
ALTER TABLE `receptions`
  MODIFY `reception_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `report_exports`
--
ALTER TABLE `report_exports`
  MODIFY `export_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `stock_thresholds`
--
ALTER TABLE `stock_thresholds`
  MODIFY `threshold_id` int(11) NOT NULL AUTO_INCREMENT;

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
