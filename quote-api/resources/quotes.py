import json
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy import and_
# Import database and models
from db import db, ShippingRoutes
# Import validation schemas
from schemas import GetShippingQuotesSchema
bp = Blueprint(
    "Quotes", __name__,
    url_prefix='/v1/quotes',
)
# Import data classes
from classes import Quote

@bp.route('/')
class GetQuotes(MethodView):
    @bp.arguments(GetShippingQuotesSchema)
    @bp.response(200, GetShippingQuotesSchema)
    @bp.alt_response(500, description="Internal server error")
    def post(self, data):
              
        # Load rates from database
        routes = db.session.execute(
            db.select(ShippingRoutes).where(and_(
                ShippingRoutes.starting_country == data['starting_country'],
                ShippingRoutes.destination_country == data['destination_country']
            ))
        ).scalars().all()

        # Calculate weights and per-box fees 
        shipment_gross_weight = 0
        shipment_vol_weight = 0
        overweight_fees = 0
        oversized_fees = 0
        for box in data['boxes']:
            # Calculate shipment gross weight and volumetric weight
            gross_weight = box['count'] * box['weight_kg']
            shipment_gross_weight += gross_weight
            vol_weight = box['count'] * (box['length'] * box['width'] * box['height']) / 6000
            shipment_vol_weight += vol_weight
            
            # Calculate oversized and overweight fees
            if box['weight_kg'] > 30 :
                overweight_fees += (80 * box['count'])
            if any([box['length'] > 120, box['width'] > 120, box['height'] > 120]):
                oversized_fees += (100 * box['count'])
        
        # Calculate service fees
        service_fees = 0
        if data['starting_country'] == 'China':
            service_fees += 300

        chargeable_weight = max(shipment_gross_weight, shipment_vol_weight)
        total_fees = oversized_fees + overweight_fees + service_fees

        # Calculate quotes if available
        quotes = []
        for route in routes:
            # Validate whether chargeable weight is within weight range
            quote = None
            for range_rate in route.rates:
                if (
                    chargeable_weight > range_rate['min_weight_kg'] and
                    chargeable_weight <= range_rate['max_weight_kg']
                ):
                    rate = range_rate['per_kg_rate']
                    quote = Quote(
                        shipping_channel = route.shipping_channel,
                        total_cost = (chargeable_weight * rate) + total_fees,
                        cost_breakdown = {
                            'shipping_cost': chargeable_weight * rate,
                            'service_fee': service_fees,
                            'oversized_fee': oversized_fees,
                            'overweight_fee': overweight_fees,
                        },
                        shipping_time_range = {
                            'min_days': route.shipping_time_min_days, 
                            'max_days': route.shipping_time_max_days
                        },
                    )
            if quote is not None:
                quotes.append(quote)

        return {
            'quotes': quotes,
        }