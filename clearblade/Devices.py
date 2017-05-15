import Client
import requests
import json

class Devices():
    def __init__(self, client):
        self.client = client
        self.headers = {
            'ClearBlade-SystemKey': self.client.systemKey,
            'ClearBlade-SystemSecret': self.client.systemSecret,
			'Content-Type': 'application/json'
        }
        if isinstance(self.client, Client.UserClient):
			self.headers['ClearBlade-UserToken'] = self.client.UserToken
        elif isinstance(self.client, Client.DevClient):
            self.headers['ClearBlade-DevToken'] = self.client.DevToken
        elif isinstance(self.client, Client.DeviceClient):
            self.headers['ClearBlade-DeviceToken'] = self.client.DeviceToken
        self.url = self.client.platform + '/api/v/2/devices/' + self.client.systemKey

    def getAllDevices(self):
        resp = requests.get(self.url, headers=self.headers)
        if resp.status_code == 200:
            try:
                resp = json.loads(resp.text)
                return resp
            except ValueError:
                print("Failed to decode response JSON: {0}".format(resp.text))
        else:
            print("Request failed with status code: {0} and response text: {1}".format(resp.status_code, resp.text))

    def updateDevice(self, deviceName, updates):
        resp = requests.put(self.url + "/" + deviceName, headers=self.headers, json=updates)
        if resp.status_code == 200:
            try:
                resp = json.loads(resp.text)
                return resp
            except ValueError:
                print("Failed to decode response JSON: {0}".format(resp.text))
        else:
            print("Request failed with status code: {0} and response text: {1}".format(resp.status_code, resp.text))