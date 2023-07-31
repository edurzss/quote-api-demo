from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import Column, Integer

db = SQLAlchemy()

class ShippingRoutes(db.Model):
    __tablename__ = 'shipping_routes'
    
    id = db.Column(db.Integer, primary_key=True)
    starting_country = db.Column(db.String, nullable=False)
    destination_country = db.Column(db.String, nullable=False)
    shipping_channel = db.Column(db.String, nullable=False)
    shipping_time_min_days = db.Column(db.Integer, nullable=False)
    shipping_time_max_days = db.Column(db.Integer, nullable=False)
    rates = db.Column(db.JSON, nullable=False)
