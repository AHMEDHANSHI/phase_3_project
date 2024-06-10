import sqlite3

class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

class Supplier:
    def __init__(self, name):
        self.name = name

class ProductSupplier:
    def __init__(self, product_id, supplier_id):
        self.product_id = product_id
        self.supplier_id = supplier_id

def create_tables():
    connection = sqlite3.connect("inventory.db")
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS products(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   price REAL,
                   quantity INTEGER
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS suppliers (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS product_supplier (
                   product_id INTEGER,
                   supplier_id INTEGER,
                   FOREIGN KEY (product_id) REFERENCES products(id),
                   FOREIGN KEY (supplier_id) REFERENCES suppliers(id),
                   PRIMARY KEY (product_id, supplier_id)
    )''')

    connection.commit()
    connection.close()

create_tables()

class InventoryDB:
    def __init__(self):
        self.connection = sqlite3.connect('inventory.db')
        self.cursor = self.connection.cursor()

    def add_product(self, product):
        self.cursor.execute('INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)',
                            (product.name, product.price, product.quantity))
        self.connection.commit()

    def add_supplier(self, supplier):
        self.cursor.execute('INSERT INTO suppliers (name) VALUES (?)', (supplier.name,))
        self.connection.commit()

    def product_exists(self, product_id):
        self.cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        return self.cursor.fetchone() is not None

    def supplier_exists(self, supplier_id):
        self.cursor.execute('SELECT * FROM suppliers WHERE id = ?', (supplier_id,))
        return self.cursor.fetchone() is not None

    def assign_supplier_to_product(self, product_supplier):
        if self.product_exists(product_supplier.product_id) and self.supplier_exists(product_supplier.supplier_id):
            self.cursor.execute('INSERT INTO product_supplier (product_id, supplier_id) VALUES (?, ?)',
                                (product_supplier.product_id, product_supplier.supplier_id))
            self.connection.commit()
            print(f"Supplier {product_supplier.supplier_id} assigned to product {product_supplier.product_id}.")
        else:
            print("Product or supplier does not exist.")

    def list_products(self):
        self.cursor.execute("SELECT * FROM products")
        return self.cursor.fetchall()

    def list_suppliers(self):
        self.cursor.execute("SELECT * FROM suppliers")
        return self.cursor.fetchall()

    def delete_product_by_id(self, product_id):
        if self.product_exists(product_id):
            self.cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
            self.connection.commit()
            print(f"Product with ID {product_id} deleted.")
        else:
            print("Product does not exist.")

    def delete_supplier_by_id(self, supplier_id):
        if self.supplier_exists(supplier_id):
            self.cursor.execute('DELETE FROM suppliers WHERE id = ?', (supplier_id,))
            self.connection.commit()
            print(f"Supplier with ID {supplier_id} deleted.")
        else:
            print("Supplier does not exist.")

    def find_product_by_id(self, product_id):
        if self.product_exists(product_id):
            self.cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
            return self.cursor.fetchone()
        else:
            print("Product does not exist.")

    def find_supplier_by_id(self, supplier_id):
        if self.supplier_exists(supplier_id):
            self.cursor.execute('SELECT * FROM suppliers WHERE id = ?', (supplier_id,))
            return self.cursor.fetchone()
        else:
            print("Supplier does not exist.")

    def close(self):
        self.connection.close()

def main():
    db = InventoryDB()

    while True:
        print("\n1. Add Product")
        print("2. Add Supplier")
        print("3. Assign Supplier to Product")
        print("4. List Products")
        print("5. List Suppliers")
        print("6. Delete Product by ID")
        print("7. Delete Supplier by ID")
        print("8. Find Product by ID")
        print("9. Find Supplier by ID")
        print("10. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            name = input("Enter product name: ")
            price = float(input("Enter product price: "))
            quantity = int(input("Enter product quantity: "))
            product = Product(name, price, quantity)
            db.add_product(product)
        elif choice == '2':
            name = input("Enter supplier name: ")
            supplier = Supplier(name)
            db.add_supplier(supplier)
        elif choice == '3':
            product_id = int(input("Enter product ID: "))
            supplier_id = int(input("Enter supplier ID: "))
            product_supplier = ProductSupplier(product_id, supplier_id)
            db.assign_supplier_to_product(product_supplier)
        elif choice == '4':
            products = db.list_products()
            for product in products:
                print(f"Product ID: {product[0]}, Name: {product[1]}, Price: {product[2]}, Quantity: {product[3]}")
        elif choice == '5':
            suppliers = db.list_suppliers()
            for supplier in suppliers:
                print(f"Supplier ID: {supplier[0]}, Name: {supplier[1]}")
        elif choice == '6':
            product_id = int(input("Enter product ID to delete: "))
            db.delete_product_by_id(product_id)
        elif choice == '7':
            supplier_id = int(input("Enter supplier ID to delete: "))
            db.delete_supplier_by_id(supplier_id)
        elif choice == '8':
            product_id = int(input("Enter product ID to find: "))
            print(db.find_product_by_id(product_id))
        elif choice == '9':
            supplier_id = int(input("Enter supplier ID to find: "))
            print(db.find_supplier_by_id(supplier_id))
        elif choice == '10':
            db.close()
            break
        else:
            print("Invalid choice. Please try again")

if __name__ == '__main__':
    main()
