from app.extensions import db
from datetime import datetime

class Subscription(db.Model):
    __tablename__ = 'subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plan_name = db.Column(db.String(50), nullable=False)  # e.g., 'Basic', 'Premium'
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False)  # Subscription end date
    status = db.Column(db.String(20), default='active')  # e.g., 'active', 'cancelled', 'expired'

    user = db.relationship("User", back_populates="subscriptions")

    def __repr__(self):
        return f"<Subscription(id={self.id}, user_id={self.user_id}, plan_name='{self.plan_name}', start_date={self.start_date}, end_date={self.end_date}, status='{self.status}')>"