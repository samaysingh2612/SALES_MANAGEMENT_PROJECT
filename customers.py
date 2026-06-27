import psycopg2
from Database import conn


class Customer:

    # ---------------- CREATE TABLE ---------------- #
    @staticmethod
    def create_table():
        cur = None
        try:
            cur = conn.cursor()

            cur.execute("""
                CREATE TABLE IF NOT EXISTS customers(
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    contact VARCHAR(100) NOT NULL
                )
            """)

            conn.commit()
            print("Customers table created successfully.")

        except Exception as e:
            conn.rollback()
            print("Error:", e)

        finally:
            if cur:
                cur.close()

    # ---------------- INSERT CUSTOMER ---------------- #
    @staticmethod
    def insert_customer(name, contact):

        cur = None

        try:
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO customers(name, contact)
                VALUES (%s, %s)
            """, (name, contact))

            conn.commit()
            print("Customer inserted successfully.")

        except Exception as e:
            conn.rollback()
            print("Error:", e)

        finally:
            if cur:
                cur.close()

    # ---------------- UPDATE CUSTOMER ---------------- #
    @staticmethod
    def update_customer(customer_id, name=None, contact=None):

        cur = None

        try:
            cur = conn.cursor()

            cur.execute(
                "SELECT * FROM customers WHERE id=%s",
                (customer_id,)
            )

            customer = cur.fetchone()

            if not customer:
                print("Customer not found.")
                return

            fields = []
            values = []

            if name:
                fields.append("name=%s")
                values.append(name)

            if contact:
                fields.append("contact=%s")
                values.append(contact)

            if not fields:
                print("Nothing to update.")
                return

            values.append(customer_id)

            query = f"""
                UPDATE customers
                SET {', '.join(fields)}
                WHERE id=%s
            """

            cur.execute(query, values)

            conn.commit()

            print("Customer updated successfully.")

        except Exception as e:
            conn.rollback()
            print("Error:", e)

        finally:
            if cur:
                cur.close()

    # ---------------- DELETE CUSTOMER ---------------- #
    @staticmethod
    def delete_customer(customer_id):

        cur = None

        try:
            cur = conn.cursor()

            cur.execute(
                "DELETE FROM customers WHERE id=%s",
                (customer_id,)
            )

            if cur.rowcount == 0:
                print("Customer not found.")
            else:
                conn.commit()
                print("Customer deleted successfully.")

        except Exception as e:
            conn.rollback()
            print("Error:", e)

        finally:
            if cur:
                cur.close()

    # ---------------- VIEW ALL CUSTOMERS ---------------- #
    @staticmethod
    def view_customers():

        cur = None

        try:
            cur = conn.cursor()

            cur.execute("SELECT * FROM customers")

            customers = cur.fetchall()

            if not customers:
                print("No customers found.")
                return

            print("\n------ Customers ------")

            for customer in customers:
                print(customer)

        except Exception as e:
            print("Error:", e)

        finally:
            if cur:
                cur.close()

    # ---------------- VIEW CUSTOMER BY ID ---------------- #
    @staticmethod
    def view_customer_by_id(customer_id):

        cur = None

        try:
            cur = conn.cursor()

            cur.execute(
                "SELECT * FROM customers WHERE id=%s",
                (customer_id,)
            )

            customer = cur.fetchone()

            if customer:
                print(customer)
            else:
                print("Customer not found.")

        except Exception as e:
            print("Error:", e)

        finally:
            if cur:
                cur.close()

    # ---------------- GET SALES OF CUSTOMER ---------------- #
    @staticmethod
    def get_sales_by_customer(customer_id):

        cur = None

        try:
            cur = conn.cursor()

            cur.execute("""
                SELECT
                    s.id,
                    s.date,
                    s.total_amount
                FROM sales s
                JOIN customers c
                ON s.customer_id = c.id
                WHERE c.id = %s
            """, (customer_id,))

            sales = cur.fetchall()

            if not sales:
                print("No sales found.")
                return

            print("\n------ Sales ------")

            for sale in sales:
                print(sale)

        except Exception as e:
            print("Error:", e)

        finally:
            if cur:
                cur.close()

    # ---------------- SEARCH CUSTOMER ---------------- #
    @staticmethod
    def search_customer(name):

        cur = None

        try:
            cur = conn.cursor()

            cur.execute("""
                SELECT *
                FROM customers
                WHERE name ILIKE %s
            """, ('%' + name + '%',))

            customers = cur.fetchall()

            if not customers:
                print("Customer not found.")
                return

            for customer in customers:
                print(customer)

        except Exception as e:
            print("Error:", e)

        finally:
            if cur:
                cur.close()

    # ---------------- MENU ---------------- #
    @staticmethod
    def customer_menu():

        while True:

            print("\n========== CUSTOMER MENU ==========")
            print("1. Create Customer Table")
            print("2. Insert Customer")
            print("3. Update Customer")
            print("4. Delete Customer")
            print("5. View All Customers")
            print("6. View Customer by ID")
            print("7. Get Sales by Customer")
            print("8. Search Customer")
            print("0. Exit")

            choice = input("\nEnter Choice : ")

            if choice == "1":
                Customer.create_table()

            elif choice == "2":

                name = input("Enter Name : ")
                contact = input("Enter Contact : ")

                Customer.insert_customer(name, contact)

            elif choice == "3":

                customer_id = int(input("Enter Customer ID : "))

                print("Leave blank if you don't want to update.")

                name = input("New Name : ")
                contact = input("New Contact : ")

                Customer.update_customer(
                    customer_id,
                    name if name else None,
                    contact if contact else None
                )

            elif choice == "4":

                customer_id = int(input("Enter Customer ID : "))
                Customer.delete_customer(customer_id)

            elif choice == "5":

                Customer.view_customers()

            elif choice == "6":

                customer_id = int(input("Enter Customer ID : "))
                Customer.view_customer_by_id(customer_id)

            elif choice == "7":

                customer_id = int(input("Enter Customer ID : "))
                Customer.get_sales_by_customer(customer_id)

            elif choice == "8":

                name = input("Enter Customer Name : ")
                Customer.search_customer(name)

            elif choice == "0":

                print("Thank You!")
                break

            else:
                print("Invalid Choice! Try Again.")


# ---------------- MAIN ---------------- #

if __name__ == "__main__":
    Customer.customer_menu()