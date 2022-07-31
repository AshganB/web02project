import os
from typing import KeysView
from flask import Flask, render_template, request, redirect, url_for,jsonify
from forms import RegistrationForm
from model import User
from sqlalchemy.exc import IntegrityError
import hashlib
from forms import LoginForm
from flask_login import login_user, logout_user, login_required, current_user, login_manager, LoginManager


# from forms import SampleForm
from forms import insertionForm


#app=Flask(__name__)
#app.secret_key="privae_key"
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, static_folder="static")
    

    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY


    login_manager = LoginManager(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info' 

    class Location:
        def __init__(self,key,name,lat,lng):
            self.key=key
            self.name=name
            self.lat=lat
            self.lng=lng

        def to_dict(self):
            return {
                'id': self.key,
                'description': self.name,
                'location': {
                    'lng': self.lng,
                    'lat': self.lat
                }
         }


    locations = (
        Location('EK','Eschbacher Klippen',50.3638 ,8.5379),
        Location('GP','Golfpark Idstein',50.2582 , 8.2530),
        Location('FK','Freibad königstein',50.1828 , 8.4535)
    )

    locations_by_key={location.key:location for location in locations}


     # db_drop_and_create_all()

    # Routes defined for this app / website

    # @app.route('/hello')
    # def hello():
    #     return 'Hello World from Python Flask!'
    
    #<<<this one was used for the location>>>
    @app.route('/new-place')
    
    def helloRoot():
        form=insertionForm()
        return render_template(
            'hello.html',
            form=form, 
            locations=locations,
            location=locations[0]

            

        )   

    # @app.route('/say-my-name')
    # def helloName():
    #     nameParam = request.args.get('name')
    #     return render_template(
    #         'hello_name.html',
    #         personName=nameParam
    #     )    

    @app.route("/<location_code>")
    def show_location(location_code):
        location=locations_by_key.get(location_code)
        if location:
            return render_template('map.html',location=location)
        else:
            return("404")
        

    @app.route('/form', methods=['GET', 'POST'])
    def form():
        form = insertionForm()
        if form.validate_on_submit():
            return redirect(url_for('hello'))

        return render_template(
            'sample_form.html',
            form=form
        )  

    # @app.route('/hello_name.html') 
    # def hello_name():
    #     return render_template('hello_name.html',placeName=request.form['place']) 

    @app.route('/esri')   
    def esri_map():
        return render_template('esrimap.html',map_key='AAPK1e1078a375cf49bb8027d405c6ac0408q8meJDs4rdyC7ld-Az0KBv5UNrDJaGDUbbXuXR4VovBVT9WXJimnnuFWHBugSxs0')              


  
    @app.route('/api/get_items_in_radius') 
    def get_items():
        return jsonify(
                {
                    "success": True,
                    "results": [l.to_dict() for l in locations] 
                }
            ), 200

    


    #route for the RegisteraionForm

    @app.route("/register", methods=['GET', 'POST'])
    def register():
        # Sanity check: if the user is already authenticated then go back to home page
        # if current_user.is_authenticated:
        #     return redirect(url_for('home'))

        # Otherwise process the RegistrationForm from request (if it came)
        form = RegistrationForm()
        if form.validate_on_submit():
            # hash user password, create user and store it in database
            hashed_password = hashlib.md5(form.password.data.encode()).hexdigest()
            user = User(
                full_name=form.fullname.data,
                display_name=form.username.data, 
                email=form.email.data, 
                password=hashed_password)

            try:
                user.insert()
                flash(f'Account created for: {form.username.data}!', 'success')
                return redirect(url_for('home'))
            except IntegrityError as e:
                flash(f'Could not register! The entered username or email might be already taken', 'danger')
                print('IntegrityError when trying to store new user')
                # db.session.rollback()
            
        return render_template('register.html', form=form)   

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(user_id)           

    @app.route("/login", methods=['GET', 'POST'])
    def login():
        # Sanity check: if the user is already authenticated then go back to home page
        # if current_user.is_authenticated:
        #    return redirect(url_for('home'))

        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(display_name=form.username.data).first()
            hashed_input_password = hashlib.md5(form.password.data.encode()).hexdigest()
            if user and user.password == hashed_input_password:
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check user name and password', 'danger')
        return render_template('login.html', title='Login', form=form) 

    @app.route("/logout")

    

    #to add new location  
    
    @app.route("/new-location", methods=['GET', 'POST'])
    #before adding a new location , a login is important first
    @login_required
    def logout():
        logout_user()
        flash(f'You have logged out!', 'success')
        return redirect(url_for('home'))
    def new_location():
        pass

     # End Routes

    # Return the fully initialized app
    return app




app = create_app()
if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    app.run(host='127.0.0.1',port=port,debug=True)