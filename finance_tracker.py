import mysql.connector
#Tried to ckeck with cmd commands to initialise git and add to it
# Connect to MySQL
conn = mysql.connector.connect(
    host="127.0.0.1",    # MySQL host (change if necessary)
    user="root",         # Your MySQL username
    password="8978714898",  # Your MySQL password
    database="finance_tracker"  # The database you created
)
cursor = conn.cursor()

# Check connection
if conn.is_connected():
    print("Successfully connected to the database!")
else:
    print("Failed to connect.")

# Function to add a new transaction
def add_transaction():
    print("\n--- Add New Transaction ---")
    category_name = input("Enter category (e.g., Food, Entertainment, Rent): ")
    amount = float(input("Enter amount (use negative for expense, positive for income): "))
    date = input("Enter date (YYYY-MM-DD): ")
    description = input("Enter description (optional): ")

    try:
        # Get category_id based on category_name
        cursor.execute("SELECT id FROM categories WHERE name = %s", (category_name,))
        category = cursor.fetchone()

        if category:
            category_id = category[0]  # Get category ID
            # Insert the transaction into the transactions table
            cursor.execute("""
                INSERT INTO transactions (category_id, amount, date, description)
                VALUES (%s, %s, %s, %s)
            """, (category_id, amount, date, description))

            # Commit the transaction
            conn.commit()
            print(f"Transaction added: {category_name} - {amount} on {date}")
        else:
            print(f"Category '{category_name}' not found. Please add it first.")
    
    except Exception as e:
        print(f"Error occurred while adding transaction: {e}")

# Function to view transactions by category
def view_transactions_by_category():
    print("\n--- View Transactions by Category ---")
    category_name = input("Enter category (e.g., Food, Entertainment, Rent): ")
    
    try:
        cursor.execute("""
            SELECT t.amount, t.date, t.description
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            WHERE c.name = %s
        """, (category_name,))
        
        transactions = cursor.fetchall()

        if transactions:
            for transaction in transactions:
                print(f"Amount: {transaction[0]}, Date: {transaction[1]}, Description: {transaction[2]}")
        else:
            print(f"No transactions found for category: {category_name}")
    
    except Exception as e:
        print(f"Error occurred while viewing transactions: {e}")

# Function to view spending summary by category
def spending_summary():
    print("\n--- Spending Summary by Category ---")
    
    try:
        cursor.execute("""
            SELECT c.name, SUM(t.amount) AS total_spent
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            GROUP BY c.name
        """)

        categories_summary = cursor.fetchall()

        if categories_summary:
            for category in categories_summary:
                print(f"Category: {category[0]}, Total Spent: {category[1]}")
        else:
            print("No spending data available.")
    
    except Exception as e:
        print(f"Error occurred while generating summary: {e}")

# Main menu function to interact with the user
def main_menu():
    while True:
        print("\n--- Personal Finance Tracker ---")
        print("1. Add a Transaction")
        print("2. View Transactions by Category")
        print("3. View Spending Summary")
        print("4. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            add_transaction()
        elif choice == '2':
            view_transactions_by_category()
        elif choice == '3':
            spending_summary()
        elif choice == '4':
            print("Exiting...")
            cursor.close()
            conn.close()
            break
        else:
            print("Invalid choice, please try again.")

# Run the main menu
if __name__ == "__main__":
    main_menu()
