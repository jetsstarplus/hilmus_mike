#in this file we register our url to safaricon

import requests

# for testing and django functionality
try:
    from .access_token import authentication        
    from . import keys
    from . import daraja
except:
    from access_token import authentication        
    import keys
    import daraja


access_token = authentication()

def register_url():
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = { "ShortCode":keys.business_shortcode,
        "ResponseType": "Completed",
        "ConfirmationURL": "https://hilmus-mike.herokuapp.com/payments/lmmapi/confirm/",
        "ValidationURL": "https://hilmus-mike.herokuapp.com/payments/lmmapi/validate/"}

    try:
        response = requests.post(api_url, json = request, headers=headers)
    except:
         response = requests.post(api_url, json = request, headers=headers, verify=False)
   

    print (response.text)