from flask import Blueprint
from dbrepository.auction_repo import auction_repo

# Skapar en Blueprint för auktioner
auctions_bp = Blueprint(
    'auctions_bp',
    __name__,
    url_prefix='/auctions',
    template_folder="templates")

from . import auctions_routes