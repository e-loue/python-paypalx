# -*- coding: utf-8 -*-
VERSION = 0.1

import datetime
import socket
import simplejson as json
from httplib2 import Http
from urlparse import urljoin

X_PAYPAL_ERROR_RESPONSE = {
    'TRUE':True,
    'FALSE':False
}

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)
    

class PaypalError(Exception):
    def __init__(self, code, msg, headers):
        self.code = code
        self.msg = msg
        self.headers = headers
    
    def __getitem__(self, key):
        if key == 'code':
            return self.code
        try:
            return self.headers[key]
        except KeyError:
            raise AttributeError(key)
    
    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        if self.code:
            return "#%s %s" % (self.code, self.msg)
        else:
            return self.msg
    

class DecodeError(PaypalError):
    def __init__(self, headers, body):
        super(DecodeError, self).__init__(None, "Could not decode JSON", headers)
        self.body = body
    
    def __repr__(self):
        return "headers: %s, content: <%s>" % (self.headers, self.body)
    

class AdaptiveAPI(object):
    debug = False
    production_host = 'https://svcs.paypal.com/'
    sandbox_host = 'https://svcs.sandbox.paypal.com/'
    
    def __init__(self, username, password, signature, application_id, email, api_operation, sandbox=False):
        self.username = username
        self.password = password
        self.signature = signature
        self.application_id = application_id
        self.email = email
        self.api_operation = api_operation
        if sandbox:
            self.host = self.sandbox_host
        else:
            self.host = self.production_host
        self.http = Http()
    
    def _check_required(self, required, **kwargs):
        for requirement in required:
            if requirement not in kwargs:
                raise PaypalError(None, "Missing required args : %s" % requirement, kwargs)
    
    def _endpoint(self, name):
        return urljoin(urljoin(self.host, self.api_operation + '/'), name)
    
    def _request(self, endpoint, data=None):
        body = None
        if data:
            body = json.dumps(data, cls=JSONEncoder)
        
        if self.debug:
            print endpoint
        
        def device_ip():
            return socket.gethostbyname(socket.gethostname())
        
        headers = {
            'X-PAYPAL-SECURITY-USERID':self.username,
            'X-PAYPAL-SECURITY-PASSWORD':self.password,
            'X-PAYPAL-SECURITY-SIGNATURE':self.signature,
            'X-PAYPAL-APPLICATION-ID':self.application_id,
            'X-PAYPAL-SANDBOX-EMAIL-ADDRESS':self.email,
            'X-PAYPAL-DEVICE-IPADDRESS':device_ip(), 
            'X-PAYPAL-REQUEST-DATA-FORMAT':'JSON',
            'X-PAYPAL-RESPONSE-DATA-FORMAT':'JSON'
        }
        
        if self.debug:
            print headers
            print body
        
        response, content = self.http.request(endpoint, "POST", body=body, headers=headers)
        if self.debug:
            print response
            print content
        
        if response['status'][0] != '2':
            code = response['status']
            message = content
            raise PaypalError(code, message, response)
        
        if content:
            try:
                content = json.loads(content)
            except ValueError:
                raise DecodeError(response, content)
        
        if X_PAYPAL_ERROR_RESPONSE[response.get('x-paypal-error-response', 'FALSE')]:
            code = response['status']
            message = content
            if isinstance(content, dict):
                code = content['error'][0]['errorId']
                message = content['error'][0]['message']
            raise PaypalError(code, message, response)
        
        return content
    
