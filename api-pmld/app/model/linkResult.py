from app import db

class LinkResult(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    place = db.Column(db.String(250), nullable=False)
    categori = db.Column(db.String(60), nullable=False)
    link = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return '<LinkResult {}>'.format(self.name)