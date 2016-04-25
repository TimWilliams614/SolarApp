from .User2 import *
from time import gmtime, strftime, localtime
import os

class Locker:
	lockerCount = 0
	currentUser = -1

	def __init__(self, ID):
		self.id = ID
		self.state = 0 #0 = available, 1 = locked
		self.userTable = UserList()
		self.owner = '-1'
		self.lockTime = 'N\A'
		self.lockDuration = 0
		Locker.lockerCount += 1

	def display(self):
		print("locker name: ", self.id, "owner: ", self.owner, ", state: ", self.state)

	def updateUserTable(self):
		self.userTable.getUserInfo(self.userTable.dataFile)

	def lock(self, userIndex):
		self.updateUserTable()
		self.state = 1
		self.owner = self.userTable.userList[userIndex].cardID
		#print(self.userTable.userList[userIndex].lockerCount)
		self.userTable.userList[userIndex].lockerCount += 1
		self.userTable.writeData(self.userTable.dataFile)
		self.lockTime = strftime("%H:%M:%S", localtime())

	def unlock(self):
		self.updateUserTable()
		self.state = 0
		for element in self.userTable.userList:
			if element.cardID == str(self.owner):
				element.lockerCount -= 1
				break
		self.owner = '-1'
		self.userTable.writeData(self.userTable.dataFile)
		self.lockDuration = 0
		self.lockTime = 'N\A'

def createLockerList(lockerAmount):
	lockerArray = []
	for i in range(lockerAmount):
		lockerArray.append(Locker(i))
	return lockerArray

class LockerList:
	def __init__(self):
		self.lockerList = []
		self.dataFile = "backend/locker.txt" #id state owner
		self.logFile = "backend/log.txt"
		self.getLockerInfo(self.dataFile)
		#user-related variables
		self.userTable = UserList()
		self.currentUser = '-1'
		self.userIndex = -1
		self.userStatus = 0 #0 = normal user, 1 = super user
		self.limit = 2 #max locker per user

	def display(self):
		print("\nuserID: ", self.currentUser, ", status: ", self.userStatus, 'yellow')
		if self.currentUser != '-1':
			for element in self.lockerList:
					if element.state == 1:
						if element.owner == self.currentUser:
							print("locker name: ", element.id, "owner: ", element.owner, ", state: owned", "green")
						else:
							print("locker name: ", element.id, "owner: ", element.owner, ", state: locked", 'red')
					else:
						print("locker name: ", element.id, "owner: ", element.owner, ", state: available")
		else:
			print("no display\n", 'red')

	def lockerState(self, lockerID): # this returns: 0 = available, 1 = locked, 2 = owned
		state = self.lockerList[lockerID].state
		owner = self.lockerList[lockerID].owner
		if state == 1:
			if owner == self.currentUser:
				return 2
			else:
				return 1
		else:
			return 0

	def checkLogin(self, newUser):
		found = 0
		i = 0
		for element in self.userTable.userList:
			self.userIndex = -1
			if element.cardID == str(newUser):
				self.userIndex = i
				found = 1
				break
			i += 1
		return found

	def login(self, newUser): #use cardID to login so newUser is cardID, return 1 if newUser is valid
		if self.checkLogin(newUser) == 1:
			self.currentUser = newUser
			self.userStatus = self.userTable.userList[self.userIndex].status
			return 1
		else:
			return 0

	def logout(self):
		self.currentUser = -1
		self.userIndex = -1
		self.userStatus = 0

	def updateUserTable(self):
		self.userTable.getUserInfo(self.userTable.dataFile)

	def chooseLocker(self, lockerPosition):
		action = ''
		lockerID = self.lockerList[lockerPosition].id
		lockerOwner = self.lockerList[lockerPosition].owner
		self.updateUserTable()
		i = self.userIndex
		uL = self.userTable.userList #uL = userList

		if lockerPosition >= len(self.lockerList) or lockerPosition < 0 or self.currentUser == -1: #lockerPosition is invalid or currentUser is -1
			print(colored("invalid",'red'))
		else:
			if self.lockerList[lockerPosition].state == 0: #if locker is available
				if uL[i].lockerCount < self.limit: #if user locker count is below limit
					self.lockerList[lockerPosition].lock(i)
					action = 'lock'
				else:
					print('you are owning maximum amount of lockers', 'red')
			else:
				if self.lockerList[lockerPosition].owner == self.currentUser: #if locked locker is owned by user
					self.lockerList[lockerPosition].unlock()
					action = 'unlock'
				else:
					if self.userStatus != 1: #not a super user
						print('you cannot interact with this locker', 'red')
					else: #if it is super user
						self.lockerList[lockerPosition].unlock()
						action = 'super-unlock'
			self.writeData(self.dataFile)
			self.recordLog(self.logFile, lockerID, lockerOwner, action)

	def writeData(self, fileName):
		#id state owner bool_recordTime startTime duration
		openFile = open(fileName, 'w')
		openFile.write(str(len(self.lockerList)) + "\n")
		for element in self.lockerList:
			openFile.write(str(element.id) + " " + str(element.state) + " " + str(element.owner) + " " + str(element.lockDuration) + " " + str(element.lockTime) + "\n")
		openFile.close()

	def getLockerInfo(self, fileName):
		openFile = open(fileName, 'r')
		arraySize = int(next(openFile))
		self.lockerList = createLockerList(arraySize)
		for line in openFile:
			i = int(line.split()[0])
			self.lockerList[i].id = i
			self.lockerList[i].state = int(line.split()[1])
			self.lockerList[i].owner = int(line.split()[2])
			self.lockerList[i].lockDuration = int(line.split()[3])
			self.lockerList[i].lockTime = line.split()[4]
		openFile.close()

	def recordLog(self, fileName, lockerID, lockerOwner, action):
		#Y-M-D H-M-S currentUser currentUserStatus lockerID lockerOwner action
		if os.stat(fileName).st_size == 0:
			with open(fileName, 'w') as openFile:
				openFile.write('year-month-day hour-min-sec currentUser currentUserStatus lockerID lockerOwner action\n')
				openFile.close()
		else:
			if action != '':
				openFile = open(fileName, 'a') 
				dateTimeStr = strftime("%Y-%m-%d %H:%M:%S", localtime())
				outputStr = dateTimeStr + " " + str(self.currentUser) + " " + str(self.userStatus) + " "
				outputStr += str(lockerID) + " " + str(lockerOwner) + " "
				outputStr += action + "\n"
				openFile.write(outputStr)
				openFile.close()

	def cleanLog(self, fileName):
		with open(fileName, 'w') as openFile:
			openFile.write('year-month-day hour-min-sec currentUser currentUserStatus lockerID lockerOwner action\n')
			openFile.close()


#lockerSys.cleanLog(lockerSys.logFile)
#lockerSys.display()