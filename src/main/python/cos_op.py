import re
import json
import datetime
from requests.utils import quote
import hashlib
import hmac
import pandas as pd
import time


def get_hash(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()


def create_signature_key(key, datestamp, region, service):
    key_date = get_hash(('AWS4' + key).encode('utf-8'), datestamp)
    key_region = get_hash(key_date, region)
    key_service = get_hash(key_region, service)
    key_signing = get_hash(key_service, 'aws4_request')
    return key_signing


def generate_link(filename, credentials, expiration):
    region = ''
    http_method = 'GET'
    endpoint = 'https://' + credentials['host']
    
    cur_time = datetime.datetime.utcnow()
    timestamp = cur_time.strftime('%Y%m%dT%H%M%SZ')
    datestamp = cur_time.strftime('%Y%m%d')

    standardized_querystring = ('X-Amz-Algorithm=AWS4-HMAC-SHA256' +
                                '&X-Amz-Credential=' + credentials['access_key_id'] + '/' + datestamp + '/' + region +
                                '/s3/aws4_request' +
                                '&X-Amz-Date=' + timestamp +
                                '&X-Amz-Expires=' + str(expiration) +
                                '&X-Amz-SignedHeaders=host')

    standardized_querystring_url_encoded = quote(standardized_querystring, safe='&=')

    standardized_resource = '/' + credentials['BUCKET'] + '/' + filename
    standardized_resource_url_encoded = quote(standardized_resource, safe='&')

    payload_hash = 'UNSIGNED-PAYLOAD'
    standardized_headers = 'host:' + credentials['host']
    signed_headers = 'host'

    standardized_request = (http_method + '\n' +
                            standardized_resource + '\n' +
                            standardized_querystring_url_encoded + '\n' +
                            standardized_headers + '\n' +
                            '\n' +
                            signed_headers + '\n' +
                            payload_hash)

    # assemble string-to-sign
    hashing_algorithm = 'AWS4-HMAC-SHA256'
    credential_scope = datestamp + '/' + region + '/' + 's3' + '/' + 'aws4_request'
    sts = (hashing_algorithm + '\n' +
           timestamp + '\n' +
           credential_scope + '\n' +
           hashlib.sha256(standardized_request.encode('utf-8')).hexdigest())

    # generate the signature
    signature_key = create_signature_key(credentials['secret_key'], datestamp, region, 's3')
    signature = hmac.new(signature_key,
                         sts.encode('utf-8'),
                         hashlib.sha256).hexdigest()

    # create and send the request
    request_url = (endpoint + '/' +
                   credentials['BUCKET'] + '/' +
                   filename + '?' +
                   standardized_querystring_url_encoded +
                   '&X-Amz-Signature=' +
                   signature)
    return request_url