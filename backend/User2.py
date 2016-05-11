class User:
	def __init__(self, cardID):
		self.cardID = cardID
		self.status = 0 #user status 0 = normal user, 1 = super user
		self.lockerCount = 0

	def changeStatus(self, input):
		self.status = input

class UserList:
	def __init__(self):
		self.dataFile = "backend/user.txt" #cardID status lockerCount
		self.userList = []
		self.getUserInfo(self.dataFile)

	def getUserInfo(self, fileName):
		openFile = open(fileName, 'r')
		self.userList = []
		for line in openFile:
			lineSplit = line.split()
			userTemp = User(lineSplit[0])
			self.userList.append(userTemp)
			self.userList[-1].status = int(lineSplit[1])
			self.userList[-1].lockerCount = int(lineSplit[2])
		openFile.close()
		
	def writeData(self, fileName):
		openFile = open(fileName, 'w')
		for element in self.userList:
			openFile.write(str(element.cardID) + " " + str(element.status) + " " + str(element.lockerCount) + "\n")
		openFile.close()

	def addUser(self, cardID):
		if cardID != '':	
			openFile = open(self.dataFile, 'a')
			openFile.write(str(cardID) + " " + str(0) + " " + str(0) + "\n")
			openFile.close()

			#add new user entry to the list
			userTemp = User(str(cardID))
			self.userList.append(userTemp)

	def display(self):
		for element in self.userList:
			string = "cardID: " + element.cardID
			string += ", status: " + str(element.status)
			string += ", lockerCount: " + str(element.lockerCount)
			print(string)