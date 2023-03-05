from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Order:
    db = "gs_cookies"

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.cookie_type = data['cookie_type']
        self.number_of_boxes = data['number_of_boxes']

    # CREATE
    @classmethod
    def save(cls, data):
        query ="INSERT INTO cookie_orders (name, cookie_type, number_of_boxes) VALUES ( %(name)s, %(cookie_type)s, %(number_of_boxes)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    # READ (all)
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM cookie_orders;"
        results = connectToMySQL(cls.db).query_db(query)
        orders = [] 

        for order in results:
            orders.append( cls(order) )
        return orders
    
    # READ (one)
    @classmethod
    def one_order(cls, id):
        query = "SELECT * FROM cookie_orders WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, {'id': id})
        return cls(results[0])

    # UPDATE 
    @classmethod
    def change(cls, data):
        query = "UPDATE cookie_orders SET name = %(name)s, cookie_type = %(cookie_type)s, number_of_boxes = %(number_of_boxes)s WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results 

    # DELETE
    @classmethod
    def delete(cls, id):
        query = "DELETE FROM cookie_orders WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, {'id': id})
        return results
    
    # VALIDATION
    @staticmethod
    def validate_order(order):
        is_valid = True # assume this is true
        if len(order['name']) < 2:
            flash("Name must be at least 2 characters.")
            is_valid = False
        if len(order['cookie_type']) < 2:
            flash("Cookie Type must be at least 2 characters.")
            is_valid = False
        if int(order['number_of_boxes']) <= 0:
            flash("Number of Boxes must be more than 0.")
            is_valid = False
        return is_valid