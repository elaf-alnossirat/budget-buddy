mysql> CREATE DATABASE budget_buddy;
Query OK, 1 row affected (0.01 sec)

mysql>
mysql> USE budget_buddy;
Database changed
mysql>
mysql> CREATE TABLE users (
    ->     id INT AUTO_INCREMENT PRIMARY KEY,
    ->     first_name VARCHAR(50) NOT NULL,
    ->     last_name VARCHAR(50) NOT NULL,
    ->     email VARCHAR(100) NOT NULL UNIQUE,
    ->     password_hash VARCHAR(255) NOT NULL
    -> );
Query OK, 0 rows affected (0.05 sec)

mysql>
mysql> CREATE TABLE transactions (
    ->     id INT AUTO_INCREMENT PRIMARY KEY,
    ->     user_id INT NOT NULL,
    ->     reference VARCHAR(100) NOT NULL,
    ->     description TEXT,
    ->     amount DECIMAL(10, 2) NOT NULL,
    ->     date DATE NOT NULL,
    ->     type ENUM('deposit', 'withdrawal', 'transfer') NOT NULL,
    ->     category ENUM('leisure', 'meal', 'bribe') NOT NULL,
    ->     FOREIGN KEY (user_id) REFERENCES users(id)
    -> );
Query OK, 0 rows affected (0.04 sec)

mysql> ALTER TABLE transactions MODIFY COLUMN category VARCHAR(50);
Query OK, 0 rows affected (48.08 sec)
Records: 0  Duplicates: 0  Warnings: 0

mysql> DESCRIBE transactions;
+-------------+-----------------------------------------+------+-----+---------+----------------+
| Field       | Type                                    | Null | Key | Default | Extra          |
+-------------+-----------------------------------------+------+-----+---------+----------------+
| id          | int                                     | NO   | PRI | NULL    | auto_increment |
| user_id     | int                                     | NO   | MUL | NULL    |                |
| reference   | varchar(100)                            | NO   |     | NULL    |                |
| description | text                                    | YES  |     | NULL    |                |
| amount      | decimal(10,2)                           | NO   |     | NULL    |                |
| date        | date                                    | NO   |     | NULL    |                |
| type        | enum('deposit','withdrawal','transfer') | NO   |     | NULL    |                |
| category    | varchar(50)                             | YES  |     | NULL    |                |
+-------------+-----------------------------------------+------+-----+---------+----------------+
8 rows in set (0.02 sec)

mysql>
mysql> DESCRIBE transactions;DESCRIBE transactions;DESCRIBE transactions;DESCRIBE transactions;DESCRIBE transactions;   