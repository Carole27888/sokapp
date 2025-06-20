from app.extensions import db
from datetime import datetime

class PaymentGatewayLog(db.Model):
    __tablename__ = 'payment_gateway_logs'

    id = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.String(50))  # e.g., 'mpesa', 'paypal'
    payload = db.Column(db.Text)  # Raw JSON/XML body
    response = db.Column(db.Text)  # API response from gateway
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)