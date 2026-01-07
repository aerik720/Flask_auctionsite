from flask import render_template, request, redirect, url_for, flash
from dbrepository.bid_repo import bid_repo
from dbrepository.reactions_repo import reactions_repo
from . import auctions_bp, auction_repo
from flask_login import login_required, current_user
from datetime import datetime


@auctions_bp.route('/')
def auctions_list():
    keyword = request.args.get("q", "").strip()
    category_keyword = request.args.get("category", "").strip()

    def to_float(value):
        try:
            return float(value) if value else None
        except ValueError:
            return None

    def to_datetime(value):
        try:
            return datetime.strptime(value, "%Y-%m-%dT%H:%M") if value else None
        except ValueError:
            return None

    min_price = to_float(request.args.get("min_price"))
    max_price = to_float(request.args.get("max_price"))
    ends_before = to_datetime(request.args.get("ends_before"))

    auctions = auction_repo.search(
        keyword=keyword or None,
        category_keyword=category_keyword or None,
        min_price=min_price,
        max_price=max_price,
        ends_before=ends_before
    )

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

@auctions_bp.route('/<int:auction_id>')
def auctions_detail(auction_id):
    auction = auction_repo.get_auction_by_id(auction_id)
    
    top2 = bid_repo.get_top_2(auction_id)
    history = auction_repo.get_bidding_history(auction_id)
    current_max = top2[0].amount if top2 else auction.starting_bid
    

    likes = reactions_repo.count(auction_id, kind='like')
    dislikes = reactions_repo.count(auction_id, kind='dislike')

    return render_template('auctions_detail.html', auction=auction, history=history, top2=top2, current_max=current_max, likes=likes, dislikes=dislikes)

@auctions_bp.route("/<int:auction_id>/bid", methods=["POST"])
@login_required
def place_bid(auction_id):
    auction = auction_repo.get_auction_by_id(auction_id)
    if request.form.get("email_radio_option") == "false":
        bidder_email = request.form.get("bidder_email")
    else:
        bidder_email = current_user.email

    amount = int(request.form.get("amount"))

    top2 = bid_repo.get_top_2(auction_id)
    current_max = top2[0].amount if top2 else auction.starting_bid

    if amount <= current_max:
        flash(f"Bid needs to be higher than current bid ({current_max}).", "warning")
        return redirect(url_for("auctions_bp.auctions_detail", auction_id=auction_id))

    bid_repo.place_bid(auction_id, bidder_email, amount)
    
    return redirect(url_for("auctions_bp.auctions_detail", auction_id=auction_id))

@auctions_bp.route("/<int:auction_id>/react", methods=["POST"])
def react(auction_id):
    kind = request.form.get("kind")

    reactions_repo.add(auction_id, kind)
    return redirect(url_for("auctions_bp.auctions_detail", auction_id=auction_id))