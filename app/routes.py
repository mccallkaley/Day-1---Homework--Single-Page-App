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
        # Do login Stuff
        email = form.email.data.lower()
        password = form.password.data
        if email in app.config.get('REGISTERED_USERS',{}).keys() and password == app.config.get('REGISTERED_USERS',{}).get(email).get('password'):
            #Login success!!!!!!!!
            return f"Login Success Welcome {app.config.get('REGISTERED_USERS',{}).get(email).get('name')}" 
        error_string = "Incorrect Email/Password Combo"
        return render_template("login.html.j2", form=form, error=error_string)
    return render_template("login.html.j2", form=form)

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