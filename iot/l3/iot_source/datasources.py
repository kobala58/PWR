import xAPIConnector
from dotenv import load_dotenv
import os
import time


def get_ask_price(instrument: str):
    load_dotenv()
    userId = os.environ.get("LOGIN")
    password = os.environ.get("PASSWORD")
    client = xAPIConnector.APIClient()
    login_response = client.execute(xAPIConnector.loginCommand(userId=userId, password=password))
    ssid = login_response['streamSessionId']
    resp = client.commandExecute('getSymbol', dict(symbol=instrument))
    client.disconnect()
    return {
        "time": int(time.time()),
        "walor": resp["returnData"]["symbol"],
        "bid": resp["returnData"]["bid"],
        "ask": resp["returnData"]["ask"],
    }


if __name__ == "__main__":
    print(get_ask_price("USDPLN"))
