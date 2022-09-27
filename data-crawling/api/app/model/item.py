from app import db

class Item(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    price = db.Column(db.BigInteger, nullable=False)
    sold = db.Column(db.BigInteger, nullable=False)
    place = db.Column(db.String(250), nullable=False)
    rate = db.Column(db.Float(2), nullable=False)
    categori = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return '<Item {}>'.format(self.name)
