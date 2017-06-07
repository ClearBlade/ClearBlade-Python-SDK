import paho.mqtt.client as mqtt
import cbLogs
import time


class Messaging:
    def __init__(self, user, port=1883, keepalive=30, url=""):
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
            self.__url = self.__parse_url(url)
        else:
            self.__url = self.__parse_url(user.url)
        self.__port = port
        self.__keepalive = keepalive
        self.__qos = 0

    def __parse_url(self, url):
        s = url.split("/api/v/1/user")[0]
        s = s.split(":")
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
            cbLogs.error("wth kind of url is this??", url)
            exit(-1)
        else:
            return s[0]

    def __connect_cb(self, client, userdata, flags, rc):
        if rc == 0:
            cbLogs.info("Connected to MQTT broker at", self.__url, "port", str(self.__port) + ".")
        elif rc == 1:
            cbLogs.error("MQTT connection to", self.__url, "port", str(self.__port) + ".", "refused. Incorrect protocol version.")  # I should probably fix this
        elif rc == 2:
            cbLogs.error("MQTT connection to", self.__url, "port", str(self.__port) + ".", "refused. Invalid client identifier.")
        elif rc == 3:
            cbLogs.error("MQTT connection to", self.__url, "port", str(self.__port) + ".", "refused. Server unavailable.")
        elif rc == 4:
            cbLogs.error("MQTT connection to", self.__url, "port", str(self.__port) + ".", "refused. Bad username or password.")
        elif rc == 5:
            cbLogs.error("MQTT connection to", self.__url, "port", str(self.__port) + ".", "refused. Not authorized.")
        else:
            cbLogs.error("MQTT connection to", self.__url, "port", str(self.__port) + ".", "refused. Tell ClearBlade to update their SDK for this case. rc=" + rc)
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
        self.__mqttc.connect_async(self.__url, self.__port, self.__keepalive)
        self.__mqttc.loop_start()
        time.sleep(1)  # subscribing will not work without this delay so I baked it in

    def disconnect(self):
        self.__mqttc.loop_stop()
        self.__mqttc.disconnect()

    def subscribe(self, channel):
        cbLogs.info("Subscribing to:", channel)
        self.__mqttc.subscribe(channel, self.__qos)

    def publish(self, channel, message):
        self.__mqttc.publish(channel, message)
