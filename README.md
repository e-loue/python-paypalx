python-paypalx
==============

python-paypalx is a client library for Adaptive PayPal's API.


Installation
------------

python-paypalx requires `httplib2` and `simplejson` to work.


Usage
-----

    from paypalx import PaypalError, AdaptivePayments, AdaptiveAccounts

    accounts = AdaptiveAccounts(
        PAYPAL_API_USERNAME,
        PAYPAL_API_PASSWORD,
        PAYPAL_API_SIGNATURE,
        PAYPAL_API_APPLICATION_ID,
        PAYPAL_API_EMAIL,
        sandbox=USE_PAYPAL_SANDBOX
    )    
    
    payments = AdaptivePayments(
        PAYPAL_API_USERNAME,
        PAYPAL_API_PASSWORD,
        PAYPAL_API_SIGNATURE,
        PAYPAL_API_APPLICATION_ID,
        PAYPAL_API_EMAIL,
        sandbox=USE_PAYPAL_SANDBOX
    )
    
    
