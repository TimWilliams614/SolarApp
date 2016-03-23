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

class AboutScreen(Screen):
    pass
#--- End of Definitions ---#


#--- App Builder Class --- #

class SolarApp(App):
    
    def build(self):
        self.manager = ScreenManager() #Kivy Screen Manager object to handle screen transistion
    	self.manager.add_widget(IdleScreen(name='idle'))
    	self.manager.add_widget(LockerScreen(name='locker'))
    	self.manager.add_widget(ConsumptionScreen(name='consumption'))
    	self.manager.add_widget(AboutScreen(name='about'))
        
        #float layout to handle manager and navbar
        layout = FloatLayout(size=(800,480))
        layout.add_widget(self.manager)
        layout.add_widget(NavBar(id='my_root',name='root'))

        return layout
#--- End App Builder ---#


#--- Start the App --- #
if __name__ == '__main__':
    SolarApp().run()

