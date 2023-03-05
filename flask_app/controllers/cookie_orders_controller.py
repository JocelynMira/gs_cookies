from flask_app import app
from flask import render_template, redirect, request
from flask_app.models.cookie_order_model import Order


# route to dashboard displaying orders
@app.route('/')
def index():
    return redirect('/cookies')

# READ 
@app.route('/cookies')
def get_all_orders():
    orders = Order.get_all()
    return render_template ('index.html', all_orders = orders)

# route to create new order
@app.route('/place_order')
def place_order():
    return render_template ('new_order.html')

# CREATE
@app.route('/new_order', methods = ['POST'])
def new_order():
    # validate to make sure data is in correct format before we transfer data
    if not Order.validate_order(request.form):
        return redirect('/place_order')
    data = { 
        'name' : request.form['name'],
        'cookie_type' : request.form['cookie_type'],
        'number_of_boxes' : request.form['number_of_boxes']
    }
    Order.save(data)
    return redirect ('/')

# route to change order
@app.route('/change/<int:id>')
def change_one_order(id):
    order = Order.one_order(id)
    return render_template ('change_order.html', order = order )

# UPDATE
@app.route('/change_order/<int:id>', methods = ['POST'])
def change(id):
    if not Order.validate_order(request.form):
        return redirect (f"/change/{id}")

    data = {
        'id': id,
        'name': request.form['name'],
        'cookie_type': request.form['cookie_type'],
        'number_of_boxes': request.form['number_of_boxes']
    }
    Order.change(data)
    return redirect ('/')

# DELETE
@app.route('/delete_order/<int:id>')
def delete(id):
    Order.delete(id)
    return redirect ('/')