from app.extensions import db
from sqlalchemy.sql import func
from sqlalchemy.orm import validates

class Payment(db.Model):
    __tablename__ = 'payments'

    PAYMENT_METHODS = [
        ('mpesa', 'M-Pesa'),
        ('paypal', 'PayPal'),
        ('stripe', 'Stripe'),
        ('bank_transfer', 'Bank Transfer')
    ]
    STATUS_OPTIONS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ]

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    transaction_id = db.Column(db.String(50), nullable=True, unique=True)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    related_order_id = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Payment(id={self.id}, user_id={self.user_id}, amount={self.amount}, payment_method={self.payment_method}, status={self.status})>"

    @validates('payment_method')
    def validate_payment_method(self, key, value):
        if value not in dict(self.PAYMENT_METHODS).keys():
            raise ValueError(f"Invalid payment method: {value}")
        return value

    @validates('status')
    def validate_status(self, key, value):
        if value not in dict(self.STATUS_OPTIONS).keys():
            raise ValueError(f"Invalid status: {value}")
        return value

    @validates('amount')
    def validate_amount(self, key, value):
        if value <= 0:
            raise ValueError("Amount must be greater than zero")
        return value

    @validates('transaction_id')
    def validate_transaction_id(self, key, value):
        if value and len(value) > 50:
            raise ValueError("Transaction ID cannot exceed 50 characters")
        return value

    @validates('description')
    def validate_description(self, key, value):
        if value and len(value) > 255:
            raise ValueError("Description cannot exceed 255 characters")
        return value

    @validates('related_order_id')
    def validate_related_order_id(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("Related order ID must be a positive integer")
        return value

    @validates('user_id')    
    def validate_user_id(self, key, value):
        if value <= 0:
            raise ValueError("User ID must be a positive integer")
        return value

    @validates('id')
    def validate_id(self, key, value):
        if value <= 0:
            raise ValueError("ID must be a positive integer")
        return value

    @validates('created_at', 'updated_at')
    def validate_datetime(self, key, value):
        import datetime
        if not isinstance(value, datetime.datetime):
            raise ValueError(f"{key} must be a valid datetime object")
        return value