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
    
    def create_auction(self, title, description, category, starting_bid, end_at, image_url=None):
        new_auction = Auction(
            title=title,
            description=description,
            category=category,
            starting_bid=starting_bid,
            end_at=end_at,
            image_url=image_url
        )
        db.session.add(new_auction)
        db.session.commit()
        return new_auction

    def update(self, auction_id, auction_data):
        """
        Uppdaterar en BEFINTLIG bostad (UPDATE-operation).
        Använder nu db.session.get() för att hämta bostaden.
        # Motsvarande SQL-fråga (exekveras vid db.session.commit()):
            # UPDATE bostad SET adress=?, stad=?, pris=?, rum=?, yta=?, beskrivning=?
            # WHERE bostad.id = ?;

        Returns:
            Bostad: Den uppdaterade bostaden, eller None om den inte fanns.
        """
        # Hämta det befintliga objektet med den moderna metoden.
        auction = db.session.get(Auction, auction_id)

        if auction:
            # Uppdatera fälten på Python-objektet.
            auction.title = auction_data['title']
            auction.description = auction_data['description']
            auction.category = auction_data['category']
            auction.starting_bid = auction_data['starting_bid']
            auction.end_at = auction_data['end_at']
            auction.image_url = auction_data['image_url']

            # Commit sparar ändringarna (UPDATE) till databasen.
            db.session.commit()

        return auction
    
    def delete(self, auction_id):
        
        auction = db.session.get(Auction, auction_id)

        if auction:
            db.session.delete(auction)
            db.session.commit()
            return True

        return False
    
    def search(self, keyword=None, min_price=None, max_price=None, ends_before=None):
        """
        Söker och filtrerar auktioner baserat på användarens val.
        - keyword: sökord i titel
        - min_price / max_price: prisintervall (startpris)
        - ends_before: visa auktioner som slutar före ett visst datum
        """

        query = Auction.query

        # Sök på titel
        if keyword:
            search = f"%{keyword.strip()}%"
            query = query.filter(Auction.title.ilike(search))

        # Prisfilter (startpris)
        if min_price is not None:
            query = query.filter(Auction.starting_bid >= min_price)

        if max_price is not None:
            query = query.filter(Auction.starting_bid <= max_price)

        # Sluttid
        if ends_before is not None:
            query = query.filter(Auction.end_at <= ends_before)

        # Sortera så att auktioner som slutar snart visas först
        return query.order_by(Auction.end_at.asc()).all()


auction_repo = AuctionRepo()