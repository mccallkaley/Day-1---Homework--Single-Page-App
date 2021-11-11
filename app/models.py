from sqlalchemy.orm import backref
from app import db
from flask_login import current_user,  UserMixin
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from app import login

#step one create tables (model
# make a new database in elephant sql)
# hide in .env


#set columns and what they are
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  #create our column
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(200), unique=True, index=True) #username need a unique one
    password = db.Column(db.String(200))
    icon = db.Column(db.Integer)
    created_on = db.Column(db.DateTime, default=dt.utcnow) #ut universal time zone  always do this
    pokemons = db.relationship('Pokemon', backref='author', lazy='dynamic')

    #give methods to take instance of user class
    def __repr__(self):  #will print out when you print your object
        return f'<User: {self.id} | {self.email}>'


    #McCall = User()
    #print(McCall)

    #data is a dict with username first name last name

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data["email"]
        self.icon = data['icon']
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

    def get_icon_url(self):
        return f'https://avatars.dicebear.com/api/identicon/{self.icon}.svg'

    
@login.user_loader   #this is going to decorate a func- make a func that tells flask login what criteria
                    # we need to get them logged in
def load_user(id):
    return User.query.get(int(id))    #id in table user is = to this id (select from user = USER)
    

# same as(SELECT * FROM user WHERE id = ???)

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)  #create our column
    name =db.Column(db.String(150), unique=True,  index=True)   #unique=True
    base_hp =db.Column(db.Integer) #unique a number so  int
    base_defense =db.Column(db.Integer)
    base_attack =db.Column(db.Integer)
    sprite_url =db.Column(db.String(500))
    date_created = db.Column(db.DateTime, default=dt.utcnow)
    date_updated = db.Column(db.DateTime, onupdate=dt.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #pulls in user id  from user table
    

    def from_dict(self,data):
        self.name = data['name']
        self.base_hp = data['base_hp']    #hit-points of this particular pokemon
        self.base_defense = data['base_defense']
        self.base_attack = data['base_attack']
        self.sprite_url = data['sprite_url']
        self.user_id = current_user.id

        # need to import current_user.id at top from userlogin

    def __repr__(self):
        return f'<id:{self.id} | Post: {self.name}>'

 # saves the Post to the database (the pokemon)
    def save(self):
        db.session.add(self) # add the Post to the db session
        db.session.commit() #save everything in the session to the database

    def edit(self, name, base_hp, base_defense,base_attack, sprite_url):
        self.name = name
        self.base_hp= base_hp
        self.base_defense = base_defense
        self.base_attack = base_attack
        self.sprite_url = sprite_url
        self.save()
    
    

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def fight(self,other):
        if(self.base_hp > 0):
            print("%s did %b damage to %s"%(self.name,self.base_attack,other.name))
            print("%s has %d hp left"%(other.name,other.base_hp))

            other.base_hp -= self.base_attack
            return other.fight(self)  #Now the other pokemon fights back
        else:
            print("%s wins! (%d hp left)"%(other.name,other.base_hp))
            return other,self  #return a tuple (winner,loser)









#class Post(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    body = db.Column(db.Text)
#    date_created = db.Column(db.DateTime, default=dt.utcnow)
 #   date_updated = db.Column(db.DateTime, onupdate=dt.utcnow)
 #   user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # saves the Post to the database
#    def save(self):
  #      db.session.add(self) # add the Post to the db session
  #      db.session.commit() #save everything in the session to the database

#    def edit(self, new_body):
#        self.body=new_body
#        self.save()
##    def __repr__(self):
 #       return f'<id:{self.id} | Post: {self.body[:15]}>'