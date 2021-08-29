import json
import requests

from dateutil import parser
from datetime import datetime

from .consts import Consts
from .commandfailederror import CommandFailedError


class LoginToken:

    def __init__(self, email, api_key):
        self.Email = email
        self.ApiKey = api_key

    def getAccessToken(self):
        return self.AccessToken
    def __setAccessToken(self, value):
        self.AccessToken = value
    
    def getIssuedTime(self):
        return self.IssuedTime
    def __setIssuedTime(self, value):
        self.IssuedTime = value
        
    def getExpiresTime(self):
        return self.ExpiresTime
    def __setExpiresTime(self, value):
        self.ExpiresTime = value
    
    def login(self):

        url = "%s%s/account/login/api" % (Consts.LOGIN_ENTRY_POINT, Consts.SERVICE_VERSION)
        payload = {
            'email': self.Email, 
            'key': self.ApiKey
        }
        headers = {
            'Content-Type': Consts.CONTENT_TYPE_JSON
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code == Consts.HTTP_SUCCESS:
            self.__setAccessToken(response.json()['access_token'])
            self.__setIssuedTime(parser.parse(response.json()['.issued']).replace(tzinfo=None))
            self.__setExpiresTime(parser.parse(response.json()['.expires']).replace(tzinfo=None))
        else:
            raise CommandFailedError(response) 
    
    def generateAuthrizationHeader(self):
        
        if datetime.utcnow() <= self.getExpiresTime(): # If token expired, renew it.
            self.login()
        
        return "Bearer %s" % (self.getAccessToken())
    