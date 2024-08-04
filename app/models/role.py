from app import db
from sqlalchemy_serializer import SerializerMixin


class Role(db.Model, SerializerMixin):
    """
    Role model to store different roles within the application.

    Attributes:
        id (int): Primary key, auto-increment.
        name (str): Name of the role, must be unique.
    """
    __tablename__ = 'roles'
    serialize_only = ('id', 'name')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return '<Role name: %r>' % self.name


    # def to_dict(self):
    #     """
    #     Convert the role object to a dictionary.
    #
    #     Returns:
    #         dict: Dictionary representation of the role.
    #     """
    #     return {
    #         'id': self.id,
    #         'name': self.name
    #     }

