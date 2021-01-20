from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    collegeid = db.Column(db.String(20), unique=True, nullable=False)
    profession = db.Column(db.String(20), unique=True, nullable=False)
    userloginid = db.Column(db.String(20), unique=True, nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.firstname}', '{self.lastname}', '{self.email}', '{self.image_file}', '{self.collegeid}', '{self.profession}', '{self.userloginid}')"

class Details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userloginid = db.Column(db.String(20), unique=True, nullable=False)
    gender = db.Column(db.String(20))
    course = db.Column(db.String(20))
    degree = db.Column(db.String(20))
    country = db.Column(db.String(20))
    intrest1 = db.Column(db.String(20))
    intrest2 = db.Column(db.String(20))
    intrest3 = db.Column(db.String(20))
    intrest4 = db.Column(db.String(20))
    intrest5 = db.Column(db.String(20))
    lnkdurl = db.Column(db.String(20))
    ghuburl = db.Column(db.String(20))

    def __repr__(self):
        return f"Details('{self.userloginid}', '{self.firstname}', '{self.lastname}', '{self.gender}', '{self.course}', '{self.degree}', '{self.country}', '{self.intrest1}', '{self.intrest2}', '{self.intrest3}', '{self.intrest4}', '{self.intrest5}', '{self.lnkdurl}', '{self.ghuburl}')"

class Projects(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    userloginid = db.Column(db.String(20), unique=False, nullable=False)
    projecttitle = db.Column(db.String(20))
    pmetadata = db.Column(db.String(20))
    pdescription = db.Column(db.String(20))
    name = db.Column(db.String(300))
    data = db.Column(db.LargeBinary)


    def __repr__(self):
        return f"Details('{self.id}', '{self.userloginid}', '{self.projecttitle}', '{self.pmetadata}', '{self.pdescription}', '{self.name}', '{self.data}' )"


class Intrested(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    userloginid = db.Column(db.String(20), unique=False, nullable=False)
    projectid = db.Column(db.String(20), unique=False, nullable=False)
    intrestflag = db.Column(db.Boolean, default=False, nullable=False)


    def __repr__(self):
        return f"Details('{self.id}', '{self.userloginid}', '{self.projectid}', '{self.intrestflag}') "
