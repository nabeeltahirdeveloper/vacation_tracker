-- Script to prepares a MySQL Server for the Vacation Tracker Webapp

CREATE DATABASE IF NOT EXISTS `lynks_db`;
CREATE USER IF NOT EXISTS 'lynks_eng'@'localhost' IDENTIFIED BY 'lynks_eng_pwd';
GRANT ALL PRIVILEGES ON lynks_db . * TO 'lynks_eng'@'localhost';
FLUSH PRIVILEGES;
GRANT SELECT ON  `performance_schema`.* TO 'lynks_eng'@'localhost';

FLUSH PRIVILEGES;

