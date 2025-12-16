from database import db
from models.reaction import Reaction

class ReactionRepo:
    def count(self, auction_id, kind):
        return Reaction.query.filter_by(auction_id=auction_id, kind=kind).count()
    
    def add(self, auction_id, kind):
        reaction = Reaction(auction_id=auction_id, kind=kind)
        db.session.add(reaction)
        db.session.commit()
    
reactions_repo = ReactionRepo()