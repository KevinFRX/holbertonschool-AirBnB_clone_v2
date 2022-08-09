-- script that prepares a MySQL server for the project

-- Creates DATABASE
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Creates USER 

CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- Setting PRIVILEGES to USERS

GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';

GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';

-- to make changes effective
FLUSH PRIVILEGES;
