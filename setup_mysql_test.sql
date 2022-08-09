-- script that prepares a MySQL server for the project

-- Creates DATABASE
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Creates USER 

CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Setting PRIVILEGES to USERS

GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';

-- to make changes effective
FLUSH PRIVILEGES;
