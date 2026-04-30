-- phpMyAdmin SQL Dump
-- version 5.2.2deb1+deb13u1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Apr 29, 2026 at 11:56 PM
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
-- Table structure for table `ble_sensor_logs`
--

CREATE TABLE `ble_sensor_logs` (
  `log_id` int(11) NOT NULL,
  `sensor_name` varchar(50) DEFAULT NULL,
  `temperature` decimal(5,2) DEFAULT NULL,
  `humidity` decimal(5,2) DEFAULT NULL,
  `light_level` int(11) DEFAULT NULL,
  `motion_detected` tinyint(1) DEFAULT 0,
  `recorded_at` datetime DEFAULT current_timestamp()
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
(1, 'Alex', 'Smith', 'alex.smith@email.com', '514-123-4567', '123 Cali St', 'Montreal', 'QC', 'H4N497', '2026-02-23 22:35:14', 36, 'pokemone1', NULL),
(17, 'Meerab', 'Khan', 'tera@gmail.com', '514-456-9870', '123 St-Marie', 'Quebec', 'Montreal', 'H4R27U', '2026-02-26 04:37:56', 0, '', NULL),
(18, 'gd', 'dg', 'juko@gmail.com', 'das', 'asd', 'asd', 'ads', 'das', '2026-02-26 04:47:55', 0, '', NULL),
(19, 'df', 'sdf', 'meerab@gmai.com', '5146789900', '456 Boulevard Nac', 'Manitoba', 'dsf', 'H5N2O9', '2026-02-26 05:19:10', 0, '', NULL),
(26, NULL, NULL, 'lowkeymischievous@gmail.com', NULL, NULL, NULL, NULL, NULL, '2026-04-16 01:21:17', 252, 'pokemone1', '2388387'),
(27, NULL, NULL, 'enfernapcoder@gmail.com', NULL, NULL, NULL, NULL, NULL, '2026-04-29 17:04:45', 216, 'pokemone1', '2388387');

-- --------------------------------------------------------

--
-- Table structure for table `inventory`
--

CREATE TABLE `inventory` (
  `inventory_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT 0,
  `last_updated` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `inventory`
--

INSERT INTO `inventory` (`inventory_id`, `product_id`, `quantity`, `last_updated`) VALUES
(9, 46, -12, '2026-04-29 14:37:12'),
(11, 48, 90, '2026-04-29 12:57:54'),
(12, 49, 12, '2026-04-29 19:53:35');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `product_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `category` varchar(50) DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `producer` varchar(100) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`product_id`, `name`, `category`, `price`, `producer`, `image`) VALUES
(46, 'KitKat', 'chocolates', 12.00, 'forgot', 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Feditorial.designtaxi.com%2Fimages%2FKitKat-US-Logo-1-1723703502.jpeg&f=1&nofb=1&ipt=d7a2ee5dbcc8404c80e032572e963d6e2f18f87b923becd4b2f370de051bf318'),
(48, 'Oh Henry', 'chocolates', 12.00, 'forgot', 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.snackhistory.com%2Fwp-content%2Fuploads%2F2021%2F11%2FOh-Henry-Level-Up-1024x1024.jpg&f=1&nofb=1&ipt=574883d21ee18b61573470366e7469f91eb5ba1fd6e35365f87a7ab7a08ffe27'),
(49, 'KitKat', 'chocolates', 12.00, 'forgot', 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Feditorial.designtaxi.com%2Fimages%2FKitKat-US-Logo-1-1723703502.jpeg&f=1&nofb=1&ipt=d7a2ee5dbcc8404c80e032572e963d6e2f18f87b923becd4b2f370de051bf318');

-- --------------------------------------------------------

--
-- Table structure for table `product_rfid`
--

CREATE TABLE `product_rfid` (
  `rfid_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `epc_code` varchar(24) NOT NULL,
  `status` enum('in_stock','sold','lost','accepted') DEFAULT 'in_stock'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `product_rfid`
--

INSERT INTO `product_rfid` (`rfid_id`, `product_id`, `epc_code`, `status`) VALUES
(15, 46, 'A00000000000000000004958', 'in_stock'),
(18, 48, 'A00000000000000000004960', 'in_stock');

-- --------------------------------------------------------

--
-- Table structure for table `product_upc`
--

CREATE TABLE `product_upc` (
  `upc_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `upc_code` varchar(13) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `product_upc`
--

INSERT INTO `product_upc` (`upc_id`, `product_id`, `upc_code`) VALUES
(18, 46, '123412341234'),
(22, 48, '789012456550'),
(24, 49, '09876789013');

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
(3, 26, 4.00, 4, '2026-04-15 21:54:45', 'SIMULATION', 'completed'),
(4, 26, 4.00, 4, '2026-04-15 22:14:29', 'SIMULATION', 'completed'),
(5, 26, 35.00, 35, '2026-04-26 22:29:55', 'SIMULATION', 'completed'),
(6, 26, 113.00, 113, '2026-04-26 23:07:33', 'SIMULATION', 'completed'),
(9, 26, 12.00, 12, '2026-04-27 22:10:46', 'SIMULATION', 'completed'),
(10, 1, 36.00, 36, '2026-04-27 22:53:13', 'SIMULATION', 'completed'),
(11, 26, 36.00, 36, '2026-04-27 22:53:26', 'SIMULATION', 'completed'),
(12, 26, 12.00, 12, '2026-04-27 23:30:00', 'SIMULATION', 'completed'),
(13, 26, 12.00, 12, '2026-04-27 23:31:15', 'SIMULATION', 'completed'),
(14, 26, 12.00, 12, '2026-04-27 23:44:00', 'SIMULATION', 'completed'),
(15, 26, 12.00, 12, '2026-04-27 23:44:53', 'SIMULATION', 'completed'),
(16, 27, 12.00, 12, '2026-04-29 13:12:43', 'SIMULATION', 'completed'),
(17, 27, 12.00, 12, '2026-04-29 13:18:25', 'SIMULATION', 'completed'),
(18, 27, 12.00, 12, '2026-04-29 13:22:28', 'SIMULATION', 'completed'),
(19, 27, 12.00, 12, '2026-04-29 13:28:50', 'SIMULATION', 'completed'),
(20, 27, 12.00, 12, '2026-04-29 13:30:50', 'SIMULATION', 'completed'),
(21, 27, 12.00, 12, '2026-04-29 13:36:18', 'SIMULATION', 'completed'),
(22, 27, 12.00, 12, '2026-04-29 13:40:25', 'SIMULATION', 'completed'),
(23, 27, 12.00, 12, '2026-04-29 13:42:32', 'SIMULATION', 'completed'),
(24, 27, 12.00, 12, '2026-04-29 13:44:00', 'SIMULATION', 'completed'),
(25, 27, 12.00, 12, '2026-04-29 13:50:14', 'SIMULATION', 'completed'),
(26, 27, 12.00, 12, '2026-04-29 13:52:39', 'SIMULATION', 'completed'),
(27, 27, 12.00, 12, '2026-04-29 13:54:39', 'SIMULATION', 'completed'),
(28, 27, 12.00, 12, '2026-04-29 13:55:28', 'SIMULATION', 'completed'),
(29, 27, 12.00, 12, '2026-04-29 13:56:02', 'SIMULATION', 'completed'),
(30, 27, 12.00, 12, '2026-04-29 14:02:08', 'SIMULATION', 'completed'),
(31, 27, 12.00, 12, '2026-04-29 14:09:33', 'SIMULATION', 'completed'),
(32, 27, 12.00, 12, '2026-04-29 14:32:08', 'SIMULATION', 'completed'),
(33, 27, 12.00, 12, '2026-04-29 14:37:12', 'SIMULATION', 'completed');

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
(10, 10, 46, 1, 12.00),
(12, 11, 46, 1, 12.00),
(14, 12, 46, 1, 12.00),
(15, 12, 46, 1, 12.00),
(16, 13, 46, 1, 12.00),
(17, 13, 46, 1, 12.00),
(18, 14, 46, 1, 12.00),
(19, 14, 46, 1, 12.00),
(20, 15, 46, 1, 12.00),
(21, 15, 46, 1, 12.00),
(22, 16, 46, 1, 12.00),
(23, 16, 46, 1, 12.00),
(24, 17, 46, 1, 12.00),
(25, 17, 46, 1, 12.00),
(26, 18, 46, 1, 12.00),
(27, 18, 46, 1, 12.00),
(28, 19, 46, 1, 12.00),
(29, 19, 46, 1, 12.00),
(30, 20, 46, 1, 12.00),
(31, 20, 46, 1, 12.00),
(32, 21, 46, 1, 12.00),
(33, 21, 46, 1, 12.00),
(34, 22, 46, 1, 12.00),
(35, 22, 46, 1, 12.00),
(36, 23, 46, 1, 12.00),
(37, 23, 46, 1, 12.00),
(38, 24, 46, 1, 12.00),
(39, 24, 46, 1, 12.00),
(40, 25, 46, 1, 12.00),
(41, 25, 46, 1, 12.00),
(42, 26, 46, 1, 12.00),
(43, 26, 46, 1, 12.00),
(44, 27, 46, 1, 12.00),
(45, 27, 46, 1, 12.00),
(46, 28, 46, 1, 12.00),
(47, 28, 46, 1, 12.00),
(48, 29, 46, 1, 12.00),
(49, 29, 46, 1, 12.00),
(50, 30, 46, 1, 12.00),
(51, 30, 46, 1, 12.00),
(52, 31, 46, 1, 12.00),
(53, 31, 46, 1, 12.00),
(54, 32, 46, 1, 12.00),
(55, 32, 46, 1, 12.00),
(56, 33, 46, 1, 12.00),
(57, 33, 46, 1, 12.00);

-- --------------------------------------------------------

--
-- Table structure for table `receptions`
--

CREATE TABLE `receptions` (
  `reception_id` int(11) NOT NULL,
  `product_id` int(11) DEFAULT NULL,
  `quantity_received` int(11) DEFAULT NULL,
  `date_received` datetime DEFAULT current_timestamp(),
  `supplier` varchar(100) DEFAULT NULL,
  `supplier_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `report_exports`
--

CREATE TABLE `report_exports` (
  `export_id` int(11) NOT NULL,
  `report_type` varchar(50) DEFAULT NULL,
  `exported_by` varchar(50) DEFAULT NULL,
  `export_format` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `stock_thresholds`
--

CREATE TABLE `stock_thresholds` (
  `threshold_id` int(11) NOT NULL,
  `category` varchar(50) NOT NULL,
  `min_quantity` int(11) NOT NULL DEFAULT 5
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `suppliers`
--

CREATE TABLE `suppliers` (
  `supplier_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL
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
-- Indexes for table `ble_sensor_logs`
--
ALTER TABLE `ble_sensor_logs`
  ADD PRIMARY KEY (`log_id`);

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
  ADD UNIQUE KEY `product_id` (`product_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`product_id`);

--
-- Indexes for table `product_rfid`
--
ALTER TABLE `product_rfid`
  ADD PRIMARY KEY (`rfid_id`),
  ADD UNIQUE KEY `epc_code` (`epc_code`),
  ADD UNIQUE KEY `uq_epc_code` (`epc_code`),
  ADD KEY `product_rfid_ibfk_1` (`product_id`);

--
-- Indexes for table `product_upc`
--
ALTER TABLE `product_upc`
  ADD PRIMARY KEY (`upc_id`),
  ADD UNIQUE KEY `upc_code` (`upc_code`),
  ADD UNIQUE KEY `uq_upc_code` (`upc_code`),
  ADD UNIQUE KEY `product_id` (`product_id`),
  ADD KEY `product_upc_ibfk_1` (`product_id`);

--
-- Indexes for table `receipts`
--
ALTER TABLE `receipts`
  ADD PRIMARY KEY (`receipt_id`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `idx_receipts_customer` (`customer_id`);

--
-- Indexes for table `receipt_items`
--
ALTER TABLE `receipt_items`
  ADD PRIMARY KEY (`item_id`),
  ADD KEY `receipt_id` (`receipt_id`),
  ADD KEY `product_id` (`product_id`),
  ADD KEY `idx_items_receipt` (`receipt_id`),
  ADD KEY `idx_items_product` (`product_id`);

--
-- Indexes for table `receptions`
--
ALTER TABLE `receptions`
  ADD PRIMARY KEY (`reception_id`),
  ADD KEY `product_id` (`product_id`),
  ADD KEY `fk_receptions_supplier` (`supplier_id`);

--
-- Indexes for table `report_exports`
--
ALTER TABLE `report_exports`
  ADD PRIMARY KEY (`export_id`);

--
-- Indexes for table `stock_thresholds`
--
ALTER TABLE `stock_thresholds`
  ADD PRIMARY KEY (`threshold_id`);

--
-- Indexes for table `suppliers`
--
ALTER TABLE `suppliers`
  ADD PRIMARY KEY (`supplier_id`),
  ADD UNIQUE KEY `name` (`name`);

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
  MODIFY `customer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT for table `inventory`
--
ALTER TABLE `inventory`
  MODIFY `inventory_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=50;

--
-- AUTO_INCREMENT for table `product_rfid`
--
ALTER TABLE `product_rfid`
  MODIFY `rfid_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `product_upc`
--
ALTER TABLE `product_upc`
  MODIFY `upc_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `receipts`
--
ALTER TABLE `receipts`
  MODIFY `receipt_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT for table `receipt_items`
--
ALTER TABLE `receipt_items`
  MODIFY `item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=58;

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
-- AUTO_INCREMENT for table `suppliers`
--
ALTER TABLE `suppliers`
  MODIFY `supplier_id` int(11) NOT NULL AUTO_INCREMENT;

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
  ADD CONSTRAINT `fk_inventory_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE;

--
-- Constraints for table `product_rfid`
--
ALTER TABLE `product_rfid`
  ADD CONSTRAINT `fk_rfid_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `product_rfid_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE;

--
-- Constraints for table `product_upc`
--
ALTER TABLE `product_upc`
  ADD CONSTRAINT `fk_upc_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `product_upc_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE;

--
-- Constraints for table `receipts`
--
ALTER TABLE `receipts`
  ADD CONSTRAINT `fk_receipts_customer` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `receipts_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`);

--
-- Constraints for table `receipt_items`
--
ALTER TABLE `receipt_items`
  ADD CONSTRAINT `fk_items_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`),
  ADD CONSTRAINT `fk_items_receipt` FOREIGN KEY (`receipt_id`) REFERENCES `receipts` (`receipt_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `receipt_items_ibfk_1` FOREIGN KEY (`receipt_id`) REFERENCES `receipts` (`receipt_id`);

--
-- Constraints for table `receptions`
--
ALTER TABLE `receptions`
  ADD CONSTRAINT `fk_receptions_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`),
  ADD CONSTRAINT `fk_receptions_supplier` FOREIGN KEY (`supplier_id`) REFERENCES `suppliers` (`supplier_id`),
  ADD CONSTRAINT `receptions_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
