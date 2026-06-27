import psycopg2
from Database import conn


class Product:

    # ---------------- CREATE TABLE ---------------- #
    @staticmethod
    def create_table():

        cur = None

        try:
            cur = conn.cursor()

            cur.execute("""
                CREATE TABLE IF NOT EXISTS products(
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    description TEXT,
                    price DECIMAL(10,2) NOT NULL,
                    quantity INTEGER NOT NULL
                )
            """)

            conn.commit()
            print("Products table created successfully.")

        except Exception as e:
            conn.rollback()
            print("Error:", e)

        finally:
            if cur:
                cur.close()

    # ---------------- INSERT PRODUCT ---------------- #
    @staticmethod
    def insert_product(name, description, price, quantity):

        cur = None

        try:
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO products(name, description, price, quantity)
                VALUES(%s,%s,%s,%s)
            """, (name, description, price, quantity))

            conn.commit()
            print("Product inserted successfully.")

        except Exception as e:
            conn.rollback()
            print("Error:", e)

        finally:
            if cur:
                cur.close()

    # ---------------- UPDATE PRODUCT ---------------- #
    @staticmethod
    def update_product(product_id, name=None, description=None,
                       price=None, quantity=None):

        cur = None

        try:
            cur = conn.cursor()

            cur.execute(
                "SELECT * FROM products WHERE id=%s",
                (product_id,)
            )

            product = cur.fetchone()

            if not product:
                print("Product not found.")
                return

            fields = []
            values = []

            if name:
                fields.append("name=%s")
                values.append(name)

            if description:
                fields.append("description=%s")
                values.append(description)

            if price is not None:
                fields.append("price=%s")
                values.append(price)

            if quantity is not None:
                fields.append("quantity=%s")
                values.append(quantity)

            if not fields:
                print("Nothing to update.")
                return

            values.append(product_id)

            query = f"""
                UPDATE products
                SET {', '.join(fields)}
                WHERE id=%s
            """

            cur.execute(query, values)

            conn.commit()

            print("Product updated successfully.")

        except Exception as e:
            conn.rollback()
            print("Error:", e)

        finally:
            if cur:
                cur.close()

    # ---------------- DELETE PRODUCT ---------------- #
    @staticmethod
    def delete_product(product_id):

        cur = None

        try:
            cur = conn.cursor()

            cur.execute(
                "DELETE FROM products WHERE id=%s",
                (product_id,)
            )

            if cur.rowcount == 0:
                print("Product not found.")
            else:
                conn.commit()
                print("Product deleted successfully.")

        except Exception as e:
            conn.rollback()
            print("Error:", e)

        finally:
            if cur:
                cur.close()

    # ---------------- VIEW ALL PRODUCTS ---------------- #
    @staticmethod
    def view_products():

        cur = None

        try:
            cur = conn.cursor()

            cur.execute("SELECT * FROM products")

            products = cur.fetchall()

            if not products:
                print("No products found.")
                return

            print("\n---------- PRODUCTS ----------")

            for product in products:
                print(product)

        except Exception as e:
            print("Error:", e)

        finally:
            if cur:
                cur.close()

    # ---------------- VIEW PRODUCT BY ID ---------------- #
    @staticmethod
    def view_product_by_id(product_id):

        cur = None

        try:
            cur = conn.cursor()

            cur.execute(
                "SELECT * FROM products WHERE id=%s",
                (product_id,)
            )

            product = cur.fetchone()

            if product:
                print(product)
            else:
                print("Product not found.")

        except Exception as e:
            print("Error:", e)

        finally:
            if cur:
                cur.close()

    # ---------------- MENU ---------------- #
    @staticmethod
    def product_menu():

        while True:

            print("\n========== PRODUCT MENU ==========")
            print("1. Create Product Table")
            print("2. Insert Product")
            print("3. Update Product")
            print("4. Delete Product")
            print("5. View All Products")
            print("6. View Product by ID")
            print("0. Exit")

            choice = input("\nEnter Choice : ")

            if choice == "1":

                Product.create_table()

            elif choice == "2":

                name = input("Enter Product Name : ")
                description = input("Enter Description : ")
                price = float(input("Enter Price : "))
                quantity = int(input("Enter Quantity : "))

                Product.insert_product(
                    name,
                    description,
                    price,
                    quantity
                )

            elif choice == "3":

                product_id = int(input("Enter Product ID : "))

                print("Leave blank if you don't want to update.")

                name = input("New Name : ")
                description = input("New Description : ")

                price_input = input("New Price : ")
                quantity_input = input("New Quantity : ")

                price = float(price_input) if price_input else None
                quantity = int(quantity_input) if quantity_input else None

                Product.update_product(
                    product_id,
                    name if name else None,
                    description if description else None,
                    price,
                    quantity
                )

            elif choice == "4":

                product_id = int(input("Enter Product ID : "))

                Product.delete_product(product_id)

            elif choice == "5":

                Product.view_products()

            elif choice == "6":

                product_id = int(input("Enter Product ID : "))

                Product.view_product_by_id(product_id)

            elif choice == "0":

                print("Thank You!")
                break

            else:

                print("Invalid Choice! Try Again.")


# ---------------- MAIN ---------------- #

if __name__ == "__main__":
    Product.product_menu()