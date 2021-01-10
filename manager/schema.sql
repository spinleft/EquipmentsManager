DROP DATABASE equipment;
CREATE DATABASE equipment;
USE equipment;

CREATE TABLE `user` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(255) UNIQUE NOT NULL,
    `password` TEXT NOT NULL
);

CREATE TABLE `information` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `type` ENUM("设备", "材料") NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `model` VARCHAR(255),
    `serial_number` VARCHAR(255),
    `contract_number` TEXT,
    `arrival_date` DATE,
    `transactor` TEXT,
    `status` ENUM("在用", "待用", "被借", "待维修", "维修中"),
    `location` TEXT,
    `contract_files` TEXT,
    `photo` TEXT,
    `location_photo` TEXT,
    `comment` TEXT,
    UNIQUE (`name`, `model`, `serial_number`)
);

CREATE VIEW `amount_count`(`type`, `name`, `model`, `amount`) AS
SELECT `type`, `name`, `model`, COUNT(*)
FROM `information`
GROUP BY `type`, `name`, `model`;

INSERT INTO `information`(`type`, `name`, `model`, `serial_number`, `contract_number`, `arrival_date`, `transactor`, `status`, `location`, `contract_files`, `photo`, `location_photo`, `comment`)
VALUES('设备', '激光器', '1型', 'cx123', '11245134', '2018-02-03', '陈思源', '在用', '1号台', '', '', '', '');

INSERT INTO `information`(`type`, `name`, `model`, `serial_number`, `contract_number`, `arrival_date`, `transactor`, `status`, `location`, `contract_files`, `photo`, `location_photo`, `comment`)
VALUES('材料', '探头', 'A型', 'pb234', '265463', '2018-09-11', '陈思源', '在用', '1号台', '', '', '', '');

