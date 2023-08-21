from __future__ import print_function, absolute_import
import json
import ssl
import requests
from requests.exceptions import *
from . import cbLogs
from .cbLogs import prettyText


def panicmessage(resp, reqtype, url, headers, params="", data=""):
    # beep beep beep
    print("")
    print(prettyText.bold + prettyText.italics + prettyText.yellow + reqtype + prettyText.endColor, "request to", prettyText.underline + url + prettyText.endColor, "failed with status code", prettyText.bold + prettyText.red + str(resp.status_code) + prettyText.endColor)
    print(prettyText.bold + "HEADERS USED:" + prettyText.endColor, headers)
    if params:
        print(prettyText.bold + "PARAMS SENT:" + prettyText.endColor, params)
    if data:
        print(prettyText.bold + "DATA SENT:" + prettyText.endColor, data)
    try:
        print(prettyText.bold + "DETAILS:" + prettyText.endColor, prettyText.bold + prettyText.purple + json.loads(resp.text)["error"]["detail"] + prettyText.endColor)
    except ValueError:
        print(prettyText.bold + "DETAILS:" + prettyText.endColor, "No details provided.")
    print("")
    print(prettyText.bold + "FULL RESPONSE:" + prettyText.endColor, resp.text)
    print("")


def get(url, headers={}, params={}, silent=False, sslVerify=True):
    # try our request
    try:
        resp = requests.get(url, headers=headers, params=params, verify=sslVerify)
    except ConnectionError:
        cbLogs.error("Connection error. Check that", url, "is up and accepting requests.")
        exit(-1)

    # check for errors
    if resp.status_code == 200:
        try:
            resp = json.loads(resp.text)
        except ValueError:
            resp = resp.text
    elif not silent:  # some requests are meant to fail
        panicmessage(resp, "GET", url, headers, params=params)
        exit(-1)

    # return successful response
    return resp


def post(url, headers={}, data={}, silent=False, sslVerify=True, x509keyPair=None):
    # make sure our data is valid json
    try:
        json.loads(data)
    except TypeError:
        data = json.dumps(data)

    if x509keyPair == None:
        # try our request
        try:
            resp = requests.post(url, headers=headers, data=data, verify=sslVerify)
        except ConnectionError:
            cbLogs.error("Connection error. Check that", url, "is up and accepting requests.")
            exit(-1)
    else:
        # MTLS auth, so create a new SSL context
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            # Load the cert and key
            context.load_cert_chain(certfile=x509keyPair["certfile"], keyfile=x509keyPair["keyfile"])
            adapter = requests.adapters.HTTPAdapter(pool_connections=1, pool_maxsize=1, pool_block=True)
            adapter.poolmanager.connection_pool_kw['ssl_context'] = context
            s = requests.session()
            s.mount('https://', adapter)
            resp = s.post(url, headers=headers, data=data, verify=sslVerify)
        except ConnectionError:
            cbLogs.error("Connection error. Check that", url, "is up and accepting requests.")
            exit(-1)


    # check for errors
    if resp.status_code == 200:
        try:
            resp = json.loads(resp.text)
        except ValueError:
            resp = resp.text
    elif not silent:  # some requests are meant to fail
        panicmessage(resp, "POST", url, headers, data=data)
        exit(-1)

    # return successful response
    return resp


def put(url, headers={}, data={}, silent=False, sslVerify=True):
    # make sure our data is valid json
    try:
        json.loads(data)
    except TypeError:
        data = json.dumps(data)

    # try our request
    try:
        resp = requests.put(url, headers=headers, data=data, verify=sslVerify)
    except ConnectionError:
        cbLogs.error("Connection error. Check that", url, "is up and accepting requests.")
        exit(-1)

    # check for errors
    if resp.status_code == 200:
        try:
            resp = json.loads(resp.text)
        except ValueError:
            resp = resp.text
    elif not silent:  # some requests are meant to fail
        panicmessage(resp, "PUT", url, headers, data=data)
        exit(-1)

    # return successful response
    return resp


def delete(url, headers={}, params={}, silent=False, sslVerify=True):
    # try our request
    try:
        resp = requests.delete(url, headers=headers, params=params, verify=sslVerify)
    except ConnectionError:
        cbLogs.error("Connection error. Check that", url, "is up and accepting requests.")
        exit(-1)

    # check for errors
    if resp.status_code == 200:
        try:
            resp = json.loads(resp.text)
        except ValueError:
            resp = resp.text
    elif not silent:  # some requests are meant to fail
        panicmessage(resp, "DELETE", url, headers, params=params)
        exit(-1)

    # return successful response
    return resp
