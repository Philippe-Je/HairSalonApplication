# Import required modules
from flask import request, jsonify  # Used to handle incoming request data and return JSON responses
from app import app, db             # Import the Flask app and the SQLAlchemy database instance
from models import Client, Stylist, Service, Appointment, Invoice  # Import ORM models
from datetime import datetime       # Used to handle and format dates and times

# =========================
# CLIENT ROUTES
# =========================

@app.route("/clients", methods=["GET"])
def get_all_clients():
    """Fetches all clients from the database and returns them as JSON."""
    clients = Client.query.all()
    return jsonify([client.to_json() for client in clients])

@app.route("/clients", methods=["POST"])
def create_client():
    """Creates a new client using the request JSON payload."""
    try:
        data = request.get_json()
        new_client = Client(
            name=data.get("name"),
            phone=data.get("phone"),
            email=data.get("email")
        )
        db.session.add(new_client)
        db.session.commit()
        return jsonify(new_client.to_json()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/clients/<int:client_id>", methods=["PUT"])
def update_client(client_id):
    """Updates an existing client's information by ID."""
    try:
        client = Client.query.get_or_404(client_id)
        data = request.get_json()
        client.name = data.get("name", client.name)
        client.phone = data.get("phone", client.phone)
        client.email = data.get("email", client.email)
        db.session.commit()
        return jsonify(client.to_json())
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/clients/<int:client_id>", methods=["DELETE"])
def delete_client(client_id):
    """Deletes a client from the database by ID."""
    try:
        client = Client.query.get_or_404(client_id)
        db.session.delete(client)
        db.session.commit()
        return jsonify({"message": "Client deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# =========================
# STYLIST ROUTES
# =========================

@app.route("/stylists", methods=["GET"])
def get_all_stylists():
    """Fetches all stylists and returns their info as JSON."""
    stylists = Stylist.query.all()
    return jsonify([stylist.to_json() for stylist in stylists])

@app.route("/stylists", methods=["POST"])
def create_stylist():
    """Creates a new stylist based on input JSON and saves to database."""
    try:
        data = request.get_json()
        new_stylist = Stylist(
            name=data.get("name"),
            specialty=data.get("specialty"),
            email=data.get("email"),
            phone=data.get("phone"),
            portfolio_images=data.get("portfolio_images", [])
        )
        db.session.add(new_stylist)
        db.session.commit()
        return jsonify(new_stylist.to_json()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/stylists/<int:stylist_id>", methods=["PUT"])
def update_stylist(stylist_id):
    """Updates stylist information such as name, specialty, and contact details."""
    try:
        stylist = Stylist.query.get_or_404(stylist_id)
        data = request.get_json()
        stylist.name = data.get("name", stylist.name)
        stylist.specialty = data.get("specialty", stylist.specialty)
        stylist.email = data.get("email", stylist.email)
        stylist.phone = data.get("phone", stylist.phone)
        stylist.portfolio_images = data.get("portfolio_images", stylist.portfolio_images)
        db.session.commit()
        return jsonify(stylist.to_json())
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/stylists/<int:stylist_id>", methods=["DELETE"])
def delete_stylist(stylist_id):
    """Deletes a stylist from the database by ID."""
    try:
        stylist = Stylist.query.get_or_404(stylist_id)
        db.session.delete(stylist)
        db.session.commit()
        return jsonify({"message": "Stylist deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# =========================
# SERVICE ROUTES
# =========================

@app.route("/services", methods=["GET"])
def get_all_services():
    """Returns a list of all available salon services."""
    services = Service.query.all()
    return jsonify([service.to_json() for service in services])

@app.route("/services", methods=["POST"])
def create_service():
    """Creates a new service (e.g., haircut, color) with pricing and duration."""
    try:
        data = request.get_json()
        new_service = Service(
            name=data.get("name"),
            duration=data.get("duration"),
            price=data.get("price")
        )
        db.session.add(new_service)
        db.session.commit()
        return jsonify(new_service.to_json()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/services/<int:service_id>", methods=["PUT"])
def update_service(service_id):
    """Updates the name, duration, or price of an existing service."""
    try:
        service = Service.query.get_or_404(service_id)
        data = request.get_json()
        service.name = data.get("name", service.name)
        service.duration = data.get("duration", service.duration)
        service.price = data.get("price", service.price)
        db.session.commit()
        return jsonify(service.to_json())
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/services/<int:service_id>", methods=["DELETE"])
def delete_service(service_id):
    """Deletes a service by its unique ID."""
    try:
        service = Service.query.get_or_404(service_id)
        db.session.delete(service)
        db.session.commit()
        return jsonify({"message": "Service deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# =========================
# APPOINTMENT ROUTES
# =========================

@app.route("/appointments", methods=["GET"])
def get_all_appointments():
    """Fetches all appointments and returns them as JSON objects."""
    appointments = Appointment.query.all()
    return jsonify([appointment.to_json() for appointment in appointments])

@app.route("/appointments", methods=["POST"])
def create_appointment():
    """
    Books a new appointment. Requires client_id, stylist_id, service_id,
    date (YYYY-MM-DD), and time (HH:MM:SS).
    """
    try:
        data = request.get_json()
        new_appointment = Appointment(
            client_id=data.get("client_id"),
            stylist_id=data.get("stylist_id"),
            service_id=data.get("service_id"),
            date=datetime.strptime(data.get("date"), "%Y-%m-%d").date(),
            time=datetime.strptime(data.get("time"), "%H:%M:%S").time(),
            status=data.get("status", "booked")
        )
        db.session.add(new_appointment)
        db.session.commit()
        return jsonify(new_appointment.to_json()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/appointments/<int:appointment_id>", methods=["PUT"])
def update_appointment(appointment_id):
    """Updates an existing appointment's date, time, service, or status."""
    try:
        appointment = Appointment.query.get_or_404(appointment_id)
        data = request.get_json()
        if "date" in data:
            appointment.date = datetime.strptime(data["date"], "%Y-%m-%d").date()
        if "time" in data:
            appointment.time = datetime.strptime(data["time"], "%H:%M:%S").time()
        appointment.status = data.get("status", appointment.status)
        appointment.service_id = data.get("service_id", appointment.service_id)
        db.session.commit()
        return jsonify(appointment.to_json())
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/appointments/<int:appointment_id>", methods=["DELETE"])
def delete_appointment(appointment_id):
    """Cancels an appointment by removing it from the database."""
    try:
        appointment = Appointment.query.get_or_404(appointment_id)
        db.session.delete(appointment)
        db.session.commit()
        return jsonify({"message": "Appointment deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# =========================
# INVOICE ROUTES
# =========================

@app.route("/invoices", methods=["GET"])
def get_all_invoices():
    """Returns all invoices for completed appointments."""
    invoices = Invoice.query.all()
    return jsonify([invoice.to_json() for invoice in invoices])

@app.route("/invoices", methods=["POST"])
def create_invoice():
    """
    Creates an invoice after an appointment. Requires:
    - appointment_id
    - total_amount
    - payment_method
    """
    try:
        data = request.get_json()
        new_invoice = Invoice(
            appointment_id=data.get("appointment_id"),
            total_amount=data.get("total_amount"),
            payment_method=data.get("payment_method"),
            paid_at=datetime.utcnow()
        )
        db.session.add(new_invoice)
        db.session.commit()
        return jsonify(new_invoice.to_json()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/invoices/<int:invoice_id>", methods=["PUT"])
def update_invoice(invoice_id):
    """Updates the payment method or total amount of an existing invoice."""
    try:
        invoice = Invoice.query.get_or_404(invoice_id)
        data = request.get_json()
        invoice.total_amount = data.get("total_amount", invoice.total_amount)
        invoice.payment_method = data.get("payment_method", invoice.payment_method)
        db.session.commit()
        return jsonify(invoice.to_json())
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/invoices/<int:invoice_id>", methods=["DELETE"])
def delete_invoice(invoice_id):
    """Deletes an invoice by its ID."""
    try:
        invoice = Invoice.query.get_or_404(invoice_id)
        db.session.delete(invoice)
        db.session.commit()
        return jsonify({"message": "Invoice deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
