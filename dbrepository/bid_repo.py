from database import db
from models.bid import Bid

class BidRepo:
    def get_top_2(self, auction_id):
        return Bid.query.filter_by(auction_id=auction_id).order_by(Bid.amount.desc()).limit(2).all()
    
    def place_bid(self, auction_id, bidder_email, amount):
        new_bid = Bid(auction_id=auction_id, bidder_email=bidder_email, amount=amount)
        db.session.add(new_bid)
        db.session.commit()

    def get_bid_by_id(self, bid_id):
        return Bid.query.get_or_404(bid_id)

    def delete_bid(self, bid_id):
        bid = self.get_bid_by_id(bid_id)
        if bid:
            db.session.delete(bid)
            db.session.commit()

bid_repo = BidRepo()

