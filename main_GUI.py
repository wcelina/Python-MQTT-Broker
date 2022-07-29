#VSCode interpreter path at home --> C:\Users\Manatee\AppData\Local\Programs\Python\Python310
#at work --> ~\AppData\Local\Microsoft\WindowsApps\Python3.10.exe

import kivy
kivy.require('2.1.0')
from kivy.app import App 
from kivy.uix.widget import Widget 
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.config import Config 

Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '175')
Builder.load_file('my.kv')

class API_Login(Widget):    #API key login
    apikey = ObjectProperty(None)

    def button_func(self): 
        if apikey is None:
            apikey = self.apikey.text
        print(f"Hello {apikey}")
        
        #
        #return apikey

#each window should get their own kv file
#main window will have multiple screens - terminal, tabs, device information, etc.

class WindowManager(ScreenManager):
    pass

class MyApp(App):
    def build(self):
        return API_Login()

if __name__ == '__main__':
    MyApp().run()


#next: select target device
