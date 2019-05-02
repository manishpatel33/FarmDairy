import base64
from binascii import hexlify, unhexlify
import datetime
from hashlib import md5
from Crypto.Cipher import AES
from django.conf import settings
import requests


class Encryption:

    def __init__(self):
        _pKey = hexlify(settings.ENC_PRIVATEKEY.encode('utf-8'))
        m = md5()
        m.update(_pKey)
        key = m.hexdigest()
        self.mkey = key.encode('utf-8')
        _skey = (settings.ENC_PRIVATEKEY + key).encode('utf-8')

        m = md5()
        m.update(_skey)
        iv = m.hexdigest()
        self.IV = unhexlify(iv.encode('utf-8'))

    # this metod is for encrypt
    # data = simple msg to be passed
    # return encrypt string
    def encrypt(self, data):
        cipher = AES.new(self.mkey, AES.MODE_CFB, self.IV)
        encrypted = cipher.encrypt(hexlify(data.encode('utf-8')))
        encrypted = base64.urlsafe_b64encode(encrypted)
        return encrypted.decode('utf-8')

    # this metod is for decrypt
    # data = encrypt msg to be passed
    # return simple string
    def decrypt(self, data):
        data = data.encode('utf-8')
        data = base64.urlsafe_b64decode(data)
        decipher = AES.new(self.mkey, AES.MODE_CFB, self.IV)
        plaintext = decipher.decrypt(data)
        return (unhexlify(plaintext).decode('utf-8'))


def recaptcha_response(request, recaptcha_response):
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
    result = requests.post(url, data=values)
    return result
