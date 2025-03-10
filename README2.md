## Python App using command line arguments

Instead of prompting the user within the python app, we can configure
our application to read options via command line arguments.  Here's
the version.  Simple replace the main() function as follows:

```python
def main():
    # Command-line interface
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <command> [arguments]")
        print("\nCommands:")
        print("  create <name> <age>       - Add a new user")
        print("  list                      - List all users")
        print("  update <id> <name> <age>  - Update user age")
        print("  delete <id>               - Delete a user")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "create" and len(sys.argv) == 4:
        if create_user(sys.argv[2], int(sys.argv[3])):
            print(f"User '{sys.argv[2]}' added successfully!")

    elif command == "list":
        users = list_users()
        if users:
            print("\nUsers in the database:")
            for row in users:
                print(row)
        else:
            print("No users found.")

    elif command == "update" and len(sys.argv) == 5:
        if update_user(int(sys.argv[2]), sys.argv[3], int(sys.argv[4])):
            print(f"User ID:'{sys.argv[2]}' updated successfully!")
        else:
            print(f"User ID:'{sys.argv[2]}' not found or update failed.")

    elif command == "delete" and len(sys.argv) == 3:
        if delete_user(sys.argv[2]):
            print(f"User ID:'{sys.argv[2]}' deleted successfully!")
        else:
            print(f"User ID:'{sys.argv[2]}' not found or deletion failed.")

    else:
        print("Invalid command or missing arguments. Run `python app.py` for usage info.")

    # Close the connection when done
    conn.close()
```


## Creating CRUD app via Web instead of Command Line

Here's a final varition of a CRUD app

```python
from fastapi import FastAPI, HTTPException
import sqlite3

app = FastAPI()

# Database connection
def get_db_connection():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row  # Allows fetching rows as dictionaries
    return conn

# Create table on startup
with get_db_connection() as conn:
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        age INTEGER NOT NULL
    )
    """)

# Create a user
@app.post("/users/")
def create_user(name: str, age: int):
    try:
        with get_db_connection() as conn:
            conn.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
        return {"message": f"User '{name}' added successfully!"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail=f"User '{name}' already exists.")

# Read all users
@app.get("/users/")
def list_users():
    with get_db_connection() as conn:
        users = conn.execute("SELECT * FROM users").fetchall()
    return {"users": [dict(user) for user in users]}

# Update a user (by id)
@app.put("/users/{id}")
def update_user(id: int, new_name: str = None, new_age: int = None):
    with get_db_connection() as conn:
        if new_name:
            conn.execute("UPDATE users SET name = ? WHERE id = ?", (new_name, id))
        if new_age is not None:
            conn.execute("UPDATE users SET age = ? WHERE id = ?", (new_age, id))
        if conn.total_changes == 0:
            raise HTTPException(status_code=404, detail=f"User with id '{id}' not found.")
    return {"message": f"User with id '{id}' updated successfully!"}

# Delete a user (by id)
@app.delete("/users/{id}")
def delete_user(id: int):
    with get_db_connection() as conn:
        conn.execute("DELETE FROM users WHERE id = ?", (id,))
        if conn.total_changes == 0:
            raise HTTPException(status_code=404, detail=f"User with id '{id}' not found.")
    return {"message": f"User with id '{id}' deleted successfully!"}
```

### How to run

1. Save the above into a file called `webapp.py`
2. First, issue the following on the command line
   ```
   pip install fastapi uvicorn
   ```
3. Run the application using the following:
   ```
   uvicorn webapp:app
   ```
4. If you are using github codespaces, you can access your app
   functions using /docs