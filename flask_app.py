from flask import Flask, redirect, url_for, render_template
from database import db
from blueprints.auth import auth_bp
from blueprints.auctions import auctions_bp
from models.auction import Auction
from datetime import datetime, timedelta
from models.user import User, makestartusers
from flask_login import LoginManager


app = Flask(__name__)
app.config["SECRET_KEY"] = "dev"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///auction.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
app.register_blueprint(auctions_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')

@app.route('/')
def home():
    return redirect(url_for("auctions_bp.auctions_list"))

def if_empty_auctiondb():
    if Auction.query.count() > 0:
        return
    
    now = datetime.now()
    db.session.add_all([
        Auction(title="Vintage Clock", description="An old vintage clock from 1920s.", category="Antiques", starting_bid=50.0, end_at=now + timedelta(days=7)),
        Auction(title="Antique Vase", description="A beautiful antique vase.", category="Antiques", starting_bid=100.0, end_at=now + timedelta(days=30)),
        Auction(title="Painting by Unknown Artist", description="A mysterious painting with no known artist.", category="Antiques", starting_bid=200.0, end_at=now + timedelta(days=60))
    ])
    db.session.commit()


with app.app_context():
    db.create_all()
    if_empty_auctiondb()
    makestartusers()

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = 'auth_bp.login'

@login_manager.user_loader

def load_user(user_id):

    """Laddar en användare från databasen baserat på ID:t i sessionen."""

    return User.query.get(int(user_id))


if __name__ == '__main__':
    app.run(debug=True)