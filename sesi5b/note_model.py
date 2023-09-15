from config import db, ma
from datetime import datetime
from marshmallow import fields

class Note(db.Model):
    __tablename__ = 'note'
    note_id = db.Column(
        db.Integer, 
        primary_key=True
    )
    person_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
    content = db.Column(db.String)
    timestamp = db.Column(
        db.DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )

class NoteSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Note
        sqla_session = db.session

    person = fields.Nested("NotePersonSchema", default=None)


class NotePersonSchema(ma.SQLAlchemyAutoSchema):
    """
    This class exists to get around a recursion issue
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    person_id = fields.Int()
    lname = fields.Str()
    fname = fields.Str()
    timestamp = fields.Str()