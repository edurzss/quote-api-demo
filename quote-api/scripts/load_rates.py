import os, json
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import (
    create_engine, Column, Integer, String, JSON
)
from sqlalchemy.orm import (
    DeclarativeBase, Session
)
# Load environment variables
load_dotenv(find_dotenv(), override=True)


# Define table model for standalone usage of the script
class Base(DeclarativeBase):
    pass
class ShippingRoutes(Base):
    __tablename__ = 'shipping_routes'
    
    id = Column(Integer, primary_key=True)
    starting_country = Column(String, nullable=False)
    destination_country = Column(String, nullable=False)
    shipping_channel = Column(String, nullable=False)
    shipping_time_min_days = Column(Integer, nullable=False)
    shipping_time_max_days = Column(Integer, nullable=False)
    rates = Column(JSON, nullable=False)

# Create PostgreSQL engine and session
engine = create_engine(os.environ.get('SQLALCHEMY_DATABASE_URI'), echo=True)
with Session(engine) as session:
    # Load rates to database
    rates_filepath = os.path.join('/src', 'rates.json')
    with open(rates_filepath, 'rt') as file:
        rates_json = json.load(file)
        for route in rates_json:
            record = ShippingRoutes(
                starting_country = route['starting_country'],
                destination_country = route['destination_country'],
                shipping_channel = route['shipping_channel'],
                shipping_time_min_days = route['shipping_time_range']['min_days'],
                shipping_time_max_days = route['shipping_time_range']['max_days'],
                rates = route['rates'],
            )
            session.add(record)
        session.commit()