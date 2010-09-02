# -*- coding: utf-8 -*-
from unittest import TestCase
from paypalx.accounts import AccountsAPI

try:
    import credentials
except ImportError:
    pass

API_USERNAME = getattr(credentials, 'API_USERNAME', "xxx_xxx_apix.xxx.com")
API_PASSWORD = getattr(credentials, 'API_PASSWORD', 'xxxxxxxxxx')
API_SIGNATURE = getattr(credentials, 'API_SIGNATURE', 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
API_APPLICATION_ID = getattr(credentials, 'API_APPLICATION_ID', 'APP-80W284485P519543T')
API_EMAIL = getattr(credentials, 'API_EMAIL', 'custX_xxxxxxxxxx_per@xxxxxxxx.com')

VISA_NUMBER = getattr(credentials, 'VISA_NUMBER', 'xxxxxxxxxxxxxxxx')
VISA_EXPIRATION = getattr(credentials, 'VISA_EXPIRATION', 'mmyyyy')

class TestAdaptiveAccounts(TestCase):
    notification_url = "http://notify.me"
    return_url = "http://return.me"
    
    def setUp(self):
        self.paypal = AccountsAPI(API_USERNAME, API_PASSWORD, API_SIGNATURE, API_APPLICATION_ID, API_EMAIL, sandbox=True)
        self.paypal.debug = False
    
    def test_create_account(self):
        response = self.paypal.create_account(
            accountType = 'Premier',
            emailAddress = 'john.doe@paypal.com',
            name = {
                'firstName':'John',
                'lastName':'Doe' 
            },
            dateOfBirth = '1968-01-01',
            address = {
                'line1':'90210, Melrose Place',
                'city':'Beverly Hills',
                'postalCode':'90210',
                'state':'CA',
                'countryCode':'US'
            },
            contactPhoneNumber = '888-555-1212',
            currencyCode = 'USD',
            citizenshipCountryCode = 'US',
            preferredLanguageCode = 'en_US',
            notificationURL = self.notification_url,
            createAccountWebOptions = {
                'returnUrl':self.return_url
            }
        )
        self.assertEquals(response['responseEnvelope']['ack'], "Success")
        self.assertEquals(response['execStatus'], "COMPLETED")
        self.assertTrue(response.has_key('createAccountKey'))
    
    def test_add_bank_account(self):
        response = self.paypal.add_bank_account(
            emailAddress = 'john.doe@paypal.com',
            confirmationType = 'WEB',
            bankCountryCode = 'US'
        )
        self.assertEquals(response['responseEnvelope']['ack'], "Success")
        self.assertEquals(response['execStatus'], "COMPLETED")
    
    def test_add_payment_card(self):
        response = self.paypal.add_payment_card(
            emailAddress = "john.doe@paypal.com",
            billingAddress = {
                'line1':'90210, Melrose Place',
                'city':'Beverly Hills',
                'postalCode':'90210',
                'state':'CA',
                'countryCode':'US'
            },
            cardType = 'Visa',
            cardNumber = VISA_NUMBER,
            confirmationType = 'WEB',
            nameOnCard = {
                'firstName':'John',
                'lastName':'Doe' 
            },
            expirationDate = {
                'month':VISA_EXPIRATION[:2],
                'year':VISA_EXPIRATION[2:6]
            }
        )
        self.assertEquals(response['responseEnvelope']['ack'], "Success")
        self.assertEquals(response['execStatus'], "WEB_URL_VERIFICATION_NEEDED")
        self.assertTrue(response.has_key('fundingSourceKey'))
    
    def test_set_funding_source_confirmed(self):
        fundingSourceKey = self.paypal.add_payment_card(
            emailAddress = "joey.triviani@paypal.com",
            billingAddress = {
                'line1':'90210, Melrose Place',
                'city':'Beverly Hills',
                'postalCode':'90210',
                'state':'CA',
                'countryCode':'US'
            },
            cardType = 'Visa',
            cardNumber = '4914240823748958',
            confirmationType = 'WEB',
            nameOnCard = {
                'firstName':'Joey',
                'lastName':'Triviani' 
            },
            expirationDate = {
                'month':'09',
                'year':'2015'
            }
        )['fundingSourceKey']
        response = self.paypal.set_funding_source_confirmed(
            emailAddress = "joey.triviani@paypal.com",
            fundingSourceKey = fundingSourceKey,
            createAccountKey = createAccountKey
        )
        self.assertEquals(response['responseEnvelope']['ack'], "Success")
    
    def test_get_verified_status(self):
        response = self.paypal.get_verified_status(
            emailAddress = "john.doe@paypal.com",
            firstName = 'John',
            lastName = 'Doe',
            matchCriteria = 'NAME'
        )
        self.assertEquals(response['responseEnvelope']['ack'], "Success")
        self.assertEquals(response['accountStatus'], 'VERIFIED')
    
    def test_get_user_agreement(self):
        response = self.paypal.get_user_agreement(
            languageCode = 'en_US',
            countryCode = 'US'
        )
        self.assertEquals(response['responseEnvelope']['ack'], "Success")
        self.assertTrue('PayPal' in response['agreement'])
    
