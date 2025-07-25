from __future__ import absolute_import
import paho.mqtt.client as mqtt
import uuid
from . import cbLogs, cbErrors


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
        cbErrors.handle(-1)
    else:
        return s[0]


class Messaging:
    def __init__(self, user=None, port=1883, keepalive=30, url="", client_id="", clean_session=None, use_tls=False):
        # mqtt client
        self.__mqttc = (client_id != "" and mqtt.Client(client_id=client_id)) or mqtt.Client(client_id=uuid.uuid4().hex)
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
        self.__use_tls = use_tls

    def __connect_cb(self, client, userdata, flags, rc):
        if rc == 0:
            cbLogs.info("Connected to MQTT broker at", self.__url, "port", str(self.__port) + ".")
        elif rc == 1:
            cbLogs.error("MQTT connection to", self.__url, "port", str(self.__port) + ".", "refused. Incorrect protocol version.")  # I should probably fix this
            cbErrors.handle(-1)
        elif rc == 2:
            cbLogs.error("MQTT connection to", self.__url, "port", str(self.__port) + ".", "refused. Invalid client identifier.")
            cbErrors.handle(-1)
        elif rc == 3:
            cbLogs.error("MQTT connection to", self.__url, "port", str(self.__port) + ".", "refused. Server unavailable.")
            cbErrors.handle(-1)
        elif rc == 4:
            cbLogs.error("MQTT connection to", self.__url, "port", str(self.__port) + ".", "refused. Bad username or password.")
            cbErrors.handle(-1)
        elif rc == 5:
            cbLogs.error("MQTT connection to", self.__url, "port", str(self.__port) + ".", "refused. Not authorized.")
            cbErrors.handle(-1)
        else:
            cbLogs.error("MQTT connection to", self.__url, "port", str(self.__port) + ".", "refused. Tell ClearBlade to update their SDK for this case. rc=" + rc)
            cbErrors.handle(-1)
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

    def set_will(self, topic, payload, qos = 0, retain = False):
        """
        Set a Will to be sent by the broker in case the client disconnects unexpectedly.
        This must be called before connect() to have any effect.

        :param str topic: The topic that the will message should be published on.
        :param payload: The message to send as a will. If not given, or set to None a
            zero length message will be used as the will. Passing an int or float
            will result in the payload being converted to a string representing
            that number. If you wish to send a true int/float, use struct.pack() to
            create the payload you require.
        :param int qos: The quality of service level to use for the will.
        :param bool retain: If set to true, the will message will be set as the retained message for the topic.
        """

        self.__mqttc.will_set(topic, payload, qos, retain)

    def clear_will(self):
        """
        Removes a will that was previously configured with `set_will()`.
        Must be called before connect() to have any effect.
        """
        self.__mqttc.will_clear()

    def connect(self, will_topic=None, will_payload=1883):
        cbLogs.info("Connecting to MQTT.")
        if self.__use_tls:
            try:
                self.__mqttc.tls_set()
            except ValueError as e:
                if str(e) == "SSL/TLS has already been configured.":
                    pass
                else:
                    raise e
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

    def publish(self, channel, message, qos=0, retain=False):
        msgType = type(message).__name__
        try:
            if msgType == "str":
                logMsg = message
            else:
                logMsg = str(message)
        except:
            logMsg = "unstringifiable object"
        cbLogs.info("Publishing", logMsg, "to", channel, ".")
        resp = self.__mqttc.publish(channel, message, qos, retain)
        return resp
