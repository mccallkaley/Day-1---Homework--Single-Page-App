from flask import render_template, request, flash, g
from flask_wtf import *
import requests
from flask_login import login_required
from app.blueprints.auth.forms import PokemonForm, SearchForm


from app.models import *
from .import bp as main

@main.route('/', methods = ['GET'])
@login_required
def index():
    return render_template('index.html.j2')


@main.route('/pokemon', methods = ['GET', 'POST'])
def pokemon():
    form = PokemonForm()
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
             

            poke = Pokemon.query.filter_by(name = form.name.data.lower()).first()
            pokemoncount = Pokemon.query.count()

            if poke:
                flash('Pokemon already exists', 'danger')
            elif pokemoncount>=5:
                flash('You can only have 5 pokemon!')

            else:
                #create and empty user
                new_pokemon_object = Pokemon()
                # build user with form data
                new_pokemon_object.from_dict(pokemon_dict)
                # save user to database
                new_pokemon_object.save()
                flash('New pokemon added to your team!', 'success')
            return render_template("pokemon.html.j2",form=form, pokemon=pokemon_dict)
        else:
            flash(f'Please check for error', 'danger')
            render_template("pokemon.html.j2",form=form)
    return render_template("pokemon.html.j2", form=form)

@main.route('/edit_post/<int:id>', methods=['GET','POST'])
@login_required
def edit_post(id):
    post = Post.query.get(id)
    if request.method == 'POST':
        post.edit(request.form.get('body'))
        flash("Your post has been edited","success")
    return render_template('edit_post.html.j2', post=post)

# GET ALL POKEMON
@main.route('/post/my_posts', methods=['GET','POST'])
@login_required
def my_posts():
    all_pokemon = Pokemon.query.all()
    print([all_pokemon])
    
    
    #all_pokemon = Pokemon.query.all()
    #all_pokemon= current_user.all_pokemon
    #Pokemon.query.all()
    #if current_user.id == post.author.id 
 
    return render_template('my_posts.html.j2', my_posts=all_pokemon)





 #if user and current_user.email != user.email:

    
       #from the stats section:
                 #base stat for hp
                 #base stat for defense
                 #base stat for attack
       #from the sprites section:
      # front_shiny (URL to the image)#}
      #base_exper = data['base_hp']