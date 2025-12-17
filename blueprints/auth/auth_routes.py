from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth_bp
from dbrepository.user_repo import user_repo


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Visar inloggningsformuläret (GET) eller behandlar inloggningsförsöket (POST).
    """

    if request.method == 'POST':
        # Hämta data från formuläret
        username = request.form['username']
        password = request.form['password']

        # 1. AUTENTISERING: Hämta användaren via unikt användarnamn
        user = user_repo.get_user_username(username=username)

        # Jämför: Kontrollera om användaren finns OCH om lösenordet matchar
        # OBS! I en riktig app ska lösenordsjämförelsen ske mot det HASHADE lösenordet.
        if user and user.password == password:

            # Autentisering lyckades så vi loggar in användaren med hjälp av flask_logins login_user funktion
            login_user(user)
            # A. Hämta 'next' destinationen från URL query-strängen.
            # så man hamnar tillbaka till den sida som krävde inloggningen. tex
            next_page = request.args.get('next')
            # B. PRIORITET: Omdirigera till den sida som användaren försökte nå (next_page).
            #    Om 'next' saknas, skicka till en neutral startsida ('index' är bäst).
            redirect_url = next_page or url_for('auctions_bp.auctions_list')

            flash(f'Inloggning lyckades! Välkommen tillbaka.', 'success')
            return redirect(redirect_url)
        else:
            # Autentisering misslyckades
            flash('Felaktigt användarnamn eller lösenord.', 'error')

    # Om metoden är GET (eller om POST misslyckades), visa login formuläret.
    return render_template('login.html')

@auth_bp.route('/logout')

@login_required # Man måste vara inloggad för att kunna logga ut
def logout():

    """
    Loggar ut den aktuella användaren och rensar sessionen.
    """

    # Flask-Login raderar användarsessionen
    logout_user()
    flash('Du har loggats ut.', 'info')
    # Omdirigera tillbaka till inloggningssidan
    return redirect(url_for('auth_bp.login'))

###############____init__.py
# myblueprints/auth/__init__.py
"""
 AUTH BLUEPRINT - Initialiseringsfil (Instruktioner för att starta autentiseringsmodulen)

SYFTE: Att definiera en isolerad del av applikationen som hanterar all autentisering
och användarhantering (login, logout, registrering).

SINGLE RESPONSIBILITY: Denna fil har ENDAST ansvar för:
1. Definiera auth-blueprintet.
2. Importera nödvändigt repository (user_repo).
3. Importera routes (URL-hanterarna) som tillhör autentiseringen.
"""
# Importera Blueprint-klassen från Flask
from flask import Blueprint
