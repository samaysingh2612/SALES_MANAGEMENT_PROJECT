from products  import Product

products = [

# ---------------- Electronics ---------------- #

("Apple iPhone 16", "128GB 5G Smartphone", 79999, 35),
("Samsung Galaxy S25", "256GB Android Smartphone", 74999, 30),
("OnePlus 13", "Flagship Android Phone", 64999, 40),
("Xiaomi Redmi Note 14", "Budget Smartphone", 18999, 70),
("Realme GT 7", "Gaming Smartphone", 35999, 45),
("Apple MacBook Air M4", "13-inch Laptop", 114999, 20),
("Dell Inspiron 15", "Intel i5 Laptop", 62999, 25),
("HP Pavilion 14", "Ryzen 5 Laptop", 58999, 30),
("Lenovo ThinkPad E14", "Business Laptop", 68999, 20),
("Asus TUF Gaming F15", "Gaming Laptop", 79999, 15),
("Logitech Wireless Mouse", "Bluetooth Mouse", 999, 120),
("HP Wired Mouse", "USB Mouse", 499, 150),
("Logitech Keyboard", "Wireless Keyboard", 1999, 100),
("Boat Rockerz 450", "Wireless Headphones", 1499, 90),
("Sony WH-CH520", "Bluetooth Headphones", 4999, 50),
("JBL Flip 6", "Portable Bluetooth Speaker", 8999, 35),
("Samsung 27 Inch Monitor", "Full HD IPS Monitor", 14999, 25),
("Dell 24 Inch Monitor", "Office Monitor", 10999, 30),
("SanDisk 128GB Pendrive", "USB 3.0 Storage", 999, 200),
("Seagate 1TB HDD", "External Hard Disk", 4499, 60),

# ---------------- Home Appliances ---------------- #

("LG Refrigerator", "260L Double Door", 32999, 12),
("Samsung Washing Machine", "7kg Fully Automatic", 25999, 15),
("IFB Microwave Oven", "23L Convection", 11999, 20),
("Prestige Induction Cooktop", "2000W Induction", 2499, 50),
("Philips Mixer Grinder", "750W Kitchen Mixer", 3999, 40),
("Bajaj Ceiling Fan", "1200mm Ceiling Fan", 1899, 60),
("Usha Room Heater", "2000W Heater", 2499, 40),
("Kent RO Water Purifier", "RO+UV Purifier", 16999, 18),
("Voltas Air Conditioner", "1.5 Ton Split AC", 37999, 10),
("Dyson Vacuum Cleaner", "Cordless Vacuum", 34999, 8),

# ---------------- Fashion ---------------- #

("Men Cotton T-Shirt", "Round Neck Black", 699, 150),
("Women Kurti", "Cotton Printed Kurti", 899, 120),
("Men Blue Jeans", "Slim Fit Denim", 1499, 90),
("Women's Jeans", "Stretchable Denim", 1699, 80),
("Nike Running Shoes", "Sports Shoes", 4999, 60),
("Adidas Sneakers", "Casual Shoes", 5499, 55),
("Puma Hoodie", "Winter Wear", 2499, 45),
("Leather Wallet", "Genuine Leather", 999, 110),
("Titan Analog Watch", "Men's Watch", 3499, 35),
("Fastrack Sunglasses", "UV Protection", 1299, 70),

# ---------------- Grocery ---------------- #

("Basmati Rice 5kg", "Premium Rice", 699, 200),
("Aashirvaad Atta 10kg", "Whole Wheat Flour", 549, 180),
("Fortune Sunflower Oil 5L", "Cooking Oil", 899, 150),
("Tata Salt 1kg", "Iodized Salt", 28, 500),
("Amul Butter", "500g Butter", 275, 120),
("Nestle Milk Powder", "500g Pack", 349, 100),
("Tata Tea Gold", "1kg Tea", 599, 90),
("Bru Instant Coffee", "200g Coffee", 399, 80),
("Maggi Noodles Pack", "12 Pack Combo", 180, 250),
("Britannia Biscuits", "Family Pack", 60, 300),

# ---------------- Books ---------------- #

("Python Programming", "Programming Guide", 799, 40),
("Data Structures in C", "DSA Book", 699, 35),
("Machine Learning", "AI Textbook", 1299, 25),
("SQL for Beginners", "Database Guide", 499, 50),
("Operating System Concepts", "OS Book", 899, 30),
("Computer Networks", "Networking Book", 999, 25),
("DBMS Concepts", "Database Systems", 850, 30),
("GATE CSE Guide", "Preparation Book", 1200, 60),
("Java Programming", "Core Java", 699, 45),
("Web Development", "HTML CSS JS", 799, 40),

# ---------------- Sports ---------------- #

("Cricket Bat", "English Willow", 4999, 25),
("Football", "Size 5 Football", 999, 80),
("Badminton Racket", "Yonex Racket", 2499, 40),
("Table Tennis Bat", "Professional Bat", 1499, 35),
("Yoga Mat", "6mm Anti-slip", 899, 100),
("Dumbbell 5kg", "Gym Equipment", 1999, 60),
("Skipping Rope", "Fitness Rope", 299, 150),
("Cycling Helmet", "Safety Helmet", 1499, 40),
("Basketball", "Official Size", 1199, 50),
("Resistance Band", "Workout Band", 499, 120),

# ---------------- Beauty ---------------- #

("Nivea Face Wash", "Oil Control", 249, 120),
("Lakme Face Cream", "Moisturizer", 399, 90),
("Mamaearth Shampoo", "Hair Care", 499, 100),
("Dove Soap Pack", "Beauty Soap", 299, 150),
("Colgate Toothpaste", "200g Pack", 149, 200),
("Oral-B Toothbrush", "Soft Bristles", 120, 180),
("Gillette Razor", "Shaving Razor", 349, 120),
("Beardo Hair Wax", "Strong Hold", 299, 80),
("Body Lotion", "Moisturizing Lotion", 450, 90),
("Perfume", "Long Lasting Fragrance", 1499, 60),

# ---------------- Office ---------------- #

("Office Chair", "Ergonomic Chair", 7999, 20),
("Wooden Study Table", "Computer Table", 6499, 18),
("Notebook Pack", "A4 Notebook", 399, 150),
("Stapler Machine", "Office Stapler", 199, 100),
("Printer HP", "Inkjet Printer", 8999, 25),
("Canon Scanner", "Document Scanner", 10999, 15),
("Whiteboard", "Magnetic Board", 2499, 30),
("Calculator", "Scientific Calculator", 899, 80),
("Pen Drive 64GB", "USB Storage", 699, 150),
("Desk Lamp", "LED Study Lamp", 999, 70)

]

for product in products:
    Product.insert_product(*product)

print("100 Products Inserted Successfully!")