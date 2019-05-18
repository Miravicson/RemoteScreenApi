from app import db
from passlib.hash import pbkdf2_sha256 as sha256


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=True)
    last_name = db.Column(db.String(120), nullable=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password, first_name='', last_name=''):
        self.username = username
        self.password = password
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def return_all(cls):
        def to_json(user):
            return {"first_name": user.first_name, "last_name": user.last_name, "username": user.username}
        return list(map(lambda user: to_json(user), cls.query.all()))

    @classmethod
    def delete_all(cls):
        try:
            number_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {"message": f"{number_deleted} row(s) has been deleted."}
        except:
            return {"message": "Something went wrong"}

    @staticmethod
    def hash_password(password):
        return sha256.hash(password)

    @staticmethod
    def verify_password(password, hash):
        return sha256.verify(password, hash)


class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(140))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)
