-- In and not out
-- Create a users table
CREATE TABLE IF NOT EXISTS `users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(255) NOT NULL,
  `name` VARCHAR(255),
  `country` ENUM('US', 'CO', 'TN') DEFAULT 'US',
  PRIMARY KEY(id),
  UNIQUE (email)
  );
