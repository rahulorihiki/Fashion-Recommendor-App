from textwrap import indent
from flask import render_template,url_for,request
from main import app , connection1 , Products , db
import json




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