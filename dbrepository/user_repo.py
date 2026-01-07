from database import db
from models.user import User

# Repository för användarhantering
class UserRepository:
    # Hämtar en användare baserat på användarnamn
    def get_user_username(self, username):
        user = User.query.filter_by(username=username).first()
        return user
    
    # Hämtar alla användare
    def get_all(self):
        return User.query.all()

    # Hämtar en användare baserat på ID
    def get_user(self, user_id):
        return User.query.get(user_id)

    # Hämtar en användare baserat på ID eller returnerar 404 om inte hittad
    def get_user_or_404(self, user_id):
        return User.query.get_or_404(user_id)
    
    # Hämtar en användare baserat på användarnamn
    def get_user_username(self, username):
        user = User.query.filter_by(username=username).first()

        if user:
            return user
        return None # Returnerar None om inte användaren finns

    # Skapar en ny användare
    def create_user(self, data):
        # Skapa en ny instans av User-modellen.
        new_user = User(
            username=data['username'],
            password=data['password'],
            roll=data['role'],
        )

        # Lägg till i sessionen
        db.session.add(new_user)
        # Spara permanent i databasen
        db.session.commit()

        return new_user

    # Uppdaterar en befintlig användare
    def update_user(self, user_id, data):
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

    # Tar bort en användare baserat på ID
    def delete_user(self, user_id):
        user = User.query.get(user_id)
        # Om användaren finns, ta bort den
        if user:
            db.session.delete(user)
            db.session.commit()
            return True

        return False


# Skapa instans av repository
user_repo = UserRepository()
