from database import db
from models.reaction import Reaction

# Repository för hantering av reaktioner
class ReactionRepo:
    # Räknar antalet reaktioner av en viss typ för en auktion
    def count(self, auction_id, kind):
        return Reaction.query.filter_by(auction_id=auction_id, kind=kind).count()
    
    # Lägger till en ny like eller dislike för en auktion
    def add(self, auction_id, kind):
        reaction = Reaction(auction_id=auction_id, kind=kind)
        db.session.add(reaction)
        db.session.commit()

    # Tar bort en reaktion av en viss typ för en auktion
    def remove(self, auction_id, kind):
        # Ta bort en rad
        reaction = (Reaction.query
             .filter_by(auction_id=auction_id, kind=kind)
             .order_by(Reaction.id.desc())
             .first())
        if reaction:
            db.session.delete(reaction)
            db.session.commit()
    
# Skapar en instans av ReactionRepo för användning i applikationen
reactions_repo = ReactionRepo()