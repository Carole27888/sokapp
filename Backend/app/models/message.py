from app.extensions import db
import datetime

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.Integer, default=lambda: int(datetime.datetime.utcnow().timestamp()))
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'))  

    sender = db.relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver = db.relationship("User", foreign_keys=[receiver_id], back_populates="received_messages")
    match = db.relationship("Match", back_populates="messages")  

    def __repr__(self):
        return f"<Message(id={self.id}, sender_id={self.sender_id}, receiver_id={self.receiver_id}, content={self.content})>"