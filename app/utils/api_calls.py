import requests
import json
from pprint import pprint

def handle_response(response, url: str) -> None:
    if response.status_code >= 300:
        raise ValueError(f'Error when calling {url}.\nError code: {response.status_code}\nRaw error: {response.text}')


def get_active_model_name(api_url: str) -> str:
    url: str = f'{api_url}/models'
    response = requests.get(url)
    handle_response(response, url)
    active_model: dict = [model for model in response.json() if model.get('is_active')][0]
    return active_model.get('name', '')


def predict_flow(api_url: str, active_model_name: str, flow: dict) -> str:
    url: str = f'{api_url}/models/predict/{active_model_name}'
    pprint(flow)
    response = requests.post(url, data=json.dumps(flow))
    handle_response(response, url)
    prediction: dict = response.json()
    return prediction.get('prediction')

def save_flow_to_db(db_url: str, flow: dict) -> dict:
    url: str = f'{db_url}/network_flows'
    response = requests.post(url, data=json.dumps(flow))
    handle_response(response, url)
    print(f'saved flow')
    print(response.json())
    return response.json()


