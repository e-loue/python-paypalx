# -*- coding: utf-8 -*-
from paypalx import AdaptiveAPI

class PaymentsAPI(AdaptiveAPI):
    def __init__(self, username, password, signature, application_id, email, sandbox=False):
        super(PaymentsAPI, self).__init__(username, password, signature, application_id, email, 'AdaptivePayments', sandbox)
    
    def pay_request(self, **kwargs):
        if 'requestEnvelope' not in kwargs:
            kwargs['requestEnvelope'] = { }
        required_values = ('actionType', 'cancelUrl', 'currencyCode', 
            'receiverList', 'returnUrl')
        self._check_required(required_values, **kwargs)
        endpoint = self._endpoint('Pay')
        return self._request(endpoint, data=kwargs)
    
    def set_payments_options(self, **kwargs):
        if 'requestEnvelope' not in kwargs:
            kwargs['requestEnvelope'] = { }
        required_values = ('payKey',)
        self._check_required(required_values, **kwargs)
        endpoint = self._endpoint('SetPaymentOptions')
        return self._request(endpoint, data=kwargs)
    
    def execute_payments(self, **kwargs):
        if 'requestEnvelope' not in kwargs:
            kwargs['requestEnvelope'] = { }
        required_values = ('payKey',)
        self._check_required(required_values, **kwargs)
        endpoint = self._endpoint('ExecutePayment')
        return self._request(endpoint, data=kwargs)
    
    def payment_details(self, **kwargs):
        if 'requestEnvelope' not in kwargs:
            kwargs['requestEnvelope'] = { }
        endpoint = self._endpoint('PaymentDetails')
        return self._request(endpoint, data=kwargs)
    
    def get_payment_options(self, **kwargs):
        if 'requestEnvelope' not in kwargs:
            kwargs['requestEnvelope'] = { }
        required_values = ('payKey',)
        self._check_required(required_values, **kwargs)
        endpoint = self._endpoint('GetPaymentOptions')
        return self._request(endpoint, data=kwargs)
    
    def preapproval(self, **kwargs):
        if 'requestEnvelope' not in kwargs:
            kwargs['requestEnvelope'] = { }
        required_values = ('endingDate', 'startingDate', 'currencyCode',
            'maxTotalAmountOfAllPayments', 'cancelUrl', 'returnUrl')
        self._check_required(required_values, **kwargs)
        endpoint = self._endpoint('Preapproval')
        return self._request(endpoint, data=kwargs)
    
    def preapproval_details(self, **kwargs):
        if 'requestEnvelope' not in kwargs:
            kwargs['requestEnvelope'] = { }
        required_values = ('preapprovalKey',)
        self._check_required(required_values, **kwargs)
        endpoint = self._endpoint('PreapprovalDetails')
        return self._request(endpoint, data=kwargs)
    
    def cancel_preapproval(self, **kwargs):
        if 'requestEnvelope' not in kwargs:
            kwargs['requestEnvelope'] = { }
        required_values = ('preapprovalKey',)
        self._check_required(required_values, **kwargs)
        endpoint = self._endpoint('CancelPreapproval')
        return self._request(endpoint, data=kwargs)
    
    def refund(self, **kwargs):
        if 'requestEnvelope' not in kwargs:
            kwargs['requestEnvelope'] = { }
        endpoint = self._endpoint('Refund')
        return self._request(endpoint, data=kwargs)
    
    def convert_currency(self, **kwargs):
        if 'requestEnvelope' not in kwargs:
            kwargs['requestEnvelope'] = { }
        required_values = ('baseAmountList', 'convertToCurrencyList')
        self._check_required(required_values, **kwargs)
        endpoint = self._endpoint('ConvertCurrency')
        return self._request(endpoint, data=kwargs)
    
