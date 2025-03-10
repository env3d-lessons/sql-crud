import sqlite3
# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect("users.db", isolation_level=None)

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