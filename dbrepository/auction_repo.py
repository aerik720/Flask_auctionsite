from database import db
from models.auction import Auction
from models.bid import Bid

# Repository för hantering av auktioner
class AuctionRepo:
    # Hämtar alla auktioner sorterade efter sluttid
    def get_all_auctions(self):
        return Auction.query.order_by(Auction.end_at.asc()).all()
    
    # Hämtar en auktion baserat på ID
    def get_auction_by_id(self, auction_id):
        return Auction.query.get_or_404(auction_id)
    
    # Hämtar budhistorik för en auktion
    def get_bidding_history(self, auction_id):
        return (Bid.query
                .filter_by(auction_id=auction_id)
                .order_by(Bid.created_at.desc())
                .all())
    
    # Skapar en ny auktion
    def create_auction(self, title, description, category, starting_bid, end_at, image_url=None):
        new_auction = Auction(
            title=title,
            description=description,
            category=category,
            starting_bid=starting_bid,
            end_at=end_at,
            image_url=image_url
        )
        # Lägg till och spara den nya auktionen i databasen
        db.session.add(new_auction)
        db.session.commit()
        return new_auction

    # Uppdaterar en befintlig auktion
    def update(self, auction_id, auction_data):
        # Hämta det befintliga objektet med den moderna metoden.
        auction = db.session.get(Auction, auction_id)

        if auction:
            # Uppdatera fälten
            auction.title = auction_data['title']
            auction.description = auction_data['description']
            auction.category = auction_data['category']
            auction.starting_bid = auction_data['starting_bid']
            auction.end_at = auction_data['end_at']
            auction.image_url = auction_data['image_url']

            # Spara ändringarna i databasen
            db.session.commit()

        return auction
    
    # Tar bort en auktion baserat på ID
    def delete(self, auction_id):
        
        auction = db.session.get(Auction, auction_id)

        if auction:
            db.session.delete(auction)
            db.session.commit()
            return True

        return False
    
    def search(self, keyword=None, category_keyword=None, min_price=None, max_price=None, ends_before=None):

        query = Auction.query

        # Sök på titel
        if keyword:
            search = f"%{keyword.strip()}%"
            query = query.filter(Auction.title.ilike(search))

        if category_keyword:
            cat_like = f"%{category_keyword.strip()}%"
            query = query.filter(Auction.category.ilike(cat_like))

        # Prisfilter
        if min_price is not None:
            query = query.filter(Auction.starting_bid >= min_price)

        if max_price is not None:
            query = query.filter(Auction.starting_bid <= max_price)

        # Sluttid
        if ends_before is not None:
            query = query.filter(Auction.end_at <= ends_before)

        # Sortera så att auktioner som slutar snart visas först
        return query.order_by(Auction.end_at.asc()).all()

# Skapar en instans av AuctionRepo
auction_repo = AuctionRepo()