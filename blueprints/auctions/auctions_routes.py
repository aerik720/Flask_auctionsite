from flask import render_template, request, redirect, url_for, flash
from dbrepository.bid_repo import bid_repo
from dbrepository.reactions_repo import reactions_repo
from . import auctions_bp, auction_repo
from flask_login import login_required, current_user


@auctions_bp.route('/')
def auctions_list():
    auctions = auction_repo.get_all_auctions()
    return render_template('auctions_list.html', auctions=auctions)

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
    bidder_email = request.form.get("bidder_email")

    amount = int(request.form.get("amount"))

    # enkel regel: måste vara > max(befintligt) och >= starting_bid
    top2 = bid_repo.get_top_2(auction_id)
    current_max = top2[0].amount if top2 else auction.starting_bid

    if amount <= current_max:
        flash(f"Budet måste vara högre än nuvarande max ({current_max}).", "warning")
        return redirect(url_for("auctions_bp.auctions_detail", auction_id=auction_id))

    bid_repo.lagg_bud(auction_id, bidder_email, amount)
    
    return redirect(url_for("auctions_bp.auctions_detail", auction_id=auction_id))

@auctions_bp.route("/<int:auction_id>/react", methods=["POST"])
def react(auction_id):
    kind = request.form.get("kind")

    reactions_repo.add(auction_id, kind)
    return redirect(url_for("auctions_bp.auctions_detail", auction_id=auction_id))