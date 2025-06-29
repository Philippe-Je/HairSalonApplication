from flask import request, jsonify
from app import app, db
from models import Client, Stylist, Service, Appointment, Invoice
from datetime import datetime

# =========================
# CLIENT ROUTES
# =========================

# GET all clients
@app.route("/clients", methods=["GET"])
def get_all_clients():
    """Fetches all clients from the database and returns them as JSON."""
    clients = Client.query.all()
    return jsonify([client.to_json() for client in clients])

# POST a new client
@app.route("/clients", methods=["POST"])
def create_client():
    """Creates a new client using the request JSON payload."""
    data = request.get_json()
    new_client = Client(
        name=data.get("name"),
        phone=data.get("phone"),
        email=data.get("email")
    )
    db.session.add(new_client)
    db.session.commit()
    return jsonify(new_client.to_json()), 201

# PUT (update) a client by ID
@app.route("/clients/<int:client_id>", methods=["PUT"])
def update_client(client_id):
    """Updates an existing client's information by ID."""
    client = Client.query.get_or_404(client_id)
    data = request.get_json()
    client.name = data.get("name", client.name)
    client.phone = data.get("phone", client.phone)
    client.email = data.get("email", client.email)
    db.session.commit()
    return jsonify(client.to_json())

# DELETE a client by ID
@app.route("/clients/<int:client_id>", methods=["DELETE"])
def delete_client(client_id):
    """Deletes a client from the database by ID."""
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    return jsonify({"message": "Client deleted successfully"})


# =========================
# STYLIST ROUTES
# =========================

# GET all stylists
@app.route("/stylists", methods=["GET"])
def get_all_stylists():
    """Fetches all stylists and returns their info as JSON."""
    stylists = Stylist.query.all()
    return jsonify([stylist.to_json() for stylist in stylists])

# POST a new stylist
@app.route("/stylists", methods=["POST"])
def create_stylist():
    """Creates a new stylist based on input JSON and saves to database."""
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

# PUT (update) a stylist by ID
@app.route("/stylists/<int:stylist_id>", methods=["PUT"])
def update_stylist(stylist_id):
    """Updates stylist information such as name, specialty, and contact details."""
    stylist = Stylist.query.get_or_404(stylist_id)
    data = request.get_json()
    stylist.name = data.get("name", stylist.name)
    stylist.specialty = data.get("specialty", stylist.specialty)
    stylist.email = data.get("email", stylist.email)
    stylist.phone = data.get("phone", stylist.phone)
    stylist.portfolio_images = data.get("portfolio_images", stylist.portfolio_images)
    db.session.commit()
    return jsonify(stylist.to_json())

# DELETE a stylist by ID
@app.route("/stylists/<int:stylist_id>", methods=["DELETE"])
def delete_stylist(stylist_id):
    """Deletes a stylist from the database by ID."""
    stylist = Stylist.query.get_or_404(stylist_id)
    db.session.delete(stylist)
    db.session.commit()
    return jsonify({"message": "Stylist deleted successfully"})


# =========================
# SERVICE ROUTES
# =========================

# GET all services
@app.route("/services", methods=["GET"])
def get_all_services():
    """Returns a list of all available salon services."""
    services = Service.query.all()
    return jsonify([service.to_json() for service in services])

# POST a new service
@app.route("/services", methods=["POST"])
def create_service():
    """Creates a new service (e.g., haircut, color) with pricing and duration."""
    data = request.get_json()
    new_service = Service(
        name=data.get("name"),
        duration=data.get("duration"),
        price=data.get("price")
    )
    db.session.add(new_service)
    db.session.commit()
    return jsonify(new_service.to_json()), 201

# PUT (update) a service by ID
@app.route("/services/<int:service_id>", methods=["PUT"])
def update_service(service_id):
    """Updates the name, duration, or price of an existing service."""
    service = Service.query.get_or_404(service_id)
    data = request.get_json()
    service.name = data.get("name", service.name)
    service.duration = data.get("duration", service.duration)
    service.price = data.get("price", service.price)
    db.session.commit()
    return jsonify(service.to_json())

# DELETE a service by ID
@app.route("/services/<int:service_id>", methods=["DELETE"])
def delete_service(service_id):
    """Deletes a service by its unique ID."""
    service = Service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    return jsonify({"message": "Service deleted successfully"})


# =========================
# APPOINTMENT ROUTES
# =========================

# GET all appointments
@app.route("/appointments", methods=["GET"])
def get_all_appointments():
    """Fetches all appointments and returns them as JSON objects."""
    appointments = Appointment.query.all()
    return jsonify([appointment.to_json() for appointment in appointments])

# POST a new appointment
@app.route("/appointments", methods=["POST"])
def create_appointment():
    """
    Books a new appointment. Requires client_id, stylist_id, service_id,
    date (YYYY-MM-DD), and time (HH:MM:SS).
    """
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

# PUT (update) an appointment
@app.route("/appointments/<int:appointment_id>", methods=["PUT"])
def update_appointment(appointment_id):
    """Updates an existing appointment's date, time, service, or status."""
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

# DELETE an appointment
@app.route("/appointments/<int:appointment_id>", methods=["DELETE"])
def delete_appointment(appointment_id):
    """Cancels an appointment by removing it from the database."""
    appointment = Appointment.query.get_or_404(appointment_id)
    db.session.delete(appointment)
    db.session.commit()
    return jsonify({"message": "Appointment deleted successfully"})


# =========================
# INVOICE ROUTES
# =========================

# GET all invoices
@app.route("/invoices", methods=["GET"])
def get_all_invoices():
    """Returns all invoices for completed appointments."""
    invoices = Invoice.query.all()
    return jsonify([invoice.to_json() for invoice in invoices])

# POST a new invoice
@app.route("/invoices", methods=["POST"])
def create_invoice():
    """
    Creates an invoice after an appointment. Requires:
    - appointment_id
    - total_amount
    - payment_method
    """
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

# PUT (update) an invoice
@app.route("/invoices/<int:invoice_id>", methods=["PUT"])
def update_invoice(invoice_id):
    """Updates the payment method or total amount of an existing invoice."""
    invoice = Invoice.query.get_or_404(invoice_id)
    data = request.get_json()
    invoice.total_amount = data.get("total_amount", invoice.total_amount)
    invoice.payment_method = data.get("payment_method", invoice.payment_method)
    db.session.commit()
    return jsonify(invoice.to_json())

# DELETE an invoice
@app.route("/invoices/<int:invoice_id>", methods=["DELETE"])
def delete_invoice(invoice_id):
    """Deletes an invoice by its ID."""
    invoice = Invoice.query.get_or_404(invoice_id)
    db.session.delete(invoice)
    db.session.commit()
    return jsonify({"message": "Invoice deleted successfully"})
