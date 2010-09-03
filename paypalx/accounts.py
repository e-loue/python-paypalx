# -*- coding: utf-8 -*-
from paypalx import AdaptiveAPI

class AdaptiveAccounts(AdaptiveAPI):
    def __init__(self, username, password, signature, application_id, email, sandbox=False):
        super(AdaptiveAccounts, self).__init__(username, password, signature, application_id, email, 'AdaptiveAccounts', sandbox)
    
    def create_account(self, **kwargs):
        if 'requestEnvelope' not in kwargs:
            kwargs['requestEnvelope'] = { }
        required_values = ('accountType', 'address', 'citizenshipCountryCode',
            'contactPhoneNumber', 'createAccountWebOptions', 'currencyCode',
            'dateOfBirth', 'name', 'preferredLanguageCode', 'requestEnvelope')
        self._check_required(required_values, **kwargs)
        endpoint = self._endpoint('CreateAccount')
        return self._request(endpoint, data=kwargs)
    
    def add_bank_account(self, **kwargs):
        if 'requestEnvelope' not in kwargs:
            kwargs['requestEnvelope'] = { }
        required_values = ('confirmationType', 'bankCountryCode', 'requestEnvelope')
        self._check_required(required_values, **kwargs)
        endpoint = self._endpoint('AddBankingAccount')
        return self._request(endpoint, data=kwargs)
    
    def add_payment_card(self, **kwargs):
        if 'requestEnvelope' not in kwargs:
            kwargs['requestEnvelope'] = { }
        required_values = ('billingAddress', 'cardType', 'cardNumber',
            'confirmationType', 'nameOnCard', 'expirationDate')
        self._check_required(required_values, **kwargs)
        endpoint = self._endpoint('AddPaymentCard')
        return self._request(endpoint, data=kwargs)
    
    def set_funding_source_confirmed(self, **kwargs):
        if 'requestEnvelope' not in kwargs:
            kwargs['requestEnvelope'] = { }
        required_values = ('fundingSourceKey',)
        self._check_required(required_values, **kwargs)
        endpoint = self._endpoint('SetFundingSourceConfirmed')
        return self._request(endpoint, data=kwargs)
    
    def get_verified_status(self, **kwargs):
        if 'requestEnvelope' not in kwargs:
            kwargs['requestEnvelope'] = { }
        required_values = ('emailAddress', 'firstName', 'lastName', 'matchCriteria')
        self._check_required(required_values, **kwargs)
        endpoint = self._endpoint('GetVerifiedStatus')
        return self._request(endpoint, data=kwargs)
    
    def get_user_agreement(self, **kwargs):
        if 'requestEnvelope' not in kwargs:
            kwargs['requestEnvelope'] = { }
        endpoint = self._endpoint('GetUserAgreement')
        return self._request(endpoint, data=kwargs)
    
