-- GPTB2 Database Initialization Script - Task 3.4
-- Creates database, user, and initial table structure

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS gptb2_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Use the database
USE gptb2_db;

-- Create user if not exists (MySQL 8.0 syntax)
CREATE USER IF NOT EXISTS 'gptb2_user'@'%' IDENTIFIED BY 'gptb2_secure_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON gptb2_db.* TO 'gptb2_user'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, INDEX, ALTER ON gptb2_db.* TO 'gptb2_user'@'%';

-- Flush privileges
FLUSH PRIVILEGES;

-- Create equations table
CREATE TABLE IF NOT EXISTS equations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    a FLOAT NOT NULL,
    b FLOAT NOT NULL,
    c FLOAT NOT NULL,
    solution TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_created_at (created_at),
    INDEX idx_coefficients (a, b, c)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert sample data for testing
INSERT INTO equations (a, b, c, solution) VALUES 
(1, -5, 6, 'x₁ = 3.000000, x₂ = 2.000000'),
(1, -3, 2, 'x₁ = 2.000000, x₂ = 1.000000'),
(1, 0, -4, 'x₁ = 2.000000, x₂ = -2.000000'),
(1, -2, 1, 'x₁ = 1.000000, x₂ = 1.000000'),
(2, -4, 2, 'x₁ = 1.000000, x₂ = 1.000000')
ON DUPLICATE KEY UPDATE solution = VALUES(solution);

-- Show table structure
DESCRIBE equations;

-- Show sample data
SELECT * FROM equations LIMIT 5;