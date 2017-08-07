# models.py

from main import app, db
import uuid
import datetime

class Paste(db.Model):
    id = db.Column(db.String(36), unique=True, primary_key=True)
    poster = db.Column(db.String(51))
    paste = db.Column(db.Text())
    date = db.Column(db.DateTime)
    value = db.Column(db.Integer)

    def __init__(self, text, poster, value):
        self.paste = text
        self.poster = poster
        self.id = str(uuid.uuid4())
        self.date = datetime.datetime.now().strftime("%c")
        self.value = value

    @property
    def serialize(self):
        '''return as a json object so we can use it in RESTful API'''
        return {'id': self.id,
    	       'date': self.date.strftime("%c"),
    	       'poster': self.poster,
               'value': self.value,
               'paster': self.paste }
