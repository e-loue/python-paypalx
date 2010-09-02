# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from unittest import TestCase
from paypalx.payments import PaymentsAPI

try:
    import credentials
except ImportError:
    pass

API_USERNAME = getattr(credentials, 'API_USERNAME', "xxx_xxx_apix.xxx.com")
API_PASSWORD = getattr(credentials, 'API_PASSWORD', 'xxxxxxxxxx')
API_SIGNATURE = getattr(credentials, 'API_SIGNATURE', 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
API_APPLICATION_ID = getattr(credentials, 'API_APPLICATION_ID', 'APP-80W284485P519543T')
API_EMAIL = getattr(credentials, 'API_EMAIL', 'custX_xxxxxxxxxx_per@xxxxxxxx.com')

EMAIL_ACCOUNT = getattr(credentials, 'EMAIL_ACCOUNT', 'custX_xxxxxxxxxx_per@xxxxxxxx.com')

VISA_NUMBER = getattr(credentials, 'VISA_NUMBER', 'xxxxxxxxxxxxxxxx')
VISA_EXPIRATION = getattr(credentials, 'VISA_EXPIRATION', 'mmyyyy')

class TestAdaptivePayments(TestCase):
    notification_url = "http://notify.me"
    return_url = "http://return.me"
    cancel_url = "http://cancel.me"
    
    def setUp(self):
        self.paypal = PaymentsAPI(API_USERNAME, API_PASSWORD, API_SIGNATURE, API_APPLICATION_ID, API_EMAIL, sandbox=True)
        self.paypal.debug = False
    
    def test_pay_request(self):
        response = self.paypal.pay_request(
            actionType = 'PAY',
            cancelUrl = self.cancel_url,
            currencyCode = 'USD',
            senderEmail = API_EMAIL,
            feesPayer = 'EACHRECEIVER',
            memo = 'Simple payment example',
            receiverList = { 'receiver': [
                { 'amount':"1.0", 'email':EMAIL_ACCOUNT, }
            ]},
            returnUrl = self.return_url,
            ipnNotificationUrl = self.notification_url
        )
        self.assertEquals(response['responseEnvelope']['ack'], "Success")
        self.assertEquals(response['paymentExecStatus'], "COMPLETED")
        self.assertTrue(response.has_key('payKey'))
    
    def test_set_payments_options(self):
        payKey = self.paypal.pay_request(
            actionType = 'CREATE',
            cancelUrl = self.cancel_url,
            currencyCode = 'USD',
            senderEmail = API_EMAIL,
            feesPayer = 'EACHRECEIVER',
            receiverList = { 'receiver': [
                { 'amount':"1.0", 'email':EMAIL_ACCOUNT, }
            ]},
            returnUrl = self.return_url,
            ipnNotificationUrl = self.notification_url
        )['payKey']
        response = self.paypal.set_payments_options(
            initiatingEntitity = {
                'institutionCustomer':{
                    'countryCode':'US',
                    'displayName':'Sesame Street',
                    'email':'elmo@sesamestreet.org',
                    'firstName':'Elmo',
                    'institutionCustomer':'1',
                    'institutionCustomer':'2',
                    'lastName':'Baby Monster'
                } 
            },
            payKey = payKey
        )
        self.assertEquals(response['responseEnvelope']['ack'], "Success")
    
    def test_execute_payments(self):
        payKey = self.paypal.pay_request(
            actionType = 'CREATE',
            cancelUrl = self.cancel_url,
            currencyCode = 'USD',
            senderEmail = API_EMAIL,
            feesPayer = 'EACHRECEIVER',
            receiverList = { 'receiver': [
                { 'amount':"1.0", 'email':EMAIL_ACCOUNT, }
            ]},
            returnUrl = self.return_url,
            ipnNotificationUrl = self.notification_url
        )['payKey']
        response = self.paypal.execute_payments(
            payKey = payKey
        )
        self.assertEquals(response['responseEnvelope']['ack'], "Success")
        self.assertEquals(response['paymentExecStatus'], 'COMPLETED')
    
    def test_payment_details(self):
        payKey = self.paypal.pay_request(
            actionType = 'CREATE',
            cancelUrl = self.cancel_url,
            currencyCode = 'USD',
            senderEmail = API_EMAIL,
            feesPayer = 'EACHRECEIVER',
            receiverList = { 'receiver': [
                { 'amount':"1.0", 'email':EMAIL_ACCOUNT, }
            ]},
            returnUrl = self.return_url,
            ipnNotificationUrl = self.notification_url
        )['payKey']
        response = self.paypal.payment_details(
            payKey = payKey
        )
        self.assertEquals(response['responseEnvelope']['ack'], "Success")
        self.assertEquals(response['payKey'], payKey)
        self.assertEquals(response['actionType'], 'CREATE')
    
    def test_get_payment_options(self):
        payKey = self.paypal.pay_request(
            actionType = 'CREATE',
            cancelUrl = self.cancel_url,
            currencyCode = 'USD',
            senderEmail = API_EMAIL,
            feesPayer = 'EACHRECEIVER',
            receiverList = { 'receiver': [
                { 'amount':"1.0", 'email':EMAIL_ACCOUNT, }
            ]},
            returnUrl = self.return_url,
            ipnNotificationUrl = self.notification_url
        )['payKey']
        response = self.paypal.get_payment_options(
            payKey = payKey
        )
        self.assertEquals(response['responseEnvelope']['ack'], "Success")
    
    def test_preapproval(self):
        response = self.paypal.preapproval(
            clientDetails = {
                'ipAddress':'127.0.0.1',
            },
            startingDate = datetime.now(),
            endingDate = datetime.now() + timedelta(days=2),
            maxTotalAmountOfAllPayments = "10.00",
            currencyCode = 'USD',
            cancelUrl = self.cancel_url,
            returnUrl = self.return_url,
        )
        self.assertEquals(response['responseEnvelope']['ack'], "Success")
        self.assertTrue(response.has_key('preapprovalKey'))
    
    def test_preapproval_details(self):
        preapprovalKey = self.paypal.preapproval(
            clientDetails = {
                'ipAddress':'127.0.0.1',
            },
            startingDate = datetime.now(),
            endingDate = datetime.now() + timedelta(days=2),
            maxTotalAmountOfAllPayments = "10.00",
            currencyCode = 'USD',
            cancelUrl = self.cancel_url,
            returnUrl = self.return_url,
        )['preapprovalKey']
        response = self.paypal.preapproval_details(
            preapprovalKey = preapprovalKey
        )
        self.assertEquals(response['responseEnvelope']['ack'], "Success")
        self.assertEquals(response['returnUrl'], self.return_url)
        self.assertEquals(response['cancelUrl'], self.cancel_url)
        self.assertEquals(response['currencyCode'], 'USD')
    
    def test_cancel_preapproval(self):
        preapprovalKey = self.paypal.preapproval(
            clientDetails = {
                'ipAddress':'127.0.0.1',
            },
            startingDate = datetime.now(),
            endingDate = datetime.now() + timedelta(days=2),
            maxTotalAmountOfAllPayments = "10.00",
            currencyCode = 'USD',
            cancelUrl = self.cancel_url,
            returnUrl = self.return_url,
        )['preapprovalKey']
        response = self.paypal.cancel_preapproval(
            preapprovalKey = preapprovalKey
        )
        self.assertEquals(response['responseEnvelope']['ack'], "Success")
    
    def test_refund(self):
        payKey = self.paypal.pay_request(
            actionType = 'PAY',
            cancelUrl = self.cancel_url,
            currencyCode = 'USD',
            senderEmail = API_EMAIL,
            feesPayer = 'EACHRECEIVER',
            receiverList = { 'receiver': [
                { 'amount':"1.0", 'email':EMAIL_ACCOUNT, }
            ]},
            returnUrl = self.return_url,
            ipnNotificationUrl = self.notification_url
        )['payKey']
        response = self.paypal.refund(
            currencyCode = 'USD',
            payKey = payKey
        )
        self.assertEquals(response['responseEnvelope']['ack'], "Success")
    
    def test_convert_currency(self):
        response = self.paypal.convert_currency(
            baseAmountList = { 'currency': [{
                'amount':"10.00", 'code':'USD'
            }]},
            convertToCurrencyList = [ { 'currencyCode':'EUR' } ]
        )
        self.assertEquals(response['responseEnvelope']['ack'], "Success")
        self.assertTrue(response.has_key('estimatedAmountTable'))
    
