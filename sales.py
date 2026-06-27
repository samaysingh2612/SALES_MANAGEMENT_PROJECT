import psycopg2
from Database import conn


class Sale:

    # ---------------- CREATE SALES TABLE ---------------- #
    @staticmethod
    def create_table():

        cur = None

        try:

            cur = conn.cursor()

            cur.execute("""
                CREATE TABLE IF NOT EXISTS sales(
                    id SERIAL PRIMARY KEY,
                    customer_id INTEGER NOT NULL
                        REFERENCES customers(id)
                        ON DELETE CASCADE,
                    date DATE NOT NULL,
                    total_amount DECIMAL(10,2) DEFAULT 0
                )
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS sale_items(
                    id SERIAL PRIMARY KEY,
                    sale_id INTEGER
                        REFERENCES sales(id)
                        ON DELETE CASCADE,
                    product_id INTEGER
                        REFERENCES products(id),
                    quantity INTEGER NOT NULL,
                    price DECIMAL(10,2) NOT NULL
                )
            """)

            conn.commit()

            print("Sales tables created successfully.")

        except Exception as e:

            conn.rollback()

            print("Error :", e)

        finally:

            if cur:
                cur.close()

    # ---------------- INSERT SALE ---------------- #

    @staticmethod
    def insert_sale(customer_id, date):

        cur = None

        try:

            cur = conn.cursor()

            cur.execute("""
                INSERT INTO sales(customer_id,date)
                VALUES(%s,%s)
                RETURNING id
            """, (customer_id, date))

            sale_id = cur.fetchone()[0]

            conn.commit()

            print(f"Sale Created Successfully. Sale ID : {sale_id}")

            return sale_id

        except Exception as e:

            conn.rollback()

            print("Error :", e)

        finally:

            if cur:
                cur.close()

    # ---------------- VIEW ALL SALES ---------------- #

    @staticmethod
    def view_sales():

        cur = None

        try:

            cur = conn.cursor()

            cur.execute("""
                SELECT *
                FROM sales
                ORDER BY id
            """)

            sales = cur.fetchall()

            if not sales:

                print("No Sales Found.")

                return

            print("\n========== SALES ==========\n")

            for sale in sales:

                print(sale)

        except Exception as e:

            print("Error :", e)

        finally:

            if cur:
                cur.close()

    # ---------------- VIEW SALE BY ID ---------------- #

    @staticmethod
    def view_sale_by_id(sale_id):

        cur = None

        try:

            cur = conn.cursor()

            cur.execute("""
                SELECT *
                FROM sales
                WHERE id=%s
            """, (sale_id,))

            sale = cur.fetchone()

            if sale:

                print(sale)

            else:

                print("Sale Not Found.")

        except Exception as e:

            print("Error :", e)

        finally:

            if cur:
                cur.close()

    # ---------------- UPDATE SALE ---------------- #

    @staticmethod
    def update_sale(sale_id, customer_id=None, date=None):

        cur = None

        try:

            cur = conn.cursor()

            cur.execute(
                "SELECT * FROM sales WHERE id=%s",
                (sale_id,)
            )

            if not cur.fetchone():

                print("Sale Not Found.")

                return

            fields = []
            values = []

            if customer_id:

                fields.append("customer_id=%s")
                values.append(customer_id)

            if date:

                fields.append("date=%s")
                values.append(date)

            if not fields:

                print("Nothing To Update.")

                return

            values.append(sale_id)

            query = f"""
                UPDATE sales
                SET {', '.join(fields)}
                WHERE id=%s
            """

            cur.execute(query, values)

            conn.commit()

            print("Sale Updated Successfully.")

        except Exception as e:

            conn.rollback()

            print("Error :", e)

        finally:

            if cur:
                cur.close()

    # ---------------- DELETE SALE ---------------- #

    @staticmethod
    def delete_sale(sale_id):

        cur = None

        try:

            cur = conn.cursor()

            cur.execute("""
                DELETE FROM sales
                WHERE id=%s
            """, (sale_id,))

            if cur.rowcount == 0:

                print("Sale Not Found.")

            else:

                conn.commit()

                print("Sale Deleted Successfully.")

        except Exception as e:

            conn.rollback()

            print("Error :", e)

        finally:

            if cur:
                cur.close()

    # ---------------- ADD SALE ITEM ---------------- #

    @staticmethod
    def add_sale_item(sale_id, product_id, quantity):

        cur = None

        try:

            cur = conn.cursor()

            # Check Product

            cur.execute("""
                SELECT price,quantity
                FROM products
                WHERE id=%s
            """, (product_id,))

            product = cur.fetchone()

            if not product:

                print("Product Not Found.")

                return

            price = product[0]
            stock = product[1]

            if quantity > stock:

                print("Insufficient Stock.")

                return

            # Insert Item

            cur.execute("""
                INSERT INTO sale_items
                (sale_id,product_id,quantity,price)

                VALUES(%s,%s,%s,%s)
            """, (
                sale_id,
                product_id,
                quantity,
                price
            ))

            # Update Inventory

            cur.execute("""
                UPDATE products

                SET quantity=quantity-%s

                WHERE id=%s
            """, (
                quantity,
                product_id
            ))

            # Update Bill

            cur.execute("""

                UPDATE sales

                SET total_amount=(

                    SELECT COALESCE(
                    SUM(quantity*price),0)

                    FROM sale_items

                    WHERE sale_id=%s

                )

                WHERE id=%s

            """, (
                sale_id,
                sale_id
            ))

            conn.commit()

            print("Sale Item Added Successfully.")

        except Exception as e:

            conn.rollback()

            print("Error :", e)

        finally:

            if cur:
                cur.close()

    # ---------------- REMOVE SALE ITEM ---------------- #

    @staticmethod
    def remove_sale_item(item_id):
        
    

        cur = None

        try:

            cur = conn.cursor()

            cur.execute("""

                SELECT sale_id,
                       product_id,
                       quantity

                FROM sale_items

                WHERE id=%s

            """, (item_id,))

            item = cur.fetchone()

            if not item:

                print("Sale Item Not Found.")

                return

            sale_id = item[0]
            product_id = item[1]
            qty = item[2]

            # Restore Stock

            cur.execute("""

                UPDATE products

                SET quantity=quantity+%s

                WHERE id=%s

            """, (
                qty,
                product_id
            ))

            # Delete Item

            cur.execute("""

                DELETE FROM sale_items

                WHERE id=%s

            """, (item_id,))

            # Recalculate Total

            cur.execute("""

                UPDATE sales

                SET total_amount=(

                    SELECT COALESCE(
                    SUM(quantity*price),0)

                    FROM sale_items

                    WHERE sale_id=%s

                )

                WHERE id=%s

            """, (
                sale_id,
                sale_id
            ))

            conn.commit()

            print("Sale Item Removed Successfully.")

        except Exception as e:

            conn.rollback()

            print("Error :", e)

        finally:

            if cur:
                cur.close()
                # ---------------- GENERATE BILL ---------------- #
    @staticmethod
    def generate_bill(sale_id):

        cur = None

        try:
            cur = conn.cursor()

            # Sale + Customer Details
            cur.execute("""
                SELECT s.id,
                       s.date,
                       c.name,
                       c.contact,
                       s.total_amount
                FROM sales s
                JOIN customers c
                ON s.customer_id = c.id
                WHERE s.id=%s
            """, (sale_id,))

            sale = cur.fetchone()

            if not sale:
                print("Sale Not Found.")
                return

            print("\n" + "=" * 60)
            print("                E-COMMERCE BILL")
            print("=" * 60)
            print(f"Sale ID      : {sale[0]}")
            print(f"Date         : {sale[1]}")
            print(f"Customer     : {sale[2]}")
            print(f"Contact      : {sale[3]}")
            print("-" * 60)

            cur.execute("""
                SELECT
                    p.name,
                    si.quantity,
                    si.price,
                    si.quantity * si.price AS subtotal
                FROM sale_items si
                JOIN products p
                ON si.product_id = p.id
                WHERE si.sale_id=%s
            """, (sale_id,))

            items = cur.fetchall()

            print("{:<20}{:<10}{:<10}{:<10}".format(
                "Product", "Qty", "Price", "Total"
            ))

            print("-" * 60)

            for item in items:
                print("{:<20}{:<10}{:<10}{:<10}".format(
                    item[0],
                    item[1],
                    item[2],
                    item[3]
                ))

            print("-" * 60)
            print(f"Grand Total : ₹ {sale[4]}")
            print("=" * 60)

            return sale[4]

        except Exception as e:
            print("Error :", e)

        finally:
            if cur:
                cur.close()

    # ---------------- SALES BETWEEN DATES ---------------- #
    @staticmethod
    def get_total_sales_by_date(start_date, end_date):

        cur = None

        try:
            cur = conn.cursor()

            cur.execute("""
                SELECT COALESCE(SUM(total_amount),0)
                FROM sales
                WHERE date BETWEEN %s AND %s
            """, (start_date, end_date))

            total = cur.fetchone()[0]

            print(f"\nTotal Sales = ₹ {total}")

            return total

        except Exception as e:
            print("Error :", e)

        finally:
            if cur:
                cur.close()

    # ---------------- TOP SELLING PRODUCTS ---------------- #
    @staticmethod
    def get_top_selling_products():

        cur = None

        try:
            cur = conn.cursor()

            cur.execute("""
                SELECT
                    p.name,
                    SUM(si.quantity) AS total_quantity
                FROM sale_items si
                JOIN products p
                ON si.product_id = p.id
                GROUP BY p.name
                ORDER BY total_quantity DESC
                LIMIT 5
            """)

            rows = cur.fetchall()

            print("\n====== TOP SELLING PRODUCTS ======\n")

            for i, row in enumerate(rows, start=1):
                print(f"{i}. {row[0]}  ---> {row[1]} Units")

        except Exception as e:
            print("Error :", e)

        finally:
            if cur:
                cur.close()

    # ---------------- SALES BY CUSTOMER ---------------- #
    @staticmethod
    def get_sales_by_customer(customer_id):

        cur = None

        try:
            cur = conn.cursor()

            cur.execute("""
                SELECT
                    id,
                    date,
                    total_amount
                FROM sales
                WHERE customer_id=%s
                ORDER BY date
            """, (customer_id,))

            rows = cur.fetchall()

            if not rows:
                print("No Sales Found.")
                return

            print("\n====== CUSTOMER SALES ======\n")

            for sale in rows:
                print(sale)

            return rows

        except Exception as e:
            print("Error :", e)

        finally:
            if cur:
                cur.close()

    # ---------------- DAILY SALES REPORT ---------------- #
    @staticmethod
    def daily_sales_report(date):

        cur = None

        try:
            cur = conn.cursor()

            cur.execute("""
                SELECT
                    COUNT(*),
                    COALESCE(SUM(total_amount),0)
                FROM sales
                WHERE date=%s
            """, (date,))

            report = cur.fetchone()

            print("\n====== DAILY REPORT ======")
            print("Date          :", date)
            print("Total Bills   :", report[0])
            print("Total Revenue : ₹", report[1])

        except Exception as e:
            print("Error :", e)

        finally:
            if cur:
                cur.close()

    # ---------------- MONTHLY SALES REPORT ---------------- #
    @staticmethod
    def monthly_sales_report(month):

        cur = None

        try:
            cur = conn.cursor()

            cur.execute("""
                SELECT
                    COUNT(*),
                    COALESCE(SUM(total_amount),0)
                FROM sales
                WHERE TO_CHAR(date,'YYYY-MM')=%s
            """, (month,))

            report = cur.fetchone()

            print("\n====== MONTHLY REPORT ======")
            print("Month         :", month)
            print("Total Bills   :", report[0])
            print("Total Revenue : ₹", report[1])

        except Exception as e:
            print("Error :", e)

        finally:
            if cur:
                cur.close()

    # ---------------- SALE MENU ---------------- #
    @staticmethod
    def sale_menu():

        while True:

            print("\n========== SALES MENU ==========")
            print("1. Create Sales Tables")
            print("2. Create New Sale")
            print("3. Add Product To Sale")
            print("4. Remove Product From Sale")
            print("5. View All Sales")
            print("6. View Sale By ID")
            print("7. Update Sale")
            print("8. Delete Sale")
            print("9. Generate Bill")
            print("10. Sales Between Dates")
            print("11. Top Selling Products")
            print("12. Customer Purchase History")
            print("13. Daily Sales Report")
            print("14. Monthly Sales Report")
            print("0. Exit")

            choice = input("\nEnter Choice : ")

            if choice == "1":
                Sale.create_table()

            elif choice == "2":
                customer = int(input("Customer ID : "))
                date = input("Date (YYYY-MM-DD) : ")
                Sale.insert_sale(customer, date)

            elif choice == "3":
                sale = int(input("Sale ID : "))
                product = int(input("Product ID : "))
                qty = int(input("Quantity : "))
                Sale.add_sale_item(sale, product, qty)

            elif choice == "4":
                item = int(input("Sale Item ID : "))
                Sale.remove_sale_item(item)

            elif choice == "5":
                Sale.view_sales()

            elif choice == "6":
                sale = int(input("Sale ID : "))
                Sale.view_sale_by_id(sale)

            elif choice == "7":
                sale = int(input("Sale ID : "))
                customer = input("New Customer ID (Blank to Skip): ")
                date = input("New Date (Blank to Skip): ")

                Sale.update_sale(
                    sale,
                    int(customer) if customer else None,
                    date if date else None
                )

            elif choice == "8":
                sale = int(input("Sale ID : "))
                Sale.delete_sale(sale)

            elif choice == "9":
                sale = int(input("Sale ID : "))
                Sale.generate_bill(sale)

            elif choice == "10":
                start = input("Start Date : ")
                end = input("End Date : ")
                Sale.get_total_sales_by_date(start, end)

            elif choice == "11":
                Sale.get_top_selling_products()

            elif choice == "12":
                customer = int(input("Customer ID : "))
                Sale.get_sales_by_customer(customer)

            elif choice == "13":
                date = input("Enter Date : ")
                Sale.daily_sales_report(date)

            elif choice == "14":
                month = input("Enter Month (YYYY-MM): ")
                Sale.monthly_sales_report(month)

            elif choice == "0":
                print("Thank You!")
                break

            else:
                print("Invalid Choice!")