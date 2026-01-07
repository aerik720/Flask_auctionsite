from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import admin_bp
from dbrepository.auction_repo import auction_repo
from dbrepository.bid_repo import bid_repo
from datetime import datetime
from dbrepository.reactions_repo import reactions_repo

# Kontrollera om nuvarande användare är admin
def is_admin():
    return current_user.is_authenticated and current_user.role == 'admin'

# Validera formulärdata
def validate_form(form_data):
    
    try:
        # Hämta och rensa formulärdata
        data = {
            'title': form_data.get('title', '').strip(),
            'description': form_data.get('description', '').strip(),
            'category': form_data.get('category', '').strip(),
            'starting_bid': float(form_data.get('starting_bid', '').strip()),
            'end_at': datetime.strptime(form_data['end_at'], "%Y-%m-%dT%H:%M"),
            'image_url': form_data.get('image_url', '').strip()
        }

        # Kontrollera att nödvändiga fält är rätt ifyllda
        if not data['title'] or not data['description'] or not data['category'] or not data['starting_bid'] or not data['end_at']:
            return None # Kräver åtminstone ett av dessa fält ifyllda

        return data

    except (KeyError, ValueError):
        # Fångar fel vid konvertering av data
        return None

# Rutt för att visa alla auktioner i adminpanelen
@admin_bp.route('/admin/auctions')
@login_required # Ingen åtkomst utan inloggnings
# Visa alla auktioner i adminpanelen
def admin_auctions_list():
    # Säkerhetskontroll att användaren är admin
    if not is_admin():
        flash("Access denied.", "danger")
        return redirect(url_for('auctions_bp.auctions_list'))

    # Hämta alla auktioner
    auctions = auction_repo.get_all_auctions()
    return render_template('admin_auctions_list.html', auctions=auctions)

# Rutt för att lägga till eller redigera en auktion
@admin_bp.route('/add', methods=['GET', 'POST'])
@admin_bp.route('/edit/<int:auction_id>', methods=['GET', 'POST'])
@login_required
def admin_form(auction_id=None):

    # Säkerhetskontroll
    if not is_admin():
        flash('Access denied: You must be an administrator.', 'danger')
        return redirect(url_for('auctions_bp.auctions_list'))

    # Variabler för formuläret
    auction_edit = None
    title = "Add new auction"
    # Tomt lista för budhistorik
    history = []
    # Om det är en redigering (Auction ID finns), hämta objektet
    if auction_id:
        # Hämta auktionen för redigering
        auction_edit = auction_repo.get_auction_by_id(auction_id)
        # Ändra titeln för redigeringsläge
        title = f"Edit: {auction_edit.title}"
        history = auction_repo.get_bidding_history(auction_id)
        # Hämta likes och dislikes för auktionen
        likes = reactions_repo.count(auction_id, "like")
        dislikes = reactions_repo.count(auction_id, "dislike")
    else:
        # Ny auktion, sätt likes och dislikes till 0
        likes = 0
        dislikes = 0

   
    # Om det är en POST-förfrågan
    if request.method == 'POST':
        # Hämta och validera formulärdata
        form_data = validate_form(request.form)

        if form_data is None:
            # Validering misslyckades
            flash('Wrong data type or missing fields. Please check your input.', 'warning')
            # Återgå till formuläret utan redirect, så att felmeddelandet visas.            
        else:
            # Om validering lyckades
            if auction_id:
                # Uppdatera befintlig auktion med Repository
                auction_repo.update(auction_id, form_data)

                flash(f'Auction "{form_data["title"]}" has been updated!', 'success')
            else:
                # Annars skapa ny auktion med Repository med formulärdata
                new_auction = auction_repo.create_auction(
                    title=form_data['title'],
                    description=form_data['description'],
                    category=form_data['category'],
                    starting_bid=form_data['starting_bid'],
                    end_at=form_data['end_at'],
                    image_url=form_data['image_url'] if form_data['image_url'] else None)
                
                flash(f'New auction "{new_auction.title}" has been added!', 'success')
            
            # Omdirigera tillbaka till admin auktion listan efter lyckad skapande eller uppdatering
            return redirect(url_for('admin_bp.admin_auctions_list'))

    return render_template(
    "admin_auction_form.html",
    auction=auction_edit,
    title=title,
    history=history,
    likes=likes,
    dislikes=dislikes
    
)

# Rutter likes uppåt
@admin_bp.route("/edit/<int:auction_id>/likes/plus", methods=["POST"])
@login_required # Kräver inloggning
def admin_likes_plus(auction_id):
    # Säkerhetskontroll
    if not is_admin():
        flash("Access denied.", "danger")
        return redirect(url_for("auctions_bp.auctions_list"))

    # Öka antalet likes med 1
    reactions_repo.add(auction_id, "like")
    return redirect(url_for("admin_bp.admin_form", auction_id=auction_id))

# Rutter likes nedåt
@admin_bp.route("/edit/<int:auction_id>/likes/minus", methods=["POST"])
@login_required # Kräver inloggning
def admin_likes_minus(auction_id):
    # Säkerhetskontroll
    if not is_admin():
        flash("Access denied.", "danger")
        return redirect(url_for("auctions_bp.auctions_list"))
    
    # Minska antalet likes med 1
    reactions_repo.remove(auction_id, "like")
    return redirect(url_for("admin_bp.admin_form", auction_id=auction_id))

# Rutt dislikes uppåt
@admin_bp.route("/edit/<int:auction_id>/dislikes/plus", methods=["POST"])
@login_required # Kräver inloggning
def admin_dislikes_plus(auction_id):
    # Säkerhetskontroll
    if not is_admin():
        flash("Access denied.", "danger")
        return redirect(url_for("auctions_bp.auctions_list"))

    # Öka antalet dislikes med 1
    reactions_repo.add(auction_id, "dislike")
    return redirect(url_for("admin_bp.admin_form", auction_id=auction_id))

# Rutt dislikes nedåt
@admin_bp.route("/edit/<int:auction_id>/dislikes/minus", methods=["POST"])
@login_required # Kräver inloggning
def admin_dislikes_minus(auction_id):
    # Säkerhetskontroll
    if not is_admin():
        flash("Access denied.", "danger")
        return redirect(url_for("auctions_bp.admin_form", auction_id=auction_id))
    
    # Minska antalet dislikes med 1
    reactions_repo.remove(auction_id, "dislike")
    return redirect(url_for("admin_bp.admin_form", auction_id=auction_id))

# Rutt för att ta bort en auktion
@admin_bp.route('/delete/<int:auction_id>', methods=['POST'])
@login_required # Kräver inloggning
def admin_delete_auction(auction_id):
    # Säkerhetskontroll
    if not is_admin():
        flash("Access denied.", "danger")
        return redirect(url_for('auctions_bp.auctions_list'))

    # Hämta auktionen baserat på ID
    auction = auction_repo.get_auction_by_id(auction_id)
    # Om auktionen finns, ta bort den
    if auction:
        auction_repo.delete(auction_id)
        flash(f'Auction "{auction.title}" has been deleted.', 'success')
    else:
        flash('Auction not found.', 'warning')

    return redirect(url_for('admin_bp.admin_auctions_list'))

# Rutt för att ta bort ett bud på en auktion
@admin_bp.route('/delete_bid/<int:bid_id>', methods=['POST'])
@login_required # Kräver inloggning
def admin_delete_bid(bid_id):
    # Säkerhetskontroll
    if not is_admin():
        flash("Access denied.", "danger")
        return redirect(url_for('auctions_bp.auctions_list'))
    # Hämta budet baserat på ID
    bid = bid_repo.get_bid_by_id(bid_id)

    auction_id = bid.auction_id
    if bid:
        # Ta bort budet
        bid_repo.delete_bid(bid_id)
        flash(f'Bid for this auction has been deleted.', 'success')
    else:
        flash('Auction not found.', 'warning')
    # Omdirigera tillbaka till admin formuläret för den auktionen
    return redirect(url_for('admin_bp.admin_form', auction_id=auction_id))

