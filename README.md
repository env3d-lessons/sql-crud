# SQLite CRUD Operations in Python

This tutorial will guide you through performing CRUD (Create, Read, Update, Delete)
operations using Python’s built-in `sqlite3` library. We’ll build a simple database
to manage a user list using only `conn.execute`, and then implement a basic command-line
interface (CLI) for user interaction.

## Setting Up the Database

Start by importing the `sqlite3` library and connecting to an SQLite database. If the
database file doesn’t exist, SQLite will create it for you.

```python
import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect("users.db")

# Create the users table if it doesn’t exist
with conn:
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL
    )
    """)
print("Table created successfully!")
```

## Create (Insert) Users

You can insert data using the `INSERT INTO` SQL command. Always use parameterized queries to prevent SQL injection.

```python
# Insert sample data into the table
with conn:
    conn.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 25))
    conn.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Bob", 30))
print("Data inserted successfully!")
```

## Read (Query) Users

Retrieve data using the `SELECT` SQL command. You can iterate over the results returned by `conn.execute`.

```python
# Fetch all users from the table
print("Users in the database:")
for row in conn.execute("SELECT * FROM users"):
    print(row)
```

## Update User Records

Modify existing records using the `UPDATE` SQL command.

```python
# Update a user’s age
with conn:
    conn.execute("UPDATE users SET age = ? WHERE name = ?", (26, "Alice"))
print("Data updated successfully!")

# Verify the update
for row in conn.execute("SELECT * FROM users WHERE name = 'Alice'"):
    print("Updated record:", row)
```

## Delete Users

Remove records using the `DELETE` SQL command.

```python
# Delete a user
with conn:
    conn.execute("DELETE FROM users WHERE name = ?", ("Bob",))
print("Data deleted successfully!")

# Verify the deletion
print("Remaining users:")
for row in conn.execute("SELECT * FROM users"):
    print(row)
```

## Closing the Connection

Although we used a `with` block to manage the connection, explicitly closing it is a good practice.

```python
conn.close()
print("Connection closed.")
```

## Full Example: A Simple CRUD Command-Line App

To illustrate CRUD operations, let's implement a basic CLI where users can add, view, update, and delete records.

```python
import sqlite3
# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect("users.db")

"""Creates the users table if it doesn't exist."""
conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    age INTEGER NOT NULL
    )
""")

def create_user(name, age):
    """Create a new user."""
    cursor = conn.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
    return cursor.lastrowid  # Return the ID of the inserted row

def list_users():
    """Return a list of all users in the database."""
    return conn.execute("SELECT * FROM users").fetchall()

def update_user(uid, name, age):
    """Update a user's age."""
    cursor = conn.execute("UPDATE users SET name = ?, age = ? WHERE id = ?", (name, age, uid))
    return cursor.rowcount > 0  # True if at least one row was updated

def delete_user(uid):
    """Delete a user."""
    cursor = conn.execute("DELETE FROM users WHERE id = ?", (uid,)) # we need to provide a comma if we only have 1 value
    return cursor.rowcount > 0  # True if at least one row was deleted

def search_user(name):
    return conn.execute("SELECT * FROM users WHERE name = ?", (name,)).fetchall()

def main():
    while True:
        print("\nChoose an option:")
        print("1. Create user")
        print("2. List users")
        print("3. Update user")
        print("4. Delete user")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter name: ")
            age = int(input("Enter age: "))
            if create_user(name, age):
                print("User created successfully!")
        elif choice == "2":
            users = list_users()
            print("\nUsers in the database:")
            for user in users:
                print(user)
        elif choice == "3":
            id = int(input("Enter id of user to update: "))
            new_name = input("Enter new name: ")
            new_age = int(input("Enter new age: "))
            if update_user(id, new_name, new_age):
                print("User updated successfully!")
            else:
                print("User not found.")
        elif choice == "4":
            id = int(input("Enter id of user to delete: "))
            if delete_user(id):
                print("User deleted successfully!")
            else:
                print("User not found.")
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")
    
    conn.close()
    print("Database connection closed.")

if __name__ == "__main__":
    main()
```

### How to Use the CLI App
1. Save the script in a file called `app.py`
2. Run the script using the command `python app.py` from the terminal.
3. Select an option (Create, View, Update, Delete, Exit).
4. Follow the prompts to interact with the database.

This simple example demonstrates CRUD operations using SQLite in Python,
showing how easy it is to build a small database-driven application.

# Exercise

## Task 1: Follow the above instructions to create `app.py`.

## Task 2: Create a "search" function

Add a search function to the above code with the function signature

```python
# Similar to list_users(), but return only users that matches the name provided
def search_user(name):
```

Modify your UI to allow for a search option.

# Hand-in

Test your solution by executing the following command on the bash terminal:

```shell
$ pytest
```

When you are satisified, execute the following commands to submit:

```shell
$ git add -A
$ git commit -m 'submit'
$ git push
```
