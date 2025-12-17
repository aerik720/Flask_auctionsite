from database import db
from models.user import User

class UserRepository:
    def get_user_username(self, username):
        user = User.query.filter_by(username=username).first()
        return user
    
    def get_all(self):
        """
        Hämtar ALLA användare från databasen.

        Returns:
            list: Lista med alla User-objekt.
        """
        return User.query.all()

    def get_user(self, user_id):
        """
        Hämtar EN specifik användare baserat på ID (Primärnyckel).

        Args:
            user_id (int): ID för användaren.

        Returns:
            User: User-objektet, eller None om det inte finns.
        """
        return User.query.get(user_id)

    def get_user_or_404(self, user_id):
        """
        Hämtar EN användare eller utlöser 404-fel. Användbar för admin-gränssnitt.

        Args:
            user_id (int): ID för användaren.

        Returns:
            User: User-objektet (garanterat att existera).
        """
        return User.query.get_or_404(user_id)

    def get_user_username(self, username):
        """
        Hämtar EN användare baserat på dess UNIKA användarnamn.
        Detta är den primära sökmetoden som används vid inloggning.

        Args:
            username (str): Användarnamnet att söka efter.

        Returns:
            User: User-objektet, eller None om användarnamnet inte hittas.
        """
        # 1. .filter_by(username=username): Lägger till villkoret WHERE username = '...'
        # 2. .first(): Exekverar frågan och returnerar ENDAST det första matchande resultatet.
        #    (Detta förutsätter att 'username' är unikt i databasen.)
        user = User.query.filter_by(username=username).first()

        if user:
            return user
        return None # Returnerar None explicit om ingen användare hittades.

    def create_user(self, data):
        """
        Skapar en NY användare i databasen (INSERT).

        Args:
            data (dict): Dictionary med user-information (username, password, role).

        Returns:
            User: Den nya User-instansen.
        """
        # Skapa en ny instans av User-modellen.
        new_user = User(
            username=data['username'],
            # VIKTIGT: Fältet 'password' bör vara hashat och saltat av en annan funktion
            # INNAN det når detta lager. Här sparas bara det värde som skickas in.
            password=data['password'],
            # 'role' används ofta för behörighetskontroll (t.ex. 'admin', 'standard').
            roll=data['role'],
        )

        # 1. Lägg till i session.
        db.session.add(new_user)
        # 2. Commit: Spara permanent.
        db.session.commit()

        return new_user

    def update_user(self, user_id, data):
        """
        Uppdaterar en BEFINTLIG användare (UPDATE-operation).

        Args:
            user_id (int): ID för användaren att uppdatera.
            data (dict): Ny data.

        Returns:
            User: Den uppdaterade användaren, eller None.
        """
        user = User.query.get(user_id)

        if user:
            # Uppdatera alla fält på objektet.
            user.username = data['username']
            # Uppdatera lösenord (OBS: data['password'] måste vara det nya hashede värdet)
            user.password = data['password']
            user.role = data['role']

            # Spara ändringarna
            db.session.commit()

        return user

    def delete_user(self, user_id):
        """
        Raderar en användare från databasen (DELETE).

        Args:
            user_id (int): ID för användaren att radera.

        Returns:
            bool: True om radering lyckades, False om användaren inte fanns.
        """
        user = User.query.get(user_id)

        if user:
            db.session.delete(user)
            # Commit: Utför DELETE.
            db.session.commit()
            return True

        return False


# Skapa EN instans av repository som kan användas överallt
user_repo = UserRepository()
