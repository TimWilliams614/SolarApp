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

#--- Widget/Screen Definitions Passed from KV file ---#
class NavBar(Screen):
	pass

class IdleScreen(ButtonBehavior,Screen):
    pass

class ConsumptionScreen(Screen):
    pass

class LockerScreen(Screen):
    pass

class LockerAccessScreen(Screen):
    pass

class AboutScreen(Screen):
    pass
#--- End of Definitions ---#
'''
def buttonStateCheck(myButton):
    test = ToggleButtonBehavior.get_widgets(myButton.group)
    for widget in test:
        print(widget.state)
    del test
'''
#--- App Builder Class --- #
class SolarApp(App):

    
    def build(self):
        idleScreen = IdleScreen(name='idle')
        lockerScreen = LockerScreen(name='locker')
        lockerAccessScreen = LockerAccessScreen(name='lockerAccess')
        consumptionScreen = ConsumptionScreen(name='consumption')
        aboutScreen = AboutScreen(name='about')
        navBar = NavBar(id='my_root',name='root')

        self.manager = ScreenManager() #Kivy Screen Manager object to handle screen transistion
        self.manager.add_widget(idleScreen)
    	self.manager.add_widget(lockerScreen)
        self.manager.add_widget(lockerAccessScreen)
    	self.manager.add_widget(consumptionScreen)
    	self.manager.add_widget(aboutScreen)
        #self.manager.current = 'lockerAccess'
        self.manager.current = 'consumption'
       
        layout = FloatLayout(size=(800,480)) #float layout to handle manager and navbar
        layout.add_widget(self.manager)
        layout.add_widget(navBar)

        '''
        lButton =  navBar.ids['consButton']
        print(lButton.text)
        test = ToggleButtonBehavior.get_widgets('mainmenu')
        for widget in test:
            print(widget.state)
        print("test")'''
        return layout
#--- End App Builder ---#

#--- Start the App --- #
if __name__ == '__main__':
    SolarApp().run()
    
