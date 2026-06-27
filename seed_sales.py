from sales import Sale
import random
from datetime import date, timedelta

today = date.today()

for i in range(100):

    customer_id = random.randint(1, 100)

    random_days = random.randint(0, 180)

    sale_date = today - timedelta(days=random_days)

    Sale.insert_sale(
        customer_id,
        sale_date
    )

print(" 100 Sales Inserted Successfully!")