from datetime import datetime
from app import db

# ========== Client ==========
class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    appointments = db.relationship('Appointment', backref='client', lazy=True)

# ========== Stylist ==========
class Stylist(db.Model):
    __tablename__ = 'stylists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))

    # Relationships
    appointments = db.relationship('Appointment', backref='stylist', lazy=True)

# ========== Service ==========
class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer)  # in minutes
    price = db.Column(db.Float)

    # Relationships
    appointments = db.relationship('Appointment', backref='service', lazy=True)

# ========== Appointment ==========
class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    stylist_id = db.Column(db.Integer, db.ForeignKey('stylists.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)

    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(50), default='booked')  # e.g., booked, completed, cancelled

    # Relationships
    invoice = db.relationship('Invoice', uselist=False, backref='appointment')  # 1-to-1

# ========== Invoice ==========
class Invoice(db.Model):
    __tablename__ = 'invoices'

    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False, unique=True)
    total_amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50))  # e.g., cash, card
    paid_at = db.Column(db.DateTime, default=datetime.utcnow)
