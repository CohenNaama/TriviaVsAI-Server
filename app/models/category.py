from app import db
from sqlalchemy_serializer import SerializerMixin


class Category(db.Model, SerializerMixin):
    """
    Category model to store question categories.

    Attributes:
        id (int): Primary key, auto-increment.
        name (str): Name of the category, must be unique.
        usage_count (int): Number of times the category has been used.
    """
    __tablename__ = 'categories'
    serialize_only = ('id', 'name', 'usage_count')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    usage_count = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"<Category id={self.id}, name={self.name}, usage_count={self.usage_count}>"
