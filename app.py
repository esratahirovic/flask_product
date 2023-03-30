#import required libraries
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy


#
app = Flask(__name__)

#Config settings 
#app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///products.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False


db = SQLAlchemy(app)

#class for creating table and i define a funciton for calculating discounted price 
class Product(db.Model):

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String, nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float)
    

    def __repr__(self):
        return {"item": self.item, "price": self.price}
    
    #calculate new price after appliying discount
    def discounted_price(self):
            if self.discount:
                return self.price * (1 - self.discount)
            else:
 
                return self.price
            
#for table creation.
with app.app_context():   
        db.create_all()
        db.session.commit()

#for showing all products on the table
@app.get("/products")
def get_all_products():
    products = Product.query.all()
    output = []
    for product in products:
        prod_info = {"item":product.item, "price": product.price, "discount": product.discount, 
                     "new_price": product.discounted_price()}
        output.append(prod_info)

    return {"products": output}

#with "id" endpoint we can see a specific product
@app.get("/products/<id>")
def get_product(id):
    product = Product.query.get(id)
    if product is None:
        return {"error": "Product not found"}
    else:
        return {"item" :product.item, "price":  product.price, "discount": product.discount, 
                "new_price": product.discounted_price()}
    
#this one is for adding a new product
@app.post("/products")
def add_product():
    product = Product(item=request.json["item"], price=request.json["price"], discount=request.json["discount"])

    db.session.add(product)
    db.session.commit()

    return {"message": "Product added successfully"}

#for updating a product with using id
@app.put("/products/<id>")
def update_product(id):
    product = Product.query.get(id)
    if product in None:
        return {"error": "Product not found"}
    else:
        if product.item is not None:
            product.item = request.json["item"]
        if product.price is not None:
            product.price = request.json["price"]
        if product.discount is not None:
            product.discount = request.json["discount"]

        db.session.commit()
        
        return {"message": "Product updated."}
    
#at last, we can delete the product
@app.delete("/product/<id>")
def delete_product(id):
    product = Product.query.get(id)
    if product is None:
        return {"error": "Product not found"}
    db.session.delete(product)
    db.session.commit()
    return {"message": "Product deleted"}

if __name__ == "__main__":
    app.run(debug=True, port=8000)
