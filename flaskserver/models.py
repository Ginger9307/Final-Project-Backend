from flaskserver import db, ma

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable = False)
    email = db.Column(db.String(120), unique=True, nullable = False)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    car = db.relationship('Car', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.name}')"

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(20), nullable=False)
    maker = db.Column(db.String(20), nullable=False)
    reg_num = db.Column(db.String(8), nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Car('{self.model}', '{self.maker}', '{self.seats}')"

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

