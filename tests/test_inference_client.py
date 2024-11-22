import unittest
from unittest.mock import patch, MagicMock
from backend.inference_client import send_request, load_config

class TestInferenceClient(unittest.TestCase):
    def setUp(self):
        self.config = {
            "server_url": "http://localhost:5000",
            "default_model": "test_model",
        }
        self.test_payload = {"model": "test_model", "param1": "value1"}

    @patch("backend.inference_client.requests.post")
    def test_send_request_success(self, mock_post):
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"output": "Test Response"}
        mock_post.return_value = mock_response

        response = send_request(self.config, "test_model", {"param1": "value1"})
        self.assertEqual(response, {"output": "Test Response"})
        mock_post.assert_called_once_with(
            f"{self.config['server_url']}/inference",
            json=self.test_payload,
        )

    @patch("backend.inference_client.requests.post")
    def test_send_request_failure(self, mock_post):
        # Mock error response
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response

        with self.assertRaises(Exception):
            send_request(self.config, "test_model", {"param1": "value1"})

    def test_load_config(self):
        # Test config loader
        with patch("builtins.open", unittest.mock.mock_open(read_data="server_url: http://localhost:5000\ndefault_model: test_model")):
            config = load_config("config.yaml")
            self.assertEqual(config["server_url"], "http://localhost:5000")
            self.assertEqual(config["default_model"], "test_model")

if __name__ == "__main__":
    unittest.main()
