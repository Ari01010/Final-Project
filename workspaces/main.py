# main.py

import argparse
from billingsystem import (
    add_menu_item, view_menu, create_order, add_to_order,
    generate_bill, record_payment, sales_report
)
from database import setup_database

def main():
    """Main function to run the command-line interface."""
    setup_database()  # Ensure the database and tables exist

    parser = argparse.ArgumentParser(description="Restaurant Billing System")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add item command
    parser_add_item = subparsers.add_parser("add-item", help="Add a new menu item")
    parser_add_item.add_argument("name", type=str, help="Name of the item")
    parser_add_item.add_argument("price", type=float, help="Price of the item")
    parser_add_item.add_argument("category", type=str, help="Category of the item")

    # View menu command
    subparsers.add_parser("view-menu", help="View all menu items")

    # Create order command
    parser_create_order = subparsers.add_parser("create-order", help="Create a new order")
    parser_create_order.add_argument("order_type", choices=["Dine-In", "Takeaway"], help="Type of order")

    # Add to order command
    parser_add_to_order = subparsers.add_parser("add-to-order", help="Add item to an order")
    parser_add_to_order.add_argument("order_id", type=int, help="ID of the order")
    parser_add_to_order.add_argument("item_id", type=int, help="ID of the menu item")
    parser_add_to_order.add_argument("quantity", type=int, help="Quantity of the item")

    # Generate bill command
    parser_generate_bill = subparsers.add_parser("generate-bill", help="Generate a bill for an order")
    parser_generate_bill.add_argument("order_id", type=int, help="ID of the order")
    parser_generate_bill.add_argument("--discount", type=float, default=0, help="Discount percentage")

    # Record payment command
    parser_record_payment = subparsers.add_parser("record-payment", help="Record a payment for an order")
    parser_record_payment.add_argument("order_id", type=int, help="ID of the order")
    parser_record_payment.add_argument("subtotal", type=float, help="Subtotal of the bill")
    parser_record_payment.add_argument("tax", type=float, help="Tax amount")
    parser_record_payment.add_argument("discount", type=float, help="Discount amount")
    parser_record_payment.add_argument("total", type=float, help="Total amount paid")
    parser_record_payment.add_argument("payment_method", type=str, help="Payment method (e.g., Cash, Credit Card)")

    # Sales report command
    parser_sales_report = subparsers.add_parser("sales-report", help="Generate a sales report")
    parser_sales_report.add_argument("start_date", type=str, help="Start date (YYYY-MM-DD)")
    parser_sales_report.add_argument("end_date", type=str, help="End date (YYYY-MM-DD)")

    args = parser.parse_args()

    if args.command == "add-item":
        add_menu_item(args.name, args.price, args.category)
    elif args.command == "view-menu":
        view_menu()
    elif args.command == "create-order":
        create_order(args.order_type)
    elif args.command == "add-to-order":
        add_to_order(args.order_id, args.item_id, args.quantity)
    elif args.command == "generate-bill":
        generate_bill(args.order_id, args.discount)
    elif args.command == "record-payment":
        record_payment(args.order_id, args.subtotal, args.tax, args.discount, args.total, args.payment_method)
    elif args.command == "sales-report":
        sales_report(args.start_date, args.end_date)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
