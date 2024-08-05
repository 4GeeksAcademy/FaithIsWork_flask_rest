from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

# Define the User model
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True) # Name column with VARCHAR(80)
    email = db.Column(db.String(80), unique=True, nullable=False)  # Email column with unique constraint
    password = db.Column(db.String(80), nullable=False)  # Password column
    favorites = relationship('Favorite', backref='user')  # Define relationship to Favorite


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            # do not serialize the password, it's a security breach
           
        }

# Define the Planet model
class Planet(db.Model):
    __tablename__ = "planet"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    favorites = relationship('Favorite', backref='planet', )


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
           
        }

# Define the Person model
class People(db.Model):  # Changed to Person for consistency
    __tablename__ = "people"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    favorites = relationship('Favorite', backref='people', )
   

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            
        }

# Define the Favorite model
class Favorite(db.Model):
    __tablename__ = "favorite"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "user.id": self.user_id,
            "planet.id": self.planet_id,
            "people.id": self.people_id,
        }