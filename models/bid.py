from database import db

# Modell för bud på auktioner
class Bid(db.Model):
    __tablename__ = 'bids'

    # Kolumner i tabellen
    id = db.Column(db.Integer, primary_key=True)
    auction_id = db.Column(db.Integer, db.ForeignKey('auctions.id'), nullable=False)
    bidder_email = db.Column(db.String(120), db.ForeignKey('users.email'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())