import requests

from utils import timestamp
from access_token import authentication
import keys
from encryption_password import data_encryption

access_token = authentication()
api_url = "https://sandbox.safaricom.co.ke/mpesa/accountbalance/v1/query"
headers = {"Authorization": "Bearer %s" % access_token}
request = { "Initiator":keys.initiatorName,
    "SecurityCredential":keys.generatedInitiatorSecurityCredential,
    "CommandID":"AccountBalance",
    "PartyA":keys.PartyA,
    "IdentifierType":"4",
    "Remarks":"This is a balance query",
    "QueueTimeOutURL":"https://thawing-spire-41307.herokuapp.com/payments/lmmapi/qeuetimeout/",
    "ResultURL":"https://thawing-spire-41307.herokuapp.com/payments/lmmapi/balance/"
    }

try:
    response = requests.post(api_url, json = request, headers=headers)
except:
    response = requests.post(api_url, json = request, headers=headers, verify=False)


print (response.text)
  