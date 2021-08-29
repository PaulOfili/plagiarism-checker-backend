import json
import requests
import re

from .consts import Consts
from .commandfailederror import CommandFailedError
from .logintoken import LoginToken

class CopyleaksCloud:

    def __init__(self, product, email, api_key):

        assert product and email and api_key, 'Missing credentials!'

        self.token = self.login(email, api_key)
        self.product = product

        
    def login(self, email, api_key):
        token = LoginToken(email, api_key)
        token.login()
        return token

    
    def createByUrl(self, file_params):
        url = file_params["fileUrl"]
        scan_id = file_params["scanId"]
        user_id = file_params["userId"]


        assert url, 'Missing URL'
        assert bool(re.match('http://|https://', url, re.I)), 'url must starts with "http://" or "https://"'
        
        service_url = "%s%s/%s/submit/url/%s" % (Consts.SERVICE_ENTRY_POINT, Consts.SERVICE_VERSION, self.product, scan_id)

        token = self.token.generateAuthrizationHeader()

        headers = {
            'Content-type': 'application/json',
            'Authorization': token
        }

        data = {
            'url': f'{url}',
            'properties': {
                'developerPayload': f'{user_id}',
                'sandbox': True,
                'webhooks': {
                    'status': 'https://plagiarism-checker-listener.herokuapp.com/webhook/{STATUS}/%s' % scan_id
                },
                'filters': {
                     'relatedMeaningEnabled': False,
                },
                'scanning': {
                    'copyleaksDb': {
                        'includeMySubmissions': False,
                        'includeOthersSubmissions': False
                    }
                }
            }
        }

        json_data = json.dumps(data)

        print(json_data)
        response = requests.put(service_url, headers=headers, data=json_data)
        print(response, response.reason, response.content)

        if response.status_code == Consts.HTTP_CREATED:
            return None
        else:
            raise CommandFailedError(response)
