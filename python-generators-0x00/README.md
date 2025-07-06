# 🎯 Objective

Create a generator that streams rows from an SQL database one by one.

# 📝 Instructions

1. **Write a Python script named `seed.py` that:**
   - Sets up a MySQL database called `ALX_prodev`.
   - Creates a table `user_data` with the following fields:
     - `user_id` (Primary Key, UUID, Indexed)
     - `name` (VARCHAR, NOT NULL)
     - `email` (VARCHAR, NOT NULL)
     - `age` (DECIMAL, NOT NULL)
   - Populates the database with sample data from `user_data.csv`.

# 🛠️ Prototypes

Implement the following functions in your script:

- `def connect_db()`: Connects to the MySQL database server.
- `def create_database(connection)`: Creates the database `ALX_prodev` if it does not exist.
- `def connect_to_prodev()`: Connects to the `ALX_prodev` database in MySQL.
- `def create_table(connection)`: Creates the table `user_data` if it does not exist, with the required fields.
- `def insert_data(connection, data)`: Inserts data into the database if it does not already exist.

# 📦 Sample Data

- Use the provided `user_data.csv` file to seed the database with initial data.

# 🚀 Usage

1. Ensure you have MySQL running and accessible.
2. Place `user_data.csv` in the same directory as `seed.py`.
3. Run the script:
   ```bash
   python3 seed.py
   ```
4. The script will set up the database, create the table, and populate it with data.

# 💡 Notes

- Make sure to install the required Python packages (e.g., `mysql-connector-python`).
- Handle exceptions and edge cases (e.g., duplicate entries, connection errors).
- Use UUIDs for `user_id`.

# 🙌 Credits

- Task by ALX.
