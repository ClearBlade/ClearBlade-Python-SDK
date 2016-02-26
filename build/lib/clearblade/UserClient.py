# from auth import Auth

class Client():
	pass

class UserClient(Client):
	def __init__(self, systemKey, systemSecret, email, password):
		self.UserToken = ""
		self.systemKey = systemKey
		self.systemSecret = systemSecret
		self.email = email 
		self.password = password

	# def Auth(self):
	# 	auth.Auth().Authenticate(UserClient)		