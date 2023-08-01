import json
from unittest import TestCase
# Import flask app
from app import create_app

class TestApi(TestCase):
    def setUp(self):
        app = create_app()
        self.client = app.test_client()    
    
    def test_good_parameters(self):
        response = self.client.post(
            '/v1/quotes/',
            data=json.dumps({
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
            }),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsInstance(data['quotes'], list)
        self.assertIsInstance(data['quotes'][0]['cost_breakdown'], dict)
        self.assertIsInstance(data['quotes'][0]['shipping_channel'], str)
        self.assertIsInstance(data['quotes'][0]['shipping_time_range'], dict)
        self.assertIsInstance(data['quotes'][0]['total_cost'], float)