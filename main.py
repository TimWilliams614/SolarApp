from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.behaviors import *
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import *
from kivy.lang import Builder
from kivy.config import Config
from kivy.clock import Clock

from backend import LockerList
from time import gmtime, strftime, localtime
from kivy.uix.behaviors import ToggleButtonBehavior

#--load in kv files --#
Builder.load_file('navBar.kv')
Builder.load_file('idle.kv')
Builder.load_file('consumption.kv')
Builder.load_file('lockerInfo.kv')
Builder.load_file('lockerAccess.kv')
Builder.load_file('about.kv')
#-- end load -- #

#---Initial Configuration---#
Config.set('graphics','borderless','1') #removes border decoration
Config.set('graphics','height','480') #static height due to tablet constraints
Config.set('graphics','width','800') #static width due to tablet constraints
Config.set('graphics','resizable','0') #Make unresizable so user can't resize or move whole window
#---End of Configuration---#

#---initiate back end---#
lockerSys = LockerList()
#---end of initiation---#

#--- Widget/Screen Definitions Passed from KV file ---#
class NavBar(Screen):

	#make consumption button "untogglable" if on consumption page
	def consPress(self,appManager):
		if appManager != 'consumption':
			self.ids.consumption.state = 'down'
			return 'consumption'
		else: 
			self.ids.consumption.state = 'down'
			return appManager

	#make locker button "unogglable" if on locker page
	def lockPress(self,appManager):
		if appManager != 'locker':
			self.ids.locker.state = 'down'
			return 'locker'
		else: 
			self.ids.locker.state = 'down'
			return appManager

	#make about button "untogglable" if on locker page
	def aboutPress(self,appManager):
		if appManager != 'about':
			self.ids.about.state = 'down'
			return 'about'
		else: 
			self.ids.about.state = 'down'
			return appManager
	

class IdleScreen(ButtonBehavior,Screen):
	pass

class ConsumptionScreen(Screen):
	pass

class LockerScreen(Screen):
	def clickLogin(self):
		if lockerSys.currentUser == -1:
			lockerSys.login(0)
		else:
			lockerSys.login((lockerSys.currentUser+1)%6)
		self.parent
		self.manager.get_screen('lockerAccess').updateAll()
		self.manager.get_screen('lockerAccess').ids.labelUser.text = str(lockerSys.userTable.userList[lockerSys.userIndex].name)
		self.manager.current = 'lockerAccess'

	def updateAll(self):
		self.ids.available_locker.text = self.availableCount() 
		self.ids.unavailable_locker.text = self.unavailableCount()

	def availableCount(self):
		count = 0
		for element in lockerSys.lockerList:
			if element.state == 0: count += 1
		return str(count)
	def unavailableCount(self):
		count = 0
		for element in lockerSys.lockerList:
			if element.state == 1: count += 1
		return str(count)


class LockerAccessScreen(Screen):
	#lockerSys = LockerList()
	lockerIndex = -1

	def controlFlow(self, Input, output1, output2, output3):
		if Input == 0:
			return output1
		if Input == 1:
			return output2
		if Input == 2:
			return output3

	def backgroundState(self, lockerID):
		Input = lockerSys.lockerState(lockerID)
		output1 = [0,0,1,0.66] #available color
		output2 = [0.878,0.4,0.4,1.0] #locked color
		output3 = [0.576,0.768,.490,1.0] #owned color
		return self.controlFlow(Input, output1, output2, output3)

	def updateAll(self):
		#update all locker background depending on user
		tButtonArray = [] #tButton = toggleButton
		for i in range(10):
			tButtonArray.append("locker" + str(i+1))
		for i in range(10):
			tButton = self.ids[tButtonArray[i]]
			tButton.background_color = self.backgroundState(int(tButton.text)-1)

		#update all other info and buttons
		if self.lockerIndex != -1:
			#update labelName
			self.ids.labelName.text = str(lockerSys.lockerList[self.lockerIndex].id + 1)

			#update labelStatus text
			Input = lockerSys.lockerState(self.lockerIndex)
			output1 = 'Available'
			output2 = 'Locked'
			output3 = 'Owned'
			self.ids.labelStatus.text = self.controlFlow(Input, output1, output2, output3)

			#update labelStatus color
			output1 = [0,0,1,1]
			output2 = [1,0,0,1]
			output3 = [0,1,0,1]
			self.ids.labelStatus.color = self.controlFlow(Input, output1, output2, output3)

			#update labelTime
			self.ids.labelTime.text = lockerSys.lockerList[self.lockerIndex].lockTime

			#update action_button
			if lockerSys.userTable.userList[lockerSys.userIndex].lockerCount < lockerSys.limit:
				#update action_button text
				output1 = 'Unlock'
				output2 = 'Unavailable'
				output3 = 'Unlock'
				self.ids.action_button.text = self.controlFlow(Input, output1, output2, output3)

				#update action_button color
				output1 = [0,0.2890625,0.484375,1.0]
				output2 = [0.0,0.0,0.0,0.8]
				output3 = [0,0.2890625,0.484375,1.0]
				self.ids.action_button.background_color = self.controlFlow(Input, output1, output2, output3)
			else:
				#update action_button text
				output1 = 'Over Locker Limit'
				output2 = 'Unavailable'
				output3 = 'Unlock'
				self.ids.action_button.text = self.controlFlow(Input, output1, output2, output3)
				#update action_button color
				output1 = [0.0,0.0,0.0,0.8]
				output2 = [0.0,0.0,0.0,0.8]
				output3 = [0,0.2890625,0.484375,1.0]
				self.ids.action_button.background_color = self.controlFlow(Input, output1, output2, output3)
		else:
			#update labelName
			self.ids.labelName.text = 'N\A'
			#update labelStatus text
			self.ids.labelStatus.text = 'N\A'
			#update labelStatus color
			self.ids.labelStatus.color = [0.0,0.0,0.0,0.8]
			#update labelTime
			self.ids.labelTime.text = 'N\A'
			#update action_button
			self.ids.action_button.background_color = [0.0,0.0,0.0,0.8]
			self.ids.action_button.text = 'Choose a Locker'
			
	def lockerClick(self, toggleButton, lockerID):
		lockerSys.updateUserTable()
		self.lockerIndex = lockerID
		self.updateAll()
		#update labelName
		self.ids.labelName.text = str(lockerSys.lockerList[lockerID].id + 1)
		#update labelStatus text
		Input = lockerSys.lockerState(lockerID)
		output1 = 'Available'
		output2 = 'Locked'
		output3 = 'Owned'
		self.ids.labelStatus.text = self.controlFlow(Input, output1, output2, output3)
		#update labelStatus color
		output1 = [0,0,1,1]
		output2 = [1,0,0,1]
		output3 = [0,1,0,1]
		self.ids.labelStatus.color = self.controlFlow(Input, output1, output2, output3)
		#update labelTime
		self.ids.labelTime.text = lockerSys.lockerList[lockerID].lockTime
		#update action_button
		if lockerSys.userTable.userList[lockerSys.userIndex].lockerCount < lockerSys.limit:
			#update action_button text
			output1 = 'Unlock'
			output2 = 'Unavailable'
			output3 = 'Unlock'
			self.ids.action_button.text = self.controlFlow(Input, output1, output2, output3)
			#update action_button color
			output1 = [0,0.2890625,0.484375,1.0]
			output2 = [0.0,0.0,0.0,0.8]
			output3 = [0,0.2890625,0.484375,1.0]
			self.ids.action_button.background_color = self.controlFlow(Input, output1, output2, output3)
		else:
			#update action_button text
			output1 = 'Over locker limit!'
			output2 = 'Unavailable'
			output3 = 'Unlock'
			self.ids.action_button.text = self.controlFlow(Input, output1, output2, output3)
			#update action_button color
			output1 = [0.0,0.0,0.0,0.8]
			output2 = [0.0,0.0,0.0,0.8]
			output3 = [0,0.2890625,0.484375,1.0]
			self.ids.action_button.background_color = self.controlFlow(Input, output1, output2, output3)
		lockerSys.lockerList[lockerID].display()

	def actionClick(self):
		if self.lockerIndex != -1:
			lockerSys.chooseLocker(self.lockerIndex)

			#update locker info from 'locker' screen
			self.manager.get_screen('locker').updateAll()
			#update locker background
			self.ids['locker' + str(self.lockerIndex+1)].background_color = self.backgroundState(self.lockerIndex)
			#update labelStatus text
			Input = lockerSys.lockerState(self.lockerIndex)
			output1 = 'Available'
			output2 = 'Locked'
			output3 = 'Owned'
			self.ids.labelStatus.text = self.controlFlow(Input, output1, output2, output3)
			#update labelStatus color
			output1 = [0,0,1,1]
			output2 = [1,0,0,1]
			output3 = [0,1,0,1]
			self.ids.labelStatus.color = self.controlFlow(Input, output1, output2, output3)
			#update labelTime
			self.ids.labelTime.text = lockerSys.lockerList[self.lockerIndex].lockTime

	def logOut(self):
		lockerSys.logout()
		self.lockerIndex = -1
		self.updateAll()
		self.manager.current = 'locker'

class AboutScreen(Screen):
	pass
#--- End of Definitions ---#

#--- App Builder Class --- #
class SolarApp(App):
	def build(self):
		self.manager = ScreenManager() #Kivy Screen Manager object to handle screen transistion
		self.manager.add_widget(IdleScreen(name='idle'))
		self.manager.add_widget(LockerScreen(name='locker'))
		self.manager.add_widget(LockerAccessScreen(name='lockerAccess'))
		self.manager.add_widget(ConsumptionScreen(name='consumption'))
		self.manager.add_widget(AboutScreen(name='about'))
		#self.manager.current = 'lockerAccess'
		self.manager.current = 'consumption'

		layout = FloatLayout(size=(800,480)) #float layout to handle manager and navbar
		layout.add_widget(self.manager)
		layout.add_widget(NavBar(id='my_root',name='root'))
		Clock.schedule_interval(self.displayTime, 1)
		Clock.schedule_interval(self.lockerDurationCount, 60)
		return layout

	#---clock function---#
	#show current time in format 24-hour:min:sec
	def displayTime(self, dt):
		AM_PM = ''
		hour = strftime("%H", localtime())
		if int(hour) < 12 or int(hour) == 24: 
			AM_PM = 'AM'
			hour = str(int(hour)%12)
		else:
			AM_PM = 'PM'
			if hour != '12': hour = str(int(hour)%12)
		minute = strftime("%M", localtime())
		TimeStr = hour + ":" + minute + " " + AM_PM
		self.manager.get_screen('locker').ids.clockTime.text = TimeStr
		self.manager.get_screen('lockerAccess').ids.clockTime.text = TimeStr
		self.manager.get_screen('consumption').ids.clockTime.text = TimeStr
		self.manager.get_screen('about').ids.clockTime.text = TimeStr

	def lockerDurationCount(self, dt):
		for element in lockerSys.lockerList:
			if element.state == 1: 
				element.lockDuration += 60 #add in 60 second everytime this is called
				lockerSys.writeData(lockerSys.dataFile)
				if element.lockDuration >= 3*60*60: #3hours duration
					print("too long")
			#if element.lockDuration%60 == 0: #record to file every minute
#--- End App Builder ---#

#--- Start the App --- #
if __name__ == '__main__':
	SolarApp().run()