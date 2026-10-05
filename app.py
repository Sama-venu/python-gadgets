from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "sample_secret_key"

# Static list of electronics gadgets
GADGETS = [
    {"id": 1, "name": "Laptop - Dell XPS 15", "price": 1500, "stock": 5},
    {"id": 2, "name": "Smartphone - iPhone 15", "price": 999, "stock": 8},
    {"id": 3, "name": "Tablet - iPad Air", "price": 599, "stock": 10},
    {"id": 4, "name": "Smartwatch - Apple Watch", "price": 399, "stock": 6},
    {"id": 5, "name": "Headphones - Sony WH-1000XM5", "price": 349, "stock": 12},
]

# In-memory bookings store
bookings = []


@app.route("/")
def index():
    """Home page listing all gadgets."""
    return render_template("index.html", gadgets=GADGETS)


@app.route("/book/<int:gadget_id>", methods=["GET", "POST"])
def book(gadget_id):
    """Handle booking for a specific gadget."""
    gadget = next((g for g in GADGETS if g["id"] == gadget_id), None)

    if not gadget:
        flash("Gadget not found!", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        customer_name = request.form.get("customer_name", "").strip()
        email = request.form.get("email", "").strip()
        quantity = request.form.get("quantity", "1")

        if not customer_name or not email:
            flash("Please fill in all fields.", "warning")
            return redirect(url_for("book", gadget_id=gadget_id))

        try:
            quantity = int(quantity)
        except ValueError:
            flash("Invalid quantity.", "warning")
            return redirect(url_for("book", gadget_id=gadget_id))

        if quantity < 1 or quantity > gadget["stock"]:
            flash(f"Quantity must be between 1 and {gadget['stock']}.", "warning")
            return redirect(url_for("book", gadget_id=gadget_id))

        # Create booking record
        booking = {
            "id": len(bookings) + 1,
            "gadget": gadget["name"],
            "customer_name": customer_name,
            "email": email,
            "quantity": quantity,
            "total": gadget["price"] * quantity,
            "booked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        bookings.append(booking)

        # Reduce stock
        gadget["stock"] -= quantity

        flash(f"Booking confirmed for {gadget['name']}!", "success")
        return redirect(url_for("bookings_list"))

    return render_template("book.html", gadget=gadget)


@app.route("/bookings")
def bookings_list():
    """Show all bookings."""
    return render_template("bookings.html", bookings=bookings)


@app.route("/cancel/<int:booking_id>")
def cancel(booking_id):
    """Cancel a booking and restore stock."""
    booking = next((b for b in bookings if b["id"] == booking_id), None)
    if booking:
        for gadget in GADGETS:
            if gadget["name"] == booking["gadget"]:
                gadget["stock"] += booking["quantity"]
                break
        bookings.remove(booking)
        flash("Booking cancelled successfully.", "info")
    else:
        flash("Booking not found.", "danger")
    return redirect(url_for("bookings_list"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
