from database import db
from models.auction import Auction
from models.bid import Bid

class AuctionRepo:
    def get_all_auctions(self):
        return Auction.query.order_by(Auction.end_at.asc()).all()
    
    def get_auction_by_id(self, auction_id):
        return Auction.query.get_or_404(auction_id)
    
    def get_bidding_history(self, auction_id):
        return (Bid.query
                .filter_by(auction_id=auction_id)
                .order_by(Bid.created_at.desc())
                .all())

auction_repo = AuctionRepo()