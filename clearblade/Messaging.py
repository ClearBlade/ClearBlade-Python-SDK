from __future__ import absolute_import
import paho.mqtt.client as mqtt
from . import cbLogs


# This function strips the scheme and the port (if they exist) off the given url
def parse_url(url):
    s = url.split(":")
    if len(s) == 3:  # we've got http and a port. get rid of them
        return s[1][2:]
    elif len(s) == 2:  # we've either got a port or an http
        try:
            int(s[1])  # if it's a port, we'll be able to convert to int
        except ValueError:
            return s[1][2:]
        else:
            return s[0]
    elif len(s) > 3:
        cbLogs.error("Couldn't parse this url:", url)
        exit(-1)
    else:
        return s[0]


class Messaging:
    def __init__(self, user=None, port=1883, keepalive=30, url=""):
        # mqtt client
        self.__mqttc = mqtt.Client()
        self.__mqttc.username_pw_set(user.token, user.system.systemKey)

        # default callback functions
        # these are wrappers for the user defined callbacks
        # we do it this way so we can log debug info and errors
        # and still allow users to update them without calling a function
        self.__mqttc.on_connect = self.__connect_cb
        self.__mqttc.on_disconnect = self.__disconnect_cb
        self.__mqttc.on_subscribe = self.__subscribe_cb
        self.__mqttc.on_unsubscribe = self.__unsubscribe_cb
        self.__mqttc.on_publish = self.__publish_cb
        self.__mqttc.on_message = self.__message_cb
        self.__mqttc.on_log = self.__log_cb

        # user defined callback functions
        self.on_connect = None
        self.on_disconnect = None
        self.on_subscribe = None
        self.on_unsubscribe = None
        self.on_publish = None
        self.on_message = None
        self.on_log = None

        # internal variables
        if url:
            self.__url = parse_url(url)
        else:
            self.__url = parse_url(user.system.url)
        self.__port = port
        self.__keepalive = keepalive
        self.__qos = 0

    def __connect_cb(self, client, userdata, flags, rc):
        if rc == 0:
            cbLogs.info("Connected to MQTT broker at", self.__url, "port", str(self.__port) + ".")
        elif rc == 1:
            cbLogs.error("MQTT connection to", self.__url, "port", str(self.__port) + ".", "refused. Incorrect protocol version.")  # I should probably fix this
            exit(-1)
        elif rc == 2:
            cbLogs.error("MQTT connection to", self.__url, "port", str(self.__port) + ".", "refused. Invalid client identifier.")
            exit(-1)
        elif rc == 3:
            cbLogs.error("MQTT connection to", self.__url, "port", str(self.__port) + ".", "refused. Server unavailable.")
            exit(-1)
        elif rc == 4:
            cbLogs.error("MQTT connection to", self.__url, "port", str(self.__port) + ".", "refused. Bad username or password.")
            exit(-1)
        elif rc == 5:
            cbLogs.error("MQTT connection to", self.__url, "port", str(self.__port) + ".", "refused. Not authorized.")
            exit(-1)
        else:
            cbLogs.error("MQTT connection to", self.__url, "port", str(self.__port) + ".", "refused. Tell ClearBlade to update their SDK for this case. rc=" + rc)
            exit(-1)
        if self.on_connect:
            self.on_connect(client, userdata, flags, rc)

    def __disconnect_cb(self, client, userdata, rc):
        if rc == 0:
            cbLogs.info("Disconnected from MQTT broker at", self.__url, "port", str(self.__port) + ".")
        else:
            cbLogs.error("Unexpected disconnect from MQTT broker at", self.__url, "port", str(self.__port) + ". Check your network.")
        if self.on_disconnect:
            self.on_disconnect(client, userdata, rc)

    def __subscribe_cb(self, client, userdata, mid, granted_qos):
        if self.on_subscribe:
            self.on_subscribe(client, userdata, mid, granted_qos)

    def __unsubscribe_cb(self, client, userdata, mid):
        if self.on_unsubscribe:
            self.on_unsubscribe(client, userdata, mid)

    def __publish_cb(self, client, userdata, mid):
        if self.on_publish:
            self.on_publish(client, userdata, mid)

    def __message_cb(self, client, userdata, message):
        if self.on_message:
            self.on_message(client, userdata, message)

    def __log_cb(self, client, userdata, level, buf):
        cbLogs.mqtt(level, buf)
        if self.on_log:
            self.on_log(client, userdata, level, buf)

    def connect(self):
        cbLogs.info("Connecting to MQTT.")
        self.__mqttc.connect(self.__url, self.__port, self.__keepalive)
        self.__mqttc.loop_start()

    def disconnect(self):
        cbLogs.info("Disconnecting from MQTT.")
        self.__mqttc.loop_stop()
        self.__mqttc.disconnect()

    def subscribe(self, channel):
        cbLogs.info("Subscribing to:", channel)
        self.__mqttc.subscribe(channel, self.__qos)

    def unsubscribe(self, channel):
        cbLogs.info("Unsubscribing from:", channel)
        self.__mqttc.unsubscribe(channel)

    def publish(self, channel, message, qos=0):
        cbLogs.info("Publishing", message, "to", channel, ".")
        self.__mqttc.publish(channel, message, qos)
