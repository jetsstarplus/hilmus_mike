
import requests

try:
    #other libraries import
    from .access_token import authentication
    from . import keys
    from .encryption_password import data_encryption
    from .utils import timestamp

except:
    #other libraries import
    from access_token import authentication
    import keys
    from encryption_password import data_encryption
    from utils import timestamp



#create the lipa na mpesa API
def lipa_na_mpesa(phone_number, amount):
        
    access_token = authentication()
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = { "Authorization": "Bearer %s" % access_token }
    request = {
        "BusinessShortCode": keys.business_shortcode,
        "Password": data_encryption(timestamp()),
        "Timestamp": timestamp(),
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA":phone_number,
        "PartyB":keys.business_shortcode,
        "PhoneNumber": phone_number ,
        "CallBackURL": "https://thawing-spire-41307.herokuapp.com/payments/lmmapi/",
        "AccountReference": "11111 ",
        "TransactionDesc": "Pay school Fees"
    }

    #sending the request and expecting back a response
    try:
        response = requests.post(api_url, json = request, headers=headers)
    except:
        response = requests.post(api_url, json = request, headers=headers, verify=False)
    
    
    return(response.text)
    # print (response.text)
  
#authentication() 
# lipa_na_mpesa()