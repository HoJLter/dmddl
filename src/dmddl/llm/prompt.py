
prompt = '''
Task: Generate an SQL INSERT script from a provided DDL schema, ensuring:

Dependency Ordering: Tables are populated in the correct order (e.g., countries before cities).

Customizable Volume: Allow adjusting the average number of records per table (e.g., "10 records for small tables, 100 for large ones").

Logical Data: Ensure realistic values (e.g., valid emails, dates within ranges) and consistent relationships (e.g., user_id in orders must exist in users).

Variety: Randomize data where possible (e.g., names, prices, timestamps) while keeping constraints valid.

Output Format:

Plain SQL script with INSERT statements in dependency-safe order.

Comments marking table sections (e.g., -- TABLE: users (20 records)).

Example Input DDL:

CREATE TABLE users (
  user_id INT PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  email VARCHAR(100) CHECK (email LIKE '%@%.%')
);

CREATE TABLE orders (
  order_id INT PRIMARY KEY,
  user_id INT REFERENCES users(user_id),
  order_date DATE DEFAULT CURRENT_DATE
);

Example Output (for 5 users and 15 orders):

-- TABLE: users (5 records)
INSERT INTO users (user_id, username, email) VALUES 
(1, 'john_doe', 'john@example.com'),
(2, 'jane_smith', 'jane@test.org'),
...;

-- TABLE: orders (15 records)
INSERT INTO orders (order_id, user_id, order_date) VALUES 
(1, 1, '2023-01-01'),
(2, 2, '2023-01-02'),
...;
Additional Rules:

For large tables, use batch INSERT (e.g., 100 rows/statement).

Skip circular dependencies or suggest fixes.

Add -- WARNING comments for potential issues (e.g., missing ON DELETE CASCADE).

Average records per table: [Small: 15 | Medium: 40 | Large: 60]

User Input:
'''