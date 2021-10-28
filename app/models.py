from app import db
from flask_login import UserMixin
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from app import login

#step one create tables (model
# make a new database in elephant sql)
# hide in .env

class User(UserMixin, db.Model):
#set columns and what they are
    id= db.Column(db.Integer, primary_key=True)   #create our column
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email =  db.Column(db.String(200),unique=True)     #username need a unique one
    password = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, default=dt.utcnow) #ut universal time zone  always do this


    #give methods to take instance of user class

    def __repr__(self):   #will print out when you print your object
        return f'<User: {self.id} | {self.email}>'

    #McCall = User()
    #print(McCall)

    #data is a dict with username first name last name

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])

        # use hashing for password = takes your string and gives you scrambled combos that = it 
        # use salting that adds a unique string before the hashing so that someone cant undo it 
        # makes it harder to steal passwords

    def hash_password(self, original_password):
        return generate_password_hash(original_password)
    # compares the user password to the password provided in the login form
    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    # saves the user to the database and when you have to change user you need to change this 
    def save(self):
        db.session.add(self) # add the user to the db session
        db.session.commit()  # save everything in session to the database do this LAST



    
@login.user_loader   #this is going to decorate a func- make a func that tells flask login what criteria
                    # we need to get them logged in
def load_user(id):
    return User.query.get(int(id))    #id in table user is = to this id (select from user = USER)
    

# same as(SELECT * FROM user WHERE id = ???)