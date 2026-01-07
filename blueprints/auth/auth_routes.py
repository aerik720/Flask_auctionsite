from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth_bp
from dbrepository.user_repo import user_repo

# Rutt för inloggning
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Hämta data från formuläret
        username = request.form['username']
        password = request.form['password']

        # Hämta användaren baserat på användarnamn
        user = user_repo.get_user_username(username=username)

        # Verifiera lösenordet 
        if user and user.password == password:
            # Kallar på funktionen för att logga in användaren
            login_user(user)
            # Kolla om 'next' parameter finns i URL:en (den sida användaren försökte nå innan inloggning)
            next_page = request.args.get('next')
            # Om 'next' finns, omdirigera dit, annars till startsidan
            redirect_url = next_page or url_for('auctions_bp.auctions_list')

            flash(f'Inloggning lyckades! Välkommen tillbaka.', 'success')
            return redirect(redirect_url)
        else:
            # Autentisering misslyckades
            flash('Felaktigt användarnamn eller lösenord.', 'error')

    # Om metoden är GET (eller om POST misslyckades), visa login formuläret.
    return render_template('login.html')

@auth_bp.route('/logout')

@login_required # Ingen åtkomst utan inloggning
def logout():
    # Logga ut användaren
    logout_user()
    flash('Du har loggats ut.', 'info')
    # Omdirigera tillbaka till inloggningssidan
    return redirect(url_for('auth_bp.login'))

# Importera Blueprint-klassen från Flask
from flask import Blueprint
