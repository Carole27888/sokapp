from app.extensions import db
from datetime import datetime
import enum

class MatchStatus(enum.Enum):
    matched = "matched"
    rejected = "rejected"
    pending = "pending"
    
class Match(db.Model):
    __tablename__ = 'matches'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    produce_listing_id = db.Column(db.Integer, db.ForeignKey('produce_listings.id'), nullable=False)
    match_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default=MatchStatus.pending.value)

    buyer = db.relationship("User_Profile", back_populates="matches")
    produce_listing = db.relationship("ProduceListing", back_populates="matches")
    messages = db.relationship("Message", back_populates="match")

    def __repr__(self):
        return f"<Match(id={self.id}, buyer_id={self.buyer_id}, produce_listing_id={self.produce_listing_id})>"