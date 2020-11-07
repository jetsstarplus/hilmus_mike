import requests

try:
    import keys
except:
    from . import keys
# from . import keys
from requests.auth import HTTPBasicAuth

#this is the authentication from safaricom
def authentication():
    """This method requests for authentication keys from safaricom"""
    consumer_key = keys.consumer_key
    consumer_secret = keys.consumer_secret
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    
    try:
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    except:
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret), verify=False)
        
   
    json_token = r.json()
    my_access_token = json_token["access_token"]
    # print(r.text)
    return my_access_token
# authentication()