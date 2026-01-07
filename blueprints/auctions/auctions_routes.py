from flask import render_template, request, redirect, url_for, flash
from dbrepository.bid_repo import bid_repo
from dbrepository.reactions_repo import reactions_repo
from . import auctions_bp, auction_repo
from flask_login import login_required, current_user
from datetime import datetime

# Rutt för att visa alla auktioner med filtermöjligheter
@auctions_bp.route('/')
def auctions_list():
    # Hämta filterparametrar
    keyword = request.args.get("q", "").strip()
    # Hämta kategori-filter
    category_keyword = request.args.get("category", "").strip()

    # Funktioner för att konvertera strängar till float
    def to_float(value):
        try:
            return float(value) if value else None
        except ValueError:
            return None

    # Funktion för att konvertera sträng till datetime
    def to_datetime(value):
        try:
            return datetime.strptime(value, "%Y-%m-%dT%H:%M") if value else None
        except ValueError:
            return None

    # Hämta pris- och datumfilter
    min_price = to_float(request.args.get("min_price"))
    max_price = to_float(request.args.get("max_price"))
    ends_before = to_datetime(request.args.get("ends_before"))

    # Hämta auktioner baserat på filter
    auctions = auction_repo.search(
        keyword=keyword or None,
        category_keyword=category_keyword or None,
        min_price=min_price,
        max_price=max_price,
        ends_before=ends_before
    )

    # Rendera mallen med auktioner och aktuella filtervärden
    return render_template(
        "auctions_list.html",
        auctions=auctions,
        filters={
            "q": keyword,
            "category": category_keyword,
            "min_price": request.args.get("min_price", ""),
            "max_price": request.args.get("max_price", ""),
            "ends_before": request.args.get("ends_before", "")
        }
    )

# Rutt för att visa detaljer om en specifik auktion
@auctions_bp.route('/<int:auction_id>')
def auctions_detail(auction_id):
    # Hämta auktionen baserat på ID
    auction = auction_repo.get_auction_by_id(auction_id)
    
    # Hämta topp 2 bud och budhistorik
    top2 = bid_repo.get_top_2(auction_id)
    history = auction_repo.get_bidding_history(auction_id)
    # Bestäm nuvarande högsta bud
    current_max = top2[0].amount if top2 else auction.starting_bid
    
    # Hämta antal likes och dislikes
    likes = reactions_repo.count(auction_id, kind='like')
    dislikes = reactions_repo.count(auction_id, kind='dislike')

    # Rendera mallen med auktionens detaljer
    return render_template('auctions_detail.html', auction=auction, history=history, top2=top2, current_max=current_max, likes=likes, dislikes=dislikes)

# Rutt för att placera ett bud på en auktion
@auctions_bp.route("/<int:auction_id>/bid", methods=["POST"])
@login_required # Kräver inloggning för att placera bud
def place_bid(auction_id):
    # Hämta auktionen baserat på ID
    auction = auction_repo.get_auction_by_id(auction_id)
    # Om radioknappen "Använd min e-post" är avmarkerad, använd det angivna e-postfältet
    if request.form.get("email_radio_option") == "false":
        bidder_email = request.form.get("bidder_email")
    # Annars, använd den inloggade användarens e-post
    else:
        bidder_email = current_user.email

    # Hämta budbeloppet från fältet
    amount = int(request.form.get("amount"))
    # Hämta de två högsta buden för auktionen
    top2 = bid_repo.get_top_2(auction_id)
    # Bestäm nuvarande högsta bud
    current_max = top2[0].amount if top2 else auction.starting_bid

    # Kontrollera att budet är högre än nuvarande högsta bud
    if amount <= current_max:
        flash(f"Bid needs to be higher than current bid ({current_max}).", "warning")
        return redirect(url_for("auctions_bp.auctions_detail", auction_id=auction_id))
    
    # Placera budet
    bid_repo.place_bid(auction_id, bidder_email, amount)
    
    # Omdirigera tillbaka till auktionens detaljsida
    return redirect(url_for("auctions_bp.auctions_detail", auction_id=auction_id))

# Rutt för att like eller dislike på en auktion
@auctions_bp.route("/<int:auction_id>/react", methods=["POST"])
def react(auction_id):
    # Hämta reaktionstypen
    kind = request.form.get("kind")

    # Lägg till reaktionen
    reactions_repo.add(auction_id, kind)
    return redirect(url_for("auctions_bp.auctions_detail", auction_id=auction_id))