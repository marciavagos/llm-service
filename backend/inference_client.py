import argparse
import requests
import yaml

# Load configuration
def load_config(config_file):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

# CLI Argument Parser
def parse_args():
    parser = argparse.ArgumentParser(description="LLM Inference Client")
    parser.add_argument('--model', required=False, help="Model name or URL")
    parser.add_argument('--config', required=False, default='config.yaml', help="Path to config file")
    parser.add_argument('--params', nargs='+', help="Additional parameters as key=value pairs")
    return parser.parse_args()

# Main Request Function
def send_request(config, model=None, params={}):
    server_url = os.environ.get('SERVER_URL', 'http://localhost:5000')
    url = f"{server_url}/inference"
    payload = {
        'model': model or config['default_model'],
        **params
    }
    response = requests.post(url, json=payload)
    return response.json()

if __name__ == "__main__":
    args = parse_args()
    config = load_config(args.config)
    model = args.model
    params = dict(param.split('=') for param in args.params) if args.params else {}
    result = send_request(config, model, params)
    print("Inference Result:", result)
