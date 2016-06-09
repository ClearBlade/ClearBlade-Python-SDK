class Client():
	pass

class UserClient(Client):
	def __init__(self, systemKey, systemSecret, email, password, platform):
		self.UserToken = ""
		self.systemKey = systemKey
		self.systemSecret = systemSecret
		self.email = email 
		self.password = password
		self.platform = platform
	
class DevClient(Client):
	def __init__(self, systemKey, systemSecret, email, password, platform):
		self.DevToken = ""
		self.systemKey = systemKey
		self.systemSecret = systemSecret
		self.email = email 
		self.password = password	
		self.platform = platform	