from database import db

class Reaction(db.Model):
    __tablename__ = 'reactions'

    id = db.Column(db.Integer, primary_key=True)
    
    auction_id = db.Column(db.Integer, db.ForeignKey('auctions.id'), nullable=False)
    kind = db.Column(db.String(10), nullable=False) # Like eller dislike
    amount = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

