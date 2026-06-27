import psycopg2
from Database import conn


class SaleItem:

    # ---------------- CREATE TABLE ---------------- #
    @staticmethod
    def create_table():

        cur = None

        try:

            cur = conn.cursor()

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

            print("Sale Items Table Created Successfully.")

        except Exception as e:

            conn.rollback()

            print("Error :", e)

        finally:

            if cur:
                cur.close()

    # ---------------- ADD ITEM ---------------- #

    @staticmethod
    def add_item(sale_id, product_id, quantity):

        cur = None

        try:

            cur = conn.cursor()

            # Check Product

            cur.execute("""
                SELECT price, quantity
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

            # Reduce Inventory

            cur.execute("""

                UPDATE products

                SET quantity=quantity-%s

                WHERE id=%s

            """, (
                quantity,
                product_id
            ))

            # Update Sale Total

            cur.execute("""

                UPDATE sales

                SET total_amount=(

                    SELECT
                    COALESCE(
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

            print("Item Added Successfully.")

        except Exception as e:

            conn.rollback()

            print("Error :", e)

        finally:

            if cur:
                cur.close()

    # ---------------- GET ITEMS ---------------- #

    @staticmethod
    def get_items_by_sale(sale_id):

        cur = None

        try:

            cur = conn.cursor()

            cur.execute("""

                SELECT

                    si.id,
                    p.name,
                    si.quantity,
                    si.price,
                    si.quantity*si.price

                FROM sale_items si

                JOIN products p

                ON si.product_id=p.id

                WHERE sale_id=%s

            """, (sale_id,))

            rows = cur.fetchall()

            return rows

        except Exception as e:

            print("Error :", e)

        finally:

            if cur:
                cur.close()

    # ---------------- VIEW ITEMS ---------------- #

    @staticmethod
    def view_sale_items(sale_id):

        items = SaleItem.get_items_by_sale(sale_id)

        if not items:

            print("No Items Found.")
            return

        print("\n========== SALE ITEMS ==========\n")

        total = 0

        print("{:<8}{:<20}{:<10}{:<10}{:<10}".format(
            "ID",
            "Product",
            "Qty",
            "Price",
            "Total"
        ))

        print("-"*65)

        for item in items:

            print("{:<8}{:<20}{:<10}{:<10}{:<10}".format(
                item[0],
                item[1],
                item[2],
                item[3],
                item[4]
            ))

            total += item[4]

        print("-"*65)

        print("Grand Total : ₹", total)

        return total

    # ---------------- DELETE ITEM ---------------- #

    @staticmethod
    def delete_item(item_id):

        cur = None

        try:

            cur = conn.cursor()

            cur.execute("""

                SELECT
                sale_id,
                product_id,
                quantity

                FROM sale_items

                WHERE id=%s

            """, (item_id,))

            item = cur.fetchone()

            if not item:

                print("Item Not Found.")
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

            # Update Bill

            cur.execute("""

                UPDATE sales

                SET total_amount=(

                    SELECT
                    COALESCE(
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

            print("Item Deleted Successfully.")

        except Exception as e:

            conn.rollback()

            print("Error :", e)

        finally:

            if cur:
                cur.close()

    # ---------------- MENU ---------------- #

    @staticmethod
    def sale_item_menu():

        while True:

            print("\n========== SALE ITEM MENU ==========")

            print("1. Create Table")
            print("2. Add Item")
            print("3. View Items")
            print("4. Delete Item")
            print("0. Exit")

            choice = input("\nEnter Choice : ")

            if choice == "1":

                SaleItem.create_table()

            elif choice == "2":

                sale = int(input("Sale ID : "))
                product = int(input("Product ID : "))
                qty = int(input("Quantity : "))

                SaleItem.add_item(
                    sale,
                    product,
                    qty
                )

            elif choice == "3":

                sale = int(input("Sale ID : "))

                SaleItem.view_sale_items(sale)

            elif choice == "4":

                item = int(input("Sale Item ID : "))

                SaleItem.delete_item(item)

            elif choice == "0":

                print("Thank You!")
                break

            else:

                print("Invalid Choice!")