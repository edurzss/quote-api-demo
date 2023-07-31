from typing import List, Dict, Tuple
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
    

def calculate_weights(boxes: List[Dict]) -> Tuple:
    """
    Calculates shipment's gross weight and volumetric weight.

    Parameters
    ----------
    boxes : list
        List of boxes
    Returns
    -------
    tuple
        gross_weight, volumetric_weight
    """
    shipment_gross_weight = 0
    shipment_vol_weight = 0

    for box in boxes:
        gross_weight = box['count'] * box['weight_kg']
        shipment_gross_weight += gross_weight

        vol_weight = box['count'] * (box['length'] * box['width'] * box['height']) / 6000
        shipment_vol_weight += vol_weight
        
    return shipment_gross_weight, shipment_vol_weight

def calculate_overweight_fees(boxes: List[Dict], starting_country: str) -> float:
    """
    Calculates total overweight fees for the shipment.

    Parameters
    ----------
    boxes : list
        List of boxes

    Returns
    -------
    float
        overweight_fees   
    """
    kg_threshold_dict = {
        'India': 15
    }
    overweight_fees = 0

    for box in boxes:
        # Calculate oversized and overweight fees
        if box['weight_kg'] > kg_threshold_dict.get(starting_country, 30) :
            overweight_fees += (80 * box['count'])

    return overweight_fees

def calculate_oversized_fees(boxes: List[Dict], starting_country: str) -> float:
    """
    Calculates total oversized fees for the shipment.

    Parameters
    ----------
    boxes : list
        List of boxes

    Returns
    -------
    float
        oversized_fees   
    """
    cm_threshold_dict = {
        'Vietnam': 70
    }
    oversized_fees = 0
    
    for box in boxes:
        if any([
            box['length'] > cm_threshold_dict.get(starting_country, 120), 
            box['width'] > cm_threshold_dict.get(starting_country, 120), 
            box['height'] > cm_threshold_dict.get(starting_country, 120)
        ]):
            oversized_fees += (100 * box['count'])

    return oversized_fees

def get_quotes(
        routes: List, 
        chargeable_weight: float, 
        service_fees: float, 
        oversized_fees: float, 
        overweight_fees: float
) -> List:
    """
    Calculates a quote for each available shipping route if 
    the cargeable weight is inside some weight range
    
    Parameters
    ----------
    routes : list
    chargeable_weight : float
        chargeable weight of the total shipment
    service_fees : float
        additional service fees
    oversized_fees : float
        additional oversized fees
    overweight_fees : float
        additional overweight fees

    Returns
    -------
    list
        List of quotes
    """
    total_fees = oversized_fees + overweight_fees + service_fees
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

    return quotes