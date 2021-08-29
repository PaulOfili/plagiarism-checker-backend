import json
from .consts import Consts

class CommandFailedError(Exception):

    def __init__(self, response):
        self.copyleaksErrorCode = CommandFailedError.__parseCopyleaksErrorCode(response)
        self.copyleaksErrorMessage = CommandFailedError.__parseCopyleaksErrorMessage(response, self.copyleaksErrorCode)
        self.httpStatusCode = response.status_code

        super(CommandFailedError, self).__init__(self.copyleaksErrorMessage)
    
    def getErrorCode(self):
        return self.httpStatusCode
    
    @staticmethod
    def __parseCopyleaksErrorCode(response):
        if response.headers.get('Copyleaks-Error-Code') is not None:
            return int(response.headers['Copyleaks-Error-Code'])
        else:
            return Consts.UNDEFINED_COPYLEAKS_HEADER_ERROR_CODE
        
    @staticmethod
    def __parseCopyleaksErrorMessage(response, copyleaksErrorCode):
        response_message = response.content.decode()
        if response_message:
            return json.loads(response.content.decode())

        elif copyleaksErrorCode == Consts.UNDEFINED_COPYLEAKS_HEADER_ERROR_CODE:
            return "The application has encountered an unknown error. Please try again later."
        else:
            return response.json()['Message']