from app import db

class TagCategory(db.Model):
    __tablename__ = 'tag_categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<TagCategory(id={self.id}, name='{self.name}', description='{self.description}')>"

    def __str__(self):
        return f"TagCategory: {self.name} - {self.description or 'No description'}"