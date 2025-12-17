from flask_login import UserMixin
from database import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')

    def get_id(self):
            """
            Denna metod KRÄVS av Flask-Login.
            Den returnerar användarens ID som en sträng för att hantera sessionen.
            """
            return str(self.id)#måste returnera en sträng

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"
    
    

STARTDATA_USERS = [
    {'username': 'Anton', 'password': '1234', 'email': 'anton@gmail.com', 'role': 'admin'},
    {'username': 'Liam', 'password': '12345', 'email': 'liam@du.se', 'role': 'user'}
]

def makestartusers():
    totalusers = User.query.count()
    if totalusers != 0:
        print(f"The table already have {totalusers} users in the database.")
        return
    
    for user_data in STARTDATA_USERS:
        newuser = User(
            username=user_data['username'],
            password=user_data['password'],
            email=user_data['email'],
            role=user_data['role']
        )
        db.session.add(newuser)

    db.session.commit()
    print(f"Added {len(STARTDATA_USERS)} users to the database.")