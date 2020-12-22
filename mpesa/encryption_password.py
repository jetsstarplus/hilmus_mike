import base64
try:
    from . import keys
except:
    import keys
# from M2Crypto.M2Crypto import RSA, X509
from base64 import b64encode
  

#encrypting the data we are using

def data_encryption(formatted_time):
    data_to_encode = keys.LipaNaMpesaOnlineShortcode + keys.LipaNaMpesaOnlinePasskey + formatted_time
    encoded_data = base64.b64encode(data_to_encode.encode())
    #print(encoded_data)
    decoded_password = encoded_data.decode('utf-8')
    # print(str(decoded_password))
    return decoded_password


  
# def encryptInitiatorPassword():
#     cert_file = open(keys.CERTIFICATE_FILE, 'r')
#     cert_data = cert_file.read() #read certificate file
#     cert_file.close()

#     cert = X509.load_cert_string(cert_data)
#     #pub_key = X509.load_cert_string(cert_data)
#     pub_key = cert.get_pubkey()
#     rsa_key = pub_key.get_rsa()
#     cipher = rsa_key.public_encrypt(keys.INITIATOR_PASS, RSA.pkcs1_padding)
#     return b64encode(cipher)


