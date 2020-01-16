-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 16, 2020 at 03:26 PM
-- Server version: 10.4.8-MariaDB
-- PHP Version: 7.3.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `billservice`
--

-- --------------------------------------------------------

--
-- Table structure for table `bill`
--

CREATE TABLE `bill` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `quantity` varchar(10) NOT NULL,
  `rate` varchar(10) NOT NULL,
  `cost` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `bill`
--

INSERT INTO `bill` (`id`, `name`, `quantity`, `rate`, `cost`) VALUES
(46, 'banana', '1.00', '20', '20.00'),
(47, 'banana', '1.00', '20', '20.00'),
(48, 'cold_drink', '2.00', '50', '100.00'),
(49, 'banana', '1.00', '20', '20.00'),
(50, 'pizza', '3.00', '125', '375.00'),
(51, 'pizza', '1.00', '100', '100.00'),
(52, 'cold_drink', '2.00', '50', '100.00'),
(53, 'pizza', '1.00', '100', '100.00'),
(54, 'cold_drink', '1.00', '50', '50.00'),
(55, 'pizza', '2.00', '100', '200.00'),
(56, 'cold_drink', '2.00', '50', '100.00'),
(57, 'pizza', '3.00', '100', '300.00'),
(58, 'cold_drink', '2.00', '50', '100.00'),
(59, 'pizza', '3.00', '100', '300.00'),
(60, 'cold_drink', '2.00', '50', '100.00'),
(61, 'pizza', '3.00', '100', '300.00'),
(62, 'cold_drink', '2.00', '50', '100.00'),
(63, 'cold_drink', '2.00', '50', '100.00'),
(64, 'pizza', '5.00', '100', '500.00');

-- --------------------------------------------------------

--
-- Table structure for table `itemlist`
--

CREATE TABLE `itemlist` (
  `name` varchar(32) NOT NULL,
  `nameid` varchar(32) NOT NULL,
  `rate` varchar(10) NOT NULL,
  `type` varchar(32) NOT NULL,
  `storetype` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `itemlist`
--

INSERT INTO `itemlist` (`name`, `nameid`, `rate`, `type`, `storetype`) VALUES
('cold drink', 'cold_drink', '50', 'energy drink', 'Fresh'),
('d_pizza', 'pizza', '100', 'fastfood', 'Frozen');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `username` varchar(32) NOT NULL,
  `password` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`username`, `password`) VALUES
('admin', '123456');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bill`
--
ALTER TABLE `bill`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `itemlist`
--
ALTER TABLE `itemlist`
  ADD PRIMARY KEY (`nameid`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bill`
--
ALTER TABLE `bill`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=65;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
