from app import db
from sqlalchemy_serializer import SerializerMixin


class Claim(db.Model, SerializerMixin):
    """
    Claim model to store user claims.

    Attributes:
        id (int): Primary key, auto-increment.
        type (str): Type of the claim.
        value (str): Value of the claim.
        user_id (int): Foreign key referencing the user.
    """
    __tablename__ = 'claims'
    serialize_only = ('id', 'type', 'value', 'user_id')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return '<Claim: %r>' % self.type


    # def to_dict(self):
    #     """
    #     Convert the claim object to a dictionary.
    #
    #     Returns:
    #         dict: Dictionary representation of the claim.
    #     """
    #     return {
    #         'id': self.id,
    #         'type': self.type,
    #         'value': self.value,
    #         'user_id': self.user_id
    #     }

