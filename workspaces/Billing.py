### 2. Core Logic (`billingsystem.py`)

#This module contains the core business logic of the application. It includes functions for managing the menu, handling orders, calculating bills, and generating reports.

#```python
# billingsystem.py

from database import create_connection

def add_menu_item(name, price, category):
    """Add a new item to the menu."""
    conn = create_connection()
    try:
        c = conn.cursor()
        c.execute("INSERT INTO menu_items (name, price, category) VALUES (?, ?, ?)", (name, price, category))
        conn.commit()
        print(f"Added '{name}' to the menu.")
    finally:
        conn.close()

def view_menu():
    """Display all items on the menu."""
    conn = create_connection()
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM menu_items")
        items = c.fetchall()
        for item in items:
            print(f"ID: {item[0]}, Name: {item[1]}, Price: ${item[2]:.2f}, Category: {item[3]}")
    finally:
        conn.close()

def create_order(order_type):
    """Create a new order."""
    conn = create_connection()
    try:
        c = conn.cursor()
        c.execute("INSERT INTO orders (order_type, status) VALUES (?, ?)", (order_type, 'open'))
        conn.commit()
        print(f"Created a new {order_type} order with ID: {c.lastrowid}")
        return c.lastrowid
    finally:
        conn.close()

def add_to_order(order_id, item_id, quantity):
    """Add an item to an existing order."""
    conn = create_connection()
    try:
        c = conn.cursor()
        c.execute("INSERT INTO order_items (order_id, item_id, quantity) VALUES (?, ?, ?)", (order_id, item_id, quantity))
        conn.commit()
        print(f"Added {quantity} of item {item_id} to order {order_id}.")
    finally:
        conn.close()

def generate_bill(order_id, discount=0):
    """Generate the bill for an order."""
    conn = create_connection()
    try:
        c = conn.cursor()
        c.execute('''
            SELECT mi.name, mi.price, oi.quantity
            FROM order_items oi
            JOIN menu_items mi ON oi.item_id = mi.id
            WHERE oi.order_id = ?
        ''', (order_id,))
        items = c.fetchall()

        subtotal = sum(item[1] * item[2] for item in items)
        tax_rate = 0.1  # 10% tax
        tax_amount = subtotal * tax_rate
        discount_amount = subtotal * (discount / 100)
        total = subtotal + tax_amount - discount_amount

        print(f"\n--- Bill for Order ID: {order_id} ---")
        for item in items:
            print(f"{item[0]} (x{item[2]}): ${item[1] * item[2]:.2f}")
        print("--------------------")
        print(f"Subtotal: ${subtotal:.2f}")
        print(f"Tax (10%): ${tax_amount:.2f}")
        if discount > 0:
            print(f"Discount ({discount}%): -${discount_amount:.2f}")
        print(f"Total: ${total:.2f}")
        print("--------------------\n")
        return subtotal, tax_amount, discount_amount, total
    finally:
        conn.close()

def record_payment(order_id, subtotal, tax, discount, total, payment_method):
    """Record a payment and close the order."""
    conn = create_connection()
    try:
        c = conn.cursor()
        c.execute('''
            INSERT INTO payments (order_id, subtotal, tax_amount, discount_amount, total_amount, payment_method)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (order_id, subtotal, tax, discount, total, payment_method))
        c.execute("UPDATE orders SET status = 'closed' WHERE id = ?", (order_id,))
        conn.commit()
        print(f"Payment of ${total:.2f} via {payment_method} recorded for order {order_id}.")
    finally:
        conn.close()

def sales_report(start_date, end_date):
    """Generate a sales report for a given period."""
    conn = create_connection()
    try:
        c = conn.cursor()
        c.execute('''
            SELECT SUM(total_amount)
            FROM payments
            WHERE DATE(payment_date) BETWEEN ? AND ?
        ''', (start_date, end_date))
        total_sales = c.fetchone()[0]

        print(f"\n--- Sales Report from {start_date} to {end_date} ---")
        if total_sales:
            print(f"Total Sales: ${total_sales:.2f}")
        else:
            print("No sales in this period.")
        print("--------------------------------\n")
    finally:
        conn.close()

