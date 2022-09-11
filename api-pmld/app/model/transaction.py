from app import db
from datetime import datetime
from app.model.user import User

class Transaction(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user = db.Column(db.BigInteger, db.ForeignKey(User.id, ondelete='CASCADE'))
    subs_at = db.Column(db.DateTime, default=datetime.now)
    month = db.Column(db.Integer, nullable=False)
    categori = db.Column(db.String(60), nullable=False)
    place = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return '<Transaction {}>'.format(self.name)
