from flask import render_template, request
import requests
from app import app
from .forms import LoginForm



@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html.j2')



@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        #do Login stuff
        email = request.form.get("email").lower()
        password = request.form.get("password")
                                #Database col = form inputted email
        u = User.query.filter_by(email=email).first()

        if u and u.check_hashed_password(password): 
            login_user(u)
            # give the user feedback that you logged in successfully
            return redirect(url_for("index")) 

        #if email in app.config.get("REGISTERED_USERS") and \
            #password == app.config.get("REGISTERED_USERS").get(email).get('password'):
            #return f"Login success Welcome {app.config.get('REGISTERED_USERS').get(email).get('name')}"
        error_string = "Invalid Email password combo"
        return render_template('login.html.j2', error = error_string, form=form)
    return render_template('login.html.j2', form=form)

@app.route('/logout')
def logout():
    if current_user:
        logout_user()
        return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Registration()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_user_data = {
                "first_name":form.first_name.data.title(),
                "last_name":form.last_name.data.title(),
                "email":form.email.data.lower(),
                "password": form.password.data
            }
            new_user_object = User()
            # build user with form data
            new_user_object.from_dict(new_user_data)
            # save user to database
            new_user_object.save()
        except:
            error_string = "There was an unexpected Error creating your account. Please Try ahain"
            return render_template('register.html.j2', form=form, error = error_string) #1 When we had an error creating a user
        return render_template(url_for('login')) #2 on a post request that successfully creates a new user
    return render_template('register.html.j2', form = form) #3 the render template on the Get request

@app.route('/pokemon', methods = ['GET', 'POST'])
def pokemon():
    if request.method == 'POST':
        name = request.form.get('name')
        url = f"https://pokeapi.co/api/v2/pokemon/{name}"
        response = requests.get(url)
        if response.ok:
            # The request worked
            if not response.json():
                return "We had an error loading your data likely the pokemon is not in the database."
            data = response.json()           
            pokemon_dict={
                'name':data['forms'][0]['name'],
                'base_hp':data['stats'][0]['base_stat'],
                'base_defense':data['stats'][2]['base_stat'],
                'base_attack':data['stats'][3]['base_stat'],
                'sprite_url':data['sprites']['front_shiny']
            }
            print(pokemon_dict)
            return render_template('pokemon.html.j2',pokemon=pokemon_dict)

        else:
            return "We have a problem! Your pokemon is not in the server!"
            # The request fail

    return render_template('pokemon.html.j2')




    
       #from the stats section:
                 #base stat for hp
                 #base stat for defense
                 #base stat for attack
       #from the sprites section:
      # front_shiny (URL to the image)#}
      #base_exper = data['base_experience']