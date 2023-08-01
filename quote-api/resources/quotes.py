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
# Import business logic functions
from logic import (
    calculate_weights, calculate_overweight_fees, calculate_oversized_fees, get_quotes
)

@bp.route('/')
class GetQuotes(MethodView):
    @bp.arguments(GetShippingQuotesSchema)
    @bp.response(200, GetShippingQuotesSchema, description="Successful response")
    @bp.alt_response(500, description="Internal server error")
    def post(self, data):
              
        # Load rates from database
        routes = db.session.execute(
            db.select(ShippingRoutes).where(and_(
                ShippingRoutes.starting_country == data['starting_country'],
                ShippingRoutes.destination_country == data['destination_country']
            ))
        ).scalars().all()

        if not routes:
            abort(500)

        # Calculate weights and per-box fees
        shipment_gross_weight, shipment_vol_weight = calculate_weights(data['boxes'])
        overweight_fees = calculate_overweight_fees(data['boxes'], data['starting_country'])
        oversized_fees = calculate_oversized_fees(data['boxes'], data['starting_country'])
        
        # Calculate service fees
        service_fees = 300 if data['starting_country'] == 'China' else 0
        
        # Calculate chargeable weight
        chargeable_weight = max(shipment_gross_weight, shipment_vol_weight)
        
        # Calculate quotes if available
        quotes = get_quotes(routes, chargeable_weight, service_fees, oversized_fees, overweight_fees)

        return {
            'quotes': quotes,
        }