CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    gender VARCHAR(10),
    language VARCHAR(50),
    phone VARCHAR(15),
    email VARCHAR(120) UNIQUE,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
