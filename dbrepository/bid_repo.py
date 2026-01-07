from database import db
from models.bid import Bid

# Repository för hantering av bud
class BidRepo:
    def get_top_2(self, auction_id):
        return Bid.query.filter_by(auction_id=auction_id).order_by(Bid.amount.desc()).limit(2).all()
    
    # Placerar ett nytt bud
    def place_bid(self, auction_id, bidder_email, amount):
        new_bid = Bid(auction_id=auction_id, bidder_email=bidder_email, amount=amount)
        db.session.add(new_bid)
        db.session.commit()

    # Hämtar ett bud baserat på ID
    def get_bid_by_id(self, bid_id):
        return Bid.query.get_or_404(bid_id)

    # Tar bort ett bud baserat på ID
    def delete_bid(self, bid_id):
        bid = self.get_bid_by_id(bid_id)
        if bid:
            db.session.delete(bid)
            db.session.commit()

# Skapar en instans av BidRepo för användning i applikationen
bid_repo = BidRepo()

