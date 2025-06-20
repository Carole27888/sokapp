from app import db
from sqlalchemy.orm import validates

class WeeklyMarketSummary(db.Model):
    __tablename__ = 'weekly_market_summary'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    county = db.Column(db.String(100), nullable=False)
    week_start_date = db.Column(db.DateTime, nullable=False)
    week_end_date = db.Column(db.DateTime, nullable=False)
    demand_data = db.Column(db.String(500), nullable=True)  # JSON or string representation of demand data
    total_sales = db.Column(db.Float, nullable=False)
    total_units_sold = db.Column(db.Integer, nullable=False)
    average_price_per_unit = db.Column(db.Float, nullable=False)

    @validates('week_start_date', 'week_end_date')
    def validate_dates(self, key, value):
        from datetime import datetime
        if not isinstance(value, (str, datetime)):
            raise ValueError(f"{key} must be a date string or DateTime object")
        return value