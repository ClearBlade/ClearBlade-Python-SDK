class Client():
	pass

class UserClient(Client):
	def __init__(self, systemKey, systemSecret, email, password, platform='https://platform.clearblade.com'):
		self.UserToken = ""
		self.systemKey = systemKey
		self.systemSecret = systemSecret
		self.email = email 
		self.password = password
		self.platform = platform
	
class DevClient(Client):
	def __init__(self, systemKey, systemSecret, email, password, platform='https://platform.clearblade.com'):
		self.DevToken = ""
		self.systemKey = systemKey
		self.systemSecret = systemSecret
		self.email = email 
		self.password = password	
		self.platform = platform	

class DeviceClient(Client):
	def __init__(self, systemKey, systemSecret, deviceName, activeKey, platform='https://platform.clearblade.com'):
		self.DeviceToken = ""
		self.systemKey = systemKey
		self.systemSecret = systemSecret
		self.deviceName = deviceName
		self.activeKey = activeKey
		self.platform = platform