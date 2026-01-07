from flask_login import UserMixin
from database import db

# Användarmodell för databasen
class User(db.Model, UserMixin):
    # Namn på tabellen i databasen
    __tablename__ = 'users'

    # Kolumner i tabellen
    id = db.Column(db.Integer, primary_key=True)

    # Gör kolumner för användarnamn, password, email och roll
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')

    # Få användarens ID för Flask-Login i strängformat
    def get_id(self):
        return str(self.id)

    # Visar användarens information för debugging
    def __repr__(self):
        return f"<User {self.username} ({self.role})>"
    
# Startdata för användare
STARTDATA_USERS = [
    {'username': 'Anton', 'password': '1234', 'email': 'anton@gmail.com', 'role': 'admin'},
    {'username': 'Liam', 'password': '12345', 'email': 'liam@du.se', 'role': 'user'}
]

# Fyller på databasen med startanvändare om tabellen är tom
def makestartusers():
    totalusers = User.query.count()
    if totalusers != 0:
        print(f"The table already have {totalusers} users in the database.")
        return
    
    # Lägg till startanvändare
    for user_data in STARTDATA_USERS:
        newuser = User(
            username=user_data['username'],
            password=user_data['password'],
            email=user_data['email'],
            role=user_data['role']
        )
        db.session.add(newuser)

    # Spara ändringarna i databasen
    db.session.commit()
    print(f"Added {len(STARTDATA_USERS)} users to the database.")