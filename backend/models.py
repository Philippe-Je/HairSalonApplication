from datetime import datetime
from app import db
from sqlalchemy.dialects.sqlite import JSON

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

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "created_at": self.created_at.isoformat()
        }

# ========== Stylist ==========
class Stylist(db.Model):
    __tablename__ = 'stylists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    
    portfolio_images = db.Column(JSON, default=[])

    appointments = db.relationship('Appointment', backref='stylist', lazy=True)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "specialty": self.specialty,
            "email": self.email,
            "phone": self.phone,
            "portfolio_images": self.portfolio_images
        }

# ========== Service ==========
class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer)  # in minutes
    price = db.Column(db.Float)

    appointments = db.relationship('Appointment', backref='service', lazy=True)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "duration": self.duration,
            "price": self.price
        }

# ========== Appointment ==========
class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    stylist_id = db.Column(db.Integer, db.ForeignKey('stylists.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)

    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(50), default='booked')

    invoice = db.relationship('Invoice', uselist=False, backref='appointment')

    def to_json(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "stylist_id": self.stylist_id,
            "service_id": self.service_id,
            "date": self.date.isoformat(),
            "time": self.time.isoformat(),
            "status": self.status
        }

# ========== Invoice ==========
class Invoice(db.Model):
    __tablename__ = 'invoices'

    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False, unique=True)
    total_amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50))
    paid_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_json(self):
        return {
            "id": self.id,
            "appointment_id": self.appointment_id,
            "total_amount": self.total_amount,
            "payment_method": self.payment_method,
            "paid_at": self.paid_at.isoformat()
        }
