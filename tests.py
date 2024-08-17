from unittest.mock import patch
import unittest
import requests
import main
from main import app


class TestWeatherApp(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    @patch('main.requests.get')
    def test_get_coordinates_successful(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.json.return_value = [{'lat': 51.5074, 'lon': -0.1278}]
        mock_response.raise_for_status = lambda: None

        coordinates = main.get_coordinates('London')
        self.assertEqual(coordinates, {'lat': 51.5074, 'lon': -0.1278})

    @patch('main.requests.get')
    def test_get_coordinates_failure(self, mock_get):
        mock_get.side_effect = requests.RequestException

        coordinates = main.get_coordinates('London')
        self.assertIsNone(coordinates)

    @patch('main.requests.get')
    def test_get_weather_data_successful(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.json.return_value = {
            'current': {'temp': 15, 'wind_speed': 3, 'rain': {'1h': 2}}
        }
        mock_response.raise_for_status = lambda: None

        weather = main.get_weather_data({'lat': 51.5074, 'lon': -0.1278})
        expected_result = {
            'latitude': 51.5074,
            'longitude': -0.1278,
            'temperature': 15,
            'wind_speed': 3,
            'precipitation': 2,
            'location': 'Lat: 51.5074, Lon: -0.1278'
        }
        self.assertEqual(weather, expected_result)

    @patch('main.requests.get')
    def test_get_weather_data_failure(self, mock_get):
        mock_get.side_effect = requests.RequestException

        weather = main.get_weather_data({'lat': 51.5074, 'lon': -0.1278})
        self.assertIsNone(weather)


if __name__ == '__main__':
    unittest.main()
