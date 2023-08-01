from unittest import TestCase
# Import database models
from db import ShippingRoutes
# Import data classes
from classes import Quote
# Import functions to test
from logic import (
    calculate_weights, calculate_overweight_fees, calculate_oversized_fees, get_quotes
)

class TestBusinessLogic(TestCase):
    def test_calculate_weights(self):
        boxes = [
            {
                "count": 2,
                "weight_kg": 25,
                "length": 60.0,
                "width": 50.0 ,
                "height": 60.0
            },
            {
                "count": 4,
                "weight_kg": 15,
                "length": 100.0,
                "width": 60.0 ,
                "height": 30.0
            },
        ]
        gross_weight = 110
        volumetric_weight = 180

        self.assertEqual(
            (gross_weight, volumetric_weight),
            calculate_weights(boxes)
        )

    def test_calculate_overweight_fees(self):
        # Test data group 1
        starting_country = 'China'
        boxes = [
            {
                "count": 2,
                "weight_kg": 25,
                "length": 60.0,
                "width": 50.0 ,
                "height": 60.0
            },
            {
                "count": 4,
                "weight_kg": 15,
                "length": 100.0,
                "width": 60.0 ,
                "height": 30.0
            },
        ]
        # Expected result
        overweight_fees = 0

        self.assertEqual(
            overweight_fees,
            calculate_overweight_fees(boxes, starting_country)
        )
        # Test data group 2
        # Requirement: For shipments from India, a carton is oversized if it is 15 kg or more.
        # Overweight fee per carton = 80 USD
        starting_country = 'India'
        boxes = [
            {
                "count": 2,
                "weight_kg": 25,
                "length": 60.0,
                "width": 50.0 ,
                "height": 60.0
            },
            {
                "count": 4,
                "weight_kg": 15,
                "length": 100.0,
                "width": 60.0 ,
                "height": 30.0
            },
        ]
        # Expected result
        overweight_fees = 160

        self.assertEqual(
            overweight_fees,
            calculate_overweight_fees(boxes, starting_country)
        )

    def test_calculate_oversized_fees(self):
        # Test data group 1
        starting_country = 'China'
        boxes = [
            {
                "count": 2,
                "weight_kg": 25,
                "length": 60.0,
                "width": 50.0 ,
                "height": 60.0
            },
            {
                "count": 4,
                "weight_kg": 15,
                "length": 100.0,
                "width": 60.0 ,
                "height": 30.0
            },
        ]
        # Expected result
        overweight_fees = 0

        self.assertEqual(
            overweight_fees,
            calculate_oversized_fees(boxes, starting_country)
        )
        # Test data group 2
        # Requirement: For shipments from Vietnam, a carton is oversized if it's  >70cm for any dimension
        # Oversized fee per carton = 100 USD
        starting_country = 'Vietnam'
        boxes = [
            {
                "count": 2,
                "weight_kg": 25,
                "length": 60.0,
                "width": 50.0 ,
                "height": 60.0
            },
            {
                "count": 4,
                "weight_kg": 15,
                "length": 100.0,
                "width": 60.0 ,
                "height": 30.0
            },
        ]
        # Expected result
        overweight_fees = 400

        self.assertEqual(
            overweight_fees,
            calculate_oversized_fees(boxes, starting_country)
        )
    
    def test_get_quotes(self):

        # Emulate shipping routes from database
        routes = [
            ShippingRoutes(
                starting_country = 'China',
                destination_country = 'USA',
                shipping_channel = 'air',
                shipping_time_min_days = 15,
                shipping_time_max_days = 20,
                rates = [
                    {
                        "min_weight_kg": 0,
                        "max_weight_kg": 20,
                        "per_kg_rate": 5.00
                    },
                    {
                        "min_weight_kg": 20,
                        "max_weight_kg": 40,
                        "per_kg_rate": 4.50
                    },
                    {
                        "min_weight_kg": 40,
                        "max_weight_kg": 100,
                        "per_kg_rate": 4.00
                    },
                    {
                        "min_weight_kg": 100,
                        "max_weight_kg": 10000,
                        "per_kg_rate": 3.50
                    }
                ]
            )
        ]
        chargeable_weight = 140
        service_fees = 300
        oversized_fees = 160
        overweight_fees = 200
        # Expected result
        quotes = [
            Quote(
                shipping_channel = 'air',
                total_cost = 1150,
                cost_breakdown = {
                    'shipping_cost': 490,
                    'service_fee': service_fees,
                    'oversized_fee': oversized_fees,
                    'overweight_fee': overweight_fees,
                },
                shipping_time_range = {
                    'min_days': 15, 
                    'max_days': 20
                },
            ),
        ]

        self.assertListEqual(
            quotes,
            get_quotes(routes, chargeable_weight, service_fees, oversized_fees, overweight_fees)
        )
