
from flask import render_template,url_for,request,redirect,flash
from main import app , connection1 , Products , db , User , Admin , login_manager , User123
import json
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length , ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])

    def validate_username(self , username):
        user =  db.session.query(User).filter_by(username = username.data).first()
        if user:
            raise ValidationError('That Username is taken. Please choose a new one')
    
    def validate_email(self , email):
        user =  db.session.query(User).filter_by(email = email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a new one')

cursor1 = connection1.cursor()
cursor1.execute("SELECT DISTINCT articleType FROM 'products' ")
distinct_fashion = cursor1.fetchall()

@app.route("/")
def contact():
    cursor1 = connection1.cursor()
    cursor1.execute("SELECT * FROM 'products' ")
    fashion = cursor1.fetchall()
    print(fashion[10])
    return render_template("index.html")

@app.route("/search/<data>" , methods = ["POST"])
def search(data):
    fashion_list = []
    for elements in distinct_fashion:
        try:
            (elements[0].lower()).index(data)
        except ValueError:
            pass  # do nothing!
            # distinct_fashion.remove(elements)
        else:
            fashion_list.append(elements[0])

    lengthss = len(fashion_list)
    fashion_string = str(lengthss)
    for i in range(lengthss - 1):
        fashion_string += '`'+fashion_list[i]
    # fashion_string = str(lengthss)+'`'+fashion_list[0]+'`'+fashion_list[1] +'`'+fashion_list[2] +'`'+fashion_list[3] +'`'+fashion_list[4] +'`'+fashion_list[5] +'`'+fashion_list[6] 
    if(lengthss == 1):
        fashion_string = str(fashion_list[0])
    
    print(data)
    return fashion_string
    

@app.route("/search-result/<a>" , methods = ["POST" , "GET"])
def search_result(a):
    page = request.args.get('page' , 1 , type = int)
    if(a == 'Tshirts'):
        pro = db.session.query(Products).filter_by(articleType = a , gender = 'Men').paginate(page = page , per_page = 9)
    else:
        pro = db.session.query(Products).filter_by(articleType = a).paginate(page = page , per_page = 9) 
    return render_template("shop.html" , pro = pro , val = a) 

@app.route("/search-result_subcategory/<a>")
def search_result_subcategory(a):
    page = request.args.get('page' , 1 , type = int)
    pro = db.session.query(Products).filter_by(subCategory = a).paginate(page = page , per_page = 9) 
    return render_template("shop.html" , pro = pro , val1 = a)

@app.route("/search-result_mastercategory/<a>")
def search_result_mastercategory(a):
    page = request.args.get('page' , 1 , type = int)
    pro = db.session.query(Products).filter_by(masterCategory = a).paginate(page = page , per_page = 9) 
    return render_template("shop.html" , pro = pro , val2 = a)


@app.route("/product-detail")
def product_detail():
    id = request.args.get('id' , type = int)
    cursor1 = connection1.cursor()
    cursor1.execute("SELECT * FROM 'products' where id = ? " , (str(id),) )
    fashion_d = cursor1.fetchall()
    print(str(id)+".json")
    with open("main/static/fashion-dataset/styles/" +str(id)+".json") as f:
        data = json.load(f)
    # For the Back image perspective
    try:
        data["data"]["styleImages"]["back"]["imageURL"]
    except KeyError:
        valval1 = "not_available"
    else:
        valval1 = data["data"]["styleImages"]["back"]["imageURL"]
    #For the left image perspective
    try:
        data["data"]["styleImages"]["left"]["imageURL"]
    except KeyError:
        valval2 = "not_available"
    else:
        valval2 = data["data"]["styleImages"]["left"]["imageURL"]
    
    #For the right image perspective
    try:
        data["data"]["styleImages"]["right"]["imageURL"]
    except KeyError:
        valval3 = "not_available"
    else:
        valval3 = data["data"]["styleImages"]["right"]["imageURL"]


    print(data["data"]["articleAttributes"])
    data_obj = {
        "id" : data["data"]["id"],
        "displayName" : data["data"]["productDisplayName"],
        "price" : data["data"]["price"],
        "brandName" : data["data"]["brandName"],
        "ageGroup" : data["data"]["ageGroup"],
        "gender" : data["data"]["gender"],
        "color" : data["data"]["baseColour"],
        "season" : data["data"]["season"],
        "year" : data["data"]["year"],
        "usage" : data["data"]["usage"],
        "productAttribute" : data["data"]["articleAttributes"],
        "brandInfo" : data["data"]["brandUserProfile"],
        "back_img_url" : valval1,
        "left_img_url" : valval2,
        "right_img_url" : valval3,
    }
    len1 = len(data_obj['productAttribute'])
    len2 = len(data_obj['brandInfo'])
    return render_template("detail.html" , data_obj = data_obj , len1 = len1 , len2 = len2)


# signup route

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        user_type = request.form['user-type']
        if user_type == "user":
            new_user = User123(username=form.username.data, email=form.email.data, password=hashed_password)
            # new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)

#login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user_type = request.form['user-type']
        if user_type == "user":
            user = User123.query.filter_by(username=form.username.data).first()
            # user = db.session.query(User).filter_by(username = form.username.data).first()
            if user:
                if check_password_hash(user.password, form.password.data):
                    login_user(user , remember = form.remember.data )
                    flash(f"Welcome {form.username.data}! , You have successfully logged in to our website." , 'success')
                    return redirect(url_for('contact'))
        elif user_type == "recruitor":
            # recruitor = Recruitor.query.filter_by(username=form.username.data).first()
            admin = db.session.query(Admin).filter_by(username = form.data.username).first()
            if admin:
                if admin.password == form.data.password:
                    print("Successssss!!!!!")
                    flash(f"Welcome {form.username.data}! , You have successfully logged in to our website as an Admin." , 'success')
                    return redirect(url_for('admin'))
        
        flash("You have given wrong username or password , please try again." , "danger")
        return redirect(url_for('login'))

    return render_template('login.html', form=form)
