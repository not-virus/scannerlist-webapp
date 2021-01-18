import json
import requests
from enum import Enum

class Status(Enum):
    OK = 1
    HTTP_ERROR = 2
    BC_NOT_FOUND = 3

def get_and_parse(upc):
    pd = ProductData()
    url = "https://api.upcitemdb.com/prod/trial/lookup?upc=" + upc
    r = requests.get(url)
    if not r.status_code == 200:
        pd.status = Status.HTTP_ERROR
        return pd
    if not ('json' in r.headers['Content-Type']):
        pd.status = Status.HTTP_ERROR
        return pd

    # Get json and parse
    req_data = json.loads(r.text)
    #print(req_data)    ##  DEBUGGING

    # Check that barcode was found successfully
    if not req_data["code"] == "OK":
        pd.status = Status.BC_NOT_FOUND
        return pd

    # Test to ensure body is not empty
    try:
        req_data["items"][0]["ean"]
    except IndexError:
        pd.status = Status.BC_NOT_FOUND
        return pd

    # Get data
    pd.ean = req_data["items"][0]["ean"]
    pd.upc = req_data["items"][0]["upc"]
    pd.name = req_data["items"][0]["title"]
    pd.desc = req_data["items"][0]["description"]
    pd.lprice = req_data["items"][0]["lowest_recorded_price"]

    # Format name
    pd.name = pd.name.title()
    #pd.desc = pd.desc.title()

    # Set status
    pd.status = Status.OK
    return pd




class ProductData():

    def __init__(self):
        self.status = None
        self.ean = None
        self.upc = None
        self.name = None
        self.desc = None
        self.lprice = None

    def ProductData(self, ean, upc, name, desc, lprice):
        self.ean = ean
        self.upc = upc
        self.name = name
        self.desc = desc
        self.lprice = lprice
