from app.extensions import db
import enum

class UserRole(enum.Enum):
    farmer = "farmer"
    admin = "admin"
    buyer = "buyer"

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default=UserRole.farmer.value)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    user_profiles = db.relationship("User_Profile", back_populates="user")
    sent_messages = db.relationship("Message", foreign_keys='Message.sender_id', back_populates="sender")
    received_messages = db.relationship("Message", foreign_keys='Message.receiver_id', back_populates="receiver")
    # matches = db.relationship("Match", back_populates="buyer")
    subscriptions = db.relationship("Subscription", back_populates="user")
    notifications_tokens = db.relationship("PushNotificationsToken", back_populates="user")
    export_data = db.relationship("ExportData", back_populates="user")
    bulk_uploads = db.relationship("BulkUpload", back_populates="user")
    swipe_actions = db.relationship("SwipeAction", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, role={self.role})>"
