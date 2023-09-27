from werkzeug.security import generate_password_hash # generates hashed pw
from flask_sqlalchemy import SQLAlchemy # allows DB to read classes/objects as tables/rows
from flask_login import UserMixin, LoginManager # load a current logged in user
from datetime import datetime
import uuid # generates a unique id
from flask_marshmallow import Marshmallow


# internal import
from .helpers import get_image



db = SQLAlchemy() # instantiate DB
login_manager = LoginManager() # instantiate Login Manager
ma = Marshmallow() # instantiate Marshmallow class


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id) # queries DB and brings back a user with the same id

# add a user
class User(db.Model, UserMixin):
    user_id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_added = db.Column(db.DateTime, default= datetime.utcnow)

# similar to INSERT INTO
    def __init__(self, username, email, password, first_name="", last_name=""):
        self.user_id = self.set_id() # creates a unique id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = self.set_password(password) # hash pw for security

    def set_id(self):
        return str(uuid.uuid4())
    
    def get_id(self):
        return str(self.user_id)

    def set_password(self, password):
        return generate_password_hash(password)
    
    def __repr__(self):
        return f"<USER: {self.username}"
    

# add a product
class Product(db.Model):
    prod_id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    image = db.Column(db.String(300), nullable = False)
    description = db.Column(db.String(200))
    year = db.Column(db.Integer, nullable = False)
    make = db.Column(db.String(100), nullable = False)
    model = db.Column(db.String(100), nullable = False)
    color = db.Column(db.String(100), nullable = False)
    miles = db.Column(db.Integer, nullable = False)
    price = db.Column(db.Numeric(precision=10, scale=2), nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    date_added = db.Column(db.DateTime, default = datetime.utcnow)
    prodord = db.relationship('ProdOrder', backref = 'product', lazy=True)

    # if a relationship with user was needed - ForeignKey
    # user_id = db.Column(db.String, dbForeignKey('user.user_id)'), nullable = False

    def __init__(self, name ,year, make, model, color, miles, price, quantity, image = "", description = ""):
        self.prod_id = self.set_id()
        self.name = name
        self.year = year
        self.make = make
        self.model = model
        self.color = color
        self.miles = miles
        self.price = price
        self.quantity = quantity
        self.image = self.set_image(image, name)
        self.description = description

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_image(self, image, name):
        if not image:
           image = get_image(name) # makes external API call
           print("api image", image)

        return image
    
    def decrement_quantity(self, quantity):

        self.quantity -= int(quantity)
        return self.quantity
    
    def increment_quantity(self, quantity):

        self.quantity += int(quantity)
        return self.quantity
    
    def __repr__(self):
        return f" <PRODUCT: {self.name}>"
    


    
class Customer(db.Model):
    cust_id = db.Column(db.String, primary_key = True)
    date_created = db.Column(db.DateTime, default = datetime.utcnow())
    prodord  = db.relationship('ProdOrder', backref = 'customer', lazy = True) #backref is just how are these related, lazy means a Customer can exist without the ProdOrder table


    def __init__(self, cust_id):
        self.cust_id = cust_id #we are getting their id from the front end 



#Many to Many relationship with Products, Customers & Orders
#So we need a join table

class ProdOrder(db.Model):
    prodorder_id = db.Column(db.String, primary_key = True)
    prod_id = db.Column(db.String, db.ForeignKey('product.prod_id'), nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    price = db.Column(db.Numeric(precision = 10, scale = 2), nullable = False)
    order_id = db.Column(db.String,  db.ForeignKey('order.order_id'), nullable = False)
    cust_id = db.Column(db.String, db.ForeignKey('customer.cust_id'), nullable = False)


    def __init__(self, prod_id, quantity, price, order_id, cust_id):
        self.prodorder_id = self.set_id()
        self.prod_id = prod_id
        self.quantity = quantity
        self.price = self.set_price(price, quantity)
        self.order_id = order_id
        self.cust_id = cust_id 


    def set_id(self):
        return str(uuid.uuid4())

    def set_price(self, price, quantity):

        quantity = float(quantity)
        price = float(price)

        self.price = quantity * price
        return self.price 
    

    def update_quantity(self, quantity): #method used for when customers update their order quantity of a specific product 

        self.quantity = int(quantity)
        return self.quantity
    




class Order(db.Model):
    order_id = db.Column(db.String, primary_key = True)
    order_total = db.Column(db.Numeric(precision = 10, scale = 2), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow())
    prodorder = db.relationship('ProdOrder', backref = 'order', lazy = True)


    def __init__(self):
        self.order_id = self.set_id()
        self.order_total = 0.00


    def set_id(self):
        return str(uuid.uuid4())
    


    #for every product's total price in prodorder table add to our order's total price 
    def increment_order_total(self, price):

        self.order_total = float(self.order_total)
        self.order_total += float(price)

        return self.order_total
    
    def decrement_order_total(self, price):

        self.order_total = float(self.order_total)
        self.order_total -= float(price)


        return self.order_total 
    
    # may need to comment this out
    def calculate_order_total(self):
        # Calculate the total order cost based on the items in the order
        total = 0
        for prodorder in self.products:
            total += prodorder.price * prodorder.quantity

        # Set the order total to 0 if there are no items in the order
        if total == 0:
            self.order_total = 0
        else:
            self.order_total = total

        return self.order_total
    
    def __repr__(self):

        return f"<ORDER: {self.order_id}>"
    
#Because we are building a RESTful API this week (Representational State Transfer) 
#json rules that world. JavaScript Object Notation aka dictionaries 
# Schemas

class ProductSchema(ma.Schema):
    class Meta:
        fields = ['prod_id', 'name', 'make', 'year', 'model', 'color', 'miles','image', 'description', 'price', 'quantity']


product_schema = ProductSchema() # 1 product
products_schema = ProductSchema(many = True) # many products






    