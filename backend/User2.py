class User:
	def __init__(self, cardID, UCMID):
		self.cardID = cardID
		self.UCMID = UCMID
		self.name = ""
		self.status = 0 #user status 0 = normal user, 1 = super user
		self.lockerCount = 0

	def changeStatus(self, input):
		self.status = input

class UserList:
	def __init__(self):
		self.dataFile = "backend/user.txt" #cardID UCMID status lockerCount name
		self.userList = []
		self.getUserInfo(self.dataFile)

	def getUserInfo(self, fileName):
		openFile = open(fileName, 'r')
		self.userList = []
		for line in openFile:
			lineSplit = line.split()
			userTemp = User(lineSplit[0], lineSplit[1])
			self.userList.append(userTemp)
			self.userList[-1].status = int(lineSplit[2])
			self.userList[-1].lockerCount = int(lineSplit[3])
			for i in lineSplit[4:]:
				self.userList[-1].name += (i + " ")
			self.userList[-1].name = self.userList[-1].name[:-1]
		openFile.close()
		
	def writeData(self, fileName):
		openFile = open(fileName, 'w')
		for element in self.userList:
			openFile.write(str(element.cardID) + " " + str(element.UCMID) + " " + str(element.status) + " " + str(element.lockerCount) + " " + str(element.name) + "\n")
		openFile.close()

	def display(self):
		for element in self.userList:
			string = "name: " + element.name
			string += ", cardID: " + element.cardID
			string += ", UCMID: " + element.UCMID
			string += ", status: " + str(element.status)
			string += ", lockerCount: " + str(element.lockerCount)
			print(string)