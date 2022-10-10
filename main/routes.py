
from flask import render_template,url_for,request,redirect,flash
from main import app , connection1 , Products , db , login_manager , User123 , Admin123
import json
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length , ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user , current_user , logout_user , login_required
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time

# Webdriver Automation functions


def get_images_from_google(wd, delay, max_images , val):
	def scroll_down(wd):
		wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(delay)

	url = f"https://www.google.com/search?q={val}&tbm=isch&ved=2ahUKEwjykJ779tbzAhXhgnIEHSVQBksQ2-cCegQIABAA&oq={val}&gs_lcp=CgNpbWcQAzIHCAAQsQMQQzIHCAAQsQMQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzoHCCMQ7wMQJ1C_31NYvOJTYPbjU2gCcAB4AIABa4gBzQSSAQMzLjOYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=7vZuYfLhOeGFytMPpaCZ2AQ&bih=817&biw=1707&rlz=1C1CHBF_enCA918CA918"
	wd.get(url)

	image_urls = set()
	skips = 0

	while len(image_urls) + skips < max_images:
		scroll_down(wd)

		thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

		for img in thumbnails[len(image_urls) + skips:max_images]:
			try:
				img.click()
				time.sleep(delay)
			except:
				continue

			images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
			for image in images:
				if image.get_attribute('src') in image_urls:
					max_images += 1
					skips += 1
					break

				if image.get_attribute('src') and 'http' in image.get_attribute('src'):
					image_urls.add(image.get_attribute('src'))
					print(f"Found {len(image_urls)}")

	return image_urls


# def download_image(download_path, url, file_name):
# 	try:
# 		image_content = requests.get(url).content
# 		image_file = io.BytesIO(image_content)
# 		image = Image.open(image_file)
# 		file_path = download_path + file_name
        
# 		with open(file_path, "wb") as f:
# 			image.save(f, "JPEG")

# 		print("Success")
# 	except Exception as e:
# 		print('FAILED -', e)


@login_manager.user_loader
def load_user(user_id):
    return User123.query.get(int(user_id))



# @login_manager.user_loader
# def load_user(user_id):
#     return User123.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])

    def validate_username(self , username):
        user = User123.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That Username is taken. Please choose a new one')
    
    def validate_email(self , email):
        user = User123.query.filter_by(email=email.data).first()
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
@login_required
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
    if current_user.is_authenticated:
        return redirect(url_for('contact'))
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
    next_url = request.form.get("next")
    if current_user.is_authenticated:
        return redirect(url_for('contact'))
    if form.validate_on_submit():
        user_type = request.form['user-type']
        if user_type == "user":
            user = User123.query.filter_by(username=form.username.data).first()
            # user = db.session.query(User).filter_by(username = form.username.data).first()
            if user:
                if check_password_hash(user.password, form.password.data):
                    login_user(user , remember = form.remember.data )
                    # next_page = request.args.get("next")
                    # print(next_page)
                    flash(f"Welcome {form.username.data}! , You have successfully logged in to our website." , 'success')
                    if next_url:
                        return redirect(next_url)
                    return redirect(url_for("contact"))
                    # return redirect(next_page) if next_page else redirect(url_for('contact'))
        elif user_type == "recruitor":
            # recruitor = Recruitor.query.filter_by(username=form.username.data).first()
            admin = Admin123.query.filter_by(username=form.username.data).first()
            if admin:
                if admin.password == form.password.data:
                    print("Successssss!!!!!")
                    flash(f"Welcome {form.username.data}! , You have successfully logged in to our website as an Admin." , 'success')
                    return redirect(url_for('admin_dashboard'))
        
        flash("You have given wrong username or password , please try again." , "danger")
        return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('contact'))


# Routes for custom error pages

@app.errorhandler(404)
def error_404(error):
    return render_template("404.html") , 404

@app.errorhandler(403)
def error_403(error):
    return render_template("403.html") , 403

@app.errorhandler(500)
def error_500(error):
    return render_template("500.html") , 500

#Admin routes

@app.route("/admin-dashboard")
# @login_required
def admin_dashboard():
    return render_template("admin-dashboard.html")

@app.route("/admin-userlist")
# @login_required
def admin_userlist():
    return render_template("admin-user.html")


@app.route("/admin-model-testing")
# @login_required
def admin_model_testing():
    return render_template("admin-test-model.html")


@app.route("/admin-add-images" , methods = ['GET' , 'POST'])
# @login_required
def admin_add_image():
    val1 = request.form.get("imgsearch")
    val2 = request.form.get("imgquantity")
    urls = "noimages"
    if request.method == 'POST':
        PATH = "C:\\Program Files (x86)\\chromedriver.exe"
        wd = webdriver.Chrome(PATH)
        urls = get_images_from_google(wd, 1, int(val2) , val1)
    return render_template("admin-addimg.html" , urls = urls)

@app.route("/admin-remove-image" , methods = ['POST' , 'GET'])
def admin_remove_image():
    urls = request.args.get("a")
    print(urls)
    return redirect(url_for('admin_add_image'))