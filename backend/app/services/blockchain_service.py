import os
import requests
import json
from dotenv import load_dotenv

load_dotenv("app/db/.env")

CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
API_KEY = os.getenv("API_KEY")


def mint_erc20_token(user_address, amount):
    """
    Calls the ERC20 token minting API.

    Parameters:
    - address (str): The wallet address to mint the token to.
    - amount (str): The amount of the token to mint.

    """
    api_endpoint = f"https://api.vorj.app/main/v2/erc20/contracts/{CONTRACT_ADDRESS}/mint"

    headers = {
        "content-type": "application/json",
        "x-api-key": API_KEY,

    }
    payload = {
        "address": user_address,
        "amount": amount,
        "exponent": 0

    }

    response = requests.post(api_endpoint, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"HTTP Status Code {response.status_code}"}


def get_erc20_balance(user_address):
    """
    Calls the ERC20 token balance API.

    Parameters:
    - address (str): The wallet address to check the balance of.

    Returns:
    - dict: The response from the API call.
    """

    api_endpoint = f"https://api.vorj.app/main/v2/erc20/contracts/{CONTRACT_ADDRESS}/balance/{user_address}"

    headers = {
        "accept": "application/json",
        "x-api-key": API_KEY
    }

    response = requests.get(api_endpoint, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"HTTP Status Code {response.status_code}"}
