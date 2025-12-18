from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import admin_bp
from dbrepository.auction_repo import auction_repo
from dbrepository.bid_repo import bid_repo
from datetime import datetime

def is_admin():
    return current_user.is_authenticated and current_user.role == 'admin'

def validate_form(form_data):
    """
    Hanterar validering, rensning och typkonvertering av formulärdata.
   
    Returns: Validerad data (dict), eller None om något misslyckas.
    """
    try:
        # 1. Hämta och konvertera data till rätt Python-typer
        data = {
            'title': form_data.get('title', '').strip(),
            'description': form_data.get('description', '').strip(),
            'category': form_data.get('category', '').strip(),
            'starting_bid': float(form_data.get('starting_bid', '').strip()),
            'end_at': datetime.strptime(form_data['end_at'], "%Y-%m-%dT%H:%M"),
            'image_url': form_data.get('image_url', '').strip()
        }

        # 2. Enkel Affärsvalidering (kontrollera att data är giltig)
        if not data['title'] or not data['description'] or not data['category'] or not data['starting_bid'] or not data['end_at']:
            return None # Kräver åtminstone ett av dessa fält ifyllda
        # Lägg till fler valideringar här, t.ex. pris är ett nummer etc.

        return data

    except (KeyError, ValueError):
        # Fångar fel om int() konverteringen misslyckas (om t.ex. 'rum' inte var ett nummer)
        return None

@admin_bp.route('/admin/auctions')
@login_required
def admin_auctions_list():
    if not is_admin():
        flash("Access denied.", "danger")
        return redirect(url_for('auctions_bp.auctions_list'))

    auctions = auction_repo.get_all_auctions()
    return render_template('admin_auctions_list.html', auctions=auctions)


@admin_bp.route('/add', methods=['GET', 'POST'])
@admin_bp.route('/edit/<int:auction_id>', methods=['GET', 'POST'])
@login_required
def admin_form(auction_id=None):
    """
    Hanterar logiken för att lägga till (CREATE) eller redigera (UPDATE) en bostad.
    Båda operationerna använder samma formulär och funktion.
    """
    # Steg 1: Säkerhetskontroll
    if not is_admin():
        flash('Access denied: You must be an administrator.', 'danger')
        return redirect(url_for('auctions_bp.auctions_list'))

    auction_edit = None
    title = "Add new auction"

    # A. Förbered för Redigering (Om auction_id finns i URL:en)
    if auction_id:
        # Använd den inbyggda 404-kontrollen i Repository-lagret
        auction_edit = auction_repo.get_auction_by_id(auction_id)
        title = f"Edit: {auction_edit.title}"
   
    # B. POST-förfrågan (Formulär inskickat)
    if request.method == 'POST':
        form_data = validate_form(request.form)

        if form_data is None:
            # Validering misslyckades
            flash('Wrong data type or missing fields. Please check your input.', 'warning')
            # Återgå till formuläret utan redirect, så att felmeddelandet visas.            
        else:
            # Validering lyckades: Dags att spara till DB
            if auction_id:
                # UPDATE: Anropa Repository-uppdatering
                auction_repo.update(auction_id, form_data)

                flash(f'Auction "{form_data["title"]}" has been updated!', 'success')
            else:
                # CREATE: Anropa Repository för att skapa ny
                new_auction = auction_repo.create_auction(
                    title=form_data['title'],
                    description=form_data['description'],
                    category=form_data['category'],
                    starting_bid=form_data['starting_bid'],
                    end_at=form_data['end_at'],
                    image_url=form_data['image_url'] if form_data['image_url'] else None)
                
                flash(f'New auction "{new_auction.title}" has been added!', 'success')
            # PRG-mönstret: Omdirigera till listan efter POST
            return redirect(url_for('admin_bp.admin_auctions_list')) # behövs inget blueprint objekt före punkten (admin_bp.xxx) då den letar efter funktionen i den Blueprint du just nu befinner dig i.

    # C. GET-förfrågan (Visa formulär)
    # Skickar objektet för att fylla i formuläret i redigeringsläge, annars skickas None
    return render_template(
        'admin_auction_form.html',
        auction=auction_edit,
        title=title
    )

@admin_bp.route('/delete/<int:auction_id>', methods=['POST'])
@login_required
def admin_delete_auction(auction_id):
    if not is_admin():
        flash("Access denied.", "danger")
        return redirect(url_for('auctions_bp.auctions_list'))

    auction = auction_repo.get_auction_by_id(auction_id)
    if auction:
        auction_repo.delete(auction_id)
        flash(f'Auction "{auction.title}" has been deleted.', 'success')
    else:
        flash('Auction not found.', 'warning')

    return redirect(url_for('admin_bp.admin_auctions_list'))

        