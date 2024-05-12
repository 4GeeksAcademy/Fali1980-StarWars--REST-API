from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    # favorite_characters = db.relationship('Favorites_characters', backref='users', lazy=True)
    # favorite_planets = db.relationship('Favorites_planets', backref='users', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "esta_vivo": self.is_active,
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable = False)
    height = db.Column(db.String(250), nullable = False)
    # favorites_characters = db.relationship('Favorites_characters', backref='character')

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "height": self.height,
            # do not serialize the password, its a security breach
        }
    
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    diameter= db.Column(db.String(250), nullable=False)
    rotation_period = db.Column(db.String(250), nullable = False)
    climate = db.Column(db.String(250), nullable = False)
    # favorites_planets = db.relationship('Favorites_planets', backref='planet')

    def __repr__(self):
        return '<Planet %r>' % self.diameter

    def serialize(self):
        return {
            "id": self.id,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "climate": self.climate,
            # do not serialize the password, its a security breach
        }
    
class Favorites_characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    characters_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     # character = db.relationship('Character', backref='favorites')
    user = db.relationship('User', backref='favorite_characters')

#     def __repr__(self):
#         return '<Favorites_characters %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "characters_id": self.characters_id,
            "user_id": self.user_id,
            # do not serialize the password, its a security breach
        }


class Favorites_planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planets_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     # planet = db.relationship('Planet', backref='favorites')
#     # user = db.relationship('User', backref='favorite_planets')

#     def __repr__(self):
#         return '<Favorites_planets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "planets_id": self.planets_id,
            "user_id": self.user_id,
            # do not serialize the password, its a security breach
        }