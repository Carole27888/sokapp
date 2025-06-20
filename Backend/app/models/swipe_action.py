from app import db
import datetime
import enum

class SwipeActionType(enum.Enum):
    right = "right"
    left = "left"
    up = "up"
    down = "down"
    none = "none"

class SwipeAction(db.Model):
    __tablename__ = 'swipe_actions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action_type = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.Float, default=lambda: datetime.datetime.utcnow().timestamp())
    produce_listing_id = db.Column(db.Integer, db.ForeignKey('produce_listings.id'), nullable=False)  # Foreign key to ProduceListing

    user = db.relationship("User", back_populates="swipe_actions")
    produce_listing = db.relationship("ProduceListing", back_populates="swipe_actions")  # Relationship to ProduceListing

    def __repr__(self):
        return f"<SwipeAction(id={self.id}, user_id={self.user_id}, action_type={self.action_type}, timestamp={self.timestamp})>"