import requests
import unittest
from unittest import TestCase

class TestIntegration(TestCase):
    def test_v1_quote(self):
        response = requests.post(
            'http://127.0.0.1/v1/quotes',
            json={
                'starting_country': 'China',
                'destination_country': 'USA',
                'boxes': [
                    {
                        'count': 1,
                        'weight_kg': 20.5,
                        'length': 40.0,
                        'width': 30.0 ,
                        'height': 25.0
                    },
                    {
                        'count': 6,
                        'weight_kg': 19.5,
                        'length': 36.0,
                        'width': 27.0 ,
                        'height': 20.5
                    }		
                ]
            },
        )
        # Expected result
        expected_response = {
            "quotes": [
                {
                    "cost_breakdown": {
                        "oversized_fee": 0.0,
                        "overweight_fee": 0.0,
                        "service_fee": 300.0,
                        "shipping_cost": 481.25
                    },
                    "shipping_channel": "air",
                    "shipping_time_range": {
                        "max_days": 20,
                        "min_days": 15
                    },
                    "total_cost": 781.25
                },
                {
                    "cost_breakdown": {
                        "oversized_fee": 0.0,
                        "overweight_fee": 0.0,
                        "service_fee": 300.0,
                        "shipping_cost": 137.5
                    },
                    "shipping_channel": "ocean",
                    "shipping_time_range": {
                        "max_days": 50,
                        "min_days": 45
                    },
                    "total_cost": 437.5
                }
            ]
        }            
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_response)

if __name__ == '__main__':
    unittest.main()