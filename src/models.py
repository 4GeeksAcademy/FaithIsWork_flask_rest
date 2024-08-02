from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define the User model
class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    favorites = db.relationship('Favorite', backref='user')

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, it's a security breach
        }

# Define the Planet model
class Planet(db.Model):
    __tablename__ = "planet"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    favorites = db.relationship('Favorite', backref='planet', )

# Define the Person model
class People(db.Model):  # Changed to Person for consistency
    __tablename__ = "people"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    favorites = db.relationship('Favorite', backref='people')

# Define the Favorite model
class Favorite(db.Model):
    __tablename__ = "favorite"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)
  
    
    