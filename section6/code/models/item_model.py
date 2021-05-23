#import sqlite3
from db import db

class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {"name":self.name, "price":self.price}
    
    @classmethod
    def find_by_name(cls, name):
        #connection = sqlite3.connect('my_data.db')
        #cursor = connection.cursor()

        #query = "SELECT * FROM items WHERE name = ?"
        #item = cursor.execute(query, (name,))
        #row = item.fetchone()
        #connection.close()

        #return cls(*row) if row else None
        return cls.query.filter_by(name=name).first()

    def save(self):
        #try:
            #connection = sqlite3.connect('my_data.db')
            #cursor = connection.cursor()

            #query = "INSERT INTO items VALUES (?, ?)"
            #cursor.execute(query, (self.name, self.price))
        #except:
            #connection.commit()
            #connection.close()
            #return {'message':'An error occurred while creating this item!'}
        #else:
            #connection.commit()
            #connection.close()
            #return self
        db.session.add(self)
        db.session.commit()

    # We don't need this function anymore, however we DO need a new one: 
    #def update_item(self):
        #try:
            #connection = sqlite3.connect('my_data.db')
            #cursor = connection.cursor()

            #query = "UPDATE items SET price = ? WHERE name = ?"
            #cursor.execute(query, (self.price, self.name))
        #except:
            #connection.commit()
            #connection.close()
            #return {'message':'An error occurred while updating this item!'}
        #finally:
            #connection.commit()
            #connection.close()
            #return self

    def delete_item(self):
        db.session.delete(self)
        db.session.commit()