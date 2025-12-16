from database import db

class Auction(db.Model):
    __tablename__ = 'auctions'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    starting_bid = db.Column(db.Float, nullable=False)
    start_at = db.Column(db.DateTime, server_default=db.func.now())
    end_at = db.Column(db.DateTime, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
