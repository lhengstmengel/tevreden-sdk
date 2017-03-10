import httplib2
from urllib.parse import urlencode
import urllib
import pprint
import json


class APIClient:

    def __init__( self, platform = None, api_key = None, domain = 'api.tevreden.nl', ssl_insecure = False ):
            
        self.platform = platform
        self.api_key = api_key
        self.domain = domain
        self.ssl_insecure = ssl_insecure;
        

    def call( self, method = 'GET', path = '/', params = {}, post_params = {}, body = '', headers = {} ):
        
        querystring = ''
        if (len(params) > 0):
            querystring = '?' + urlencode(params)
            
        if (len(post_params) > 0):
            headers['content-type'] = 'application/x-www-form-urlencoded'
            body = urlencode(post_params)

        headers.update({
            'tevreden-platform': self.platform, 
            'tevreden-api-key': self.api_key
        })
            
        h = httplib2.Http(".cache", disable_ssl_certificate_validation=self.ssl_insecure)
        (response, raw_content) = h.request(
            "https://%s%s%s" % (self.domain, path, querystring),
            method, 
            body=body, 
            headers=headers
        )

        content = raw_content.decode("utf-8")
        if response['content-type'] == 'application/json':
            decoded_content = json.loads(content)
        else:
            decoded_content = content
        
        if response.status == 200 or response.status == 201:
            return decoded_content
        elif response.status == 400:
            raise BadRequestError(decoded_content)
        elif response.status == 401:
            raise UnauthorizedError(decoded_content)
        elif response.status == 403:
            raise ForbiddenError(decoded_content)
        elif response.status == 404:
            raise NotFoundError(decoded_content)
        elif response.status == 405:
            raise MethodNotAllowedError(decoded_content)
        elif response.status == 420:
            raise TooManyRequestsError(decoded_content)
        elif response.status == 500:
            raise InternalServerError(decoded_content)
        elif response.status == 501:
            raise NotImplementedError(decoded_content)


    def get_platforms( self ):
        r = self.call( path = '/platforms' )
        return r['platforms']


    def get_locations( self, params = {} ):
        r = self.call( path = '/locations', params = params )
        return r['locations']
        
    def get_location( self, id, params = {} ):
        r = self.call( path = '/locations/%s' % id, params = params  )
        return r['location']

    def get_organisations( self, params = {} ):
        r = self.call( path = '/organisations', params = params )
        return r['organisations']
        
    def get_organisation( self, id, params = {} ):
        r = self.call( path = '/organisations/%s' % id, params = params )
        return r['organisation']


# Exceptions



class APIError(Exception):
    def __init__(self, response):
        self.response = response

class MissingPlatformError(APIError):
    pass
    
class MissingApiKeyError(APIError):
    pass

class BadRequestError(APIError):
    pass
    
class UnauthorizedError(APIError):
    pass

class ForbiddenError(APIError):
    pass

class NotFoundError(APIError):
    pass

class MethodNotAllowedError(APIError):
    pass

class TooManyRequestsError(APIError):
    pass
    
class InternalServerError(APIError):
    pass
    
class NotImplementedError(APIError):
    pass
    
