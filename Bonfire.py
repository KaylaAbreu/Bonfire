from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.text import LabelBase
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
import mysql.connector

Window.size = (350,580)

class LoginScreen(Screen):
    def on_signup(self):
        # Switch to the SignupScreen
        self.manager.current = 'signup'
    def on_forgotPassword(self):
        # Switch to the ForgotPasswordScreen
        self.manager.current = 'forgotPassword'

    def on_login(self, username, password):
        username = self.ids.username.text
        password = self.ids.password.text

        if self.check_credentials(username, password):
            # Successful login, navigate to the next screen
            self.manager.current = 'success'
        else:
            # Invalid login, display an error message
            self.ids.error_label.text = "Invalid username or password"

    def check_credentials(self, username, password):
        app = MDApp.get_running_app()
        # Query the database to check if the credentials are valid
        query = "select * from login where username = %s and password = %s"
        values = (username, password)
        app.cursor.execute(query, values)
        result = app.cursor.fetchone()
        return result is not None
        
class SuccessScreen(Screen):
    def on_logout(self):
        # Switch back to the login screen
        self.manager.current = 'login'

class SignupScreen(Screen):
    def on_login(self):
       
        self.manager.current = 'login'

class ForgotPasswordScreen(Screen):
    def on_login(self):
       
        self.manager.current = 'login'

# Create a ScreenManager to manage the screens
class Bonfire(MDApp):

    database= mysql.connector.Connect(host="localhost",user="root",password ="admin321", database="bonfire")
    cursor = database.cursor()
    cursor.execute("select * from login")
    for i in cursor.fetchall():
        print(i[0],i[1])

    def send_data(self,username,password):
        self.cursor.execute(f"insert into login (username,password) values('{username.text}','{password.text}')")
        self.database.commit()
        for i in self.cursor.fetchall():
            print(i[0],i[1])
        
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string("""

ScreenManager:
    LoginScreen:
    SignupScreen:
    ForgotPasswordScreen:
    SuccessScreen:

<LoginScreen>:
    name: 'login'
    MDFloatLayout:
        md_bg_color: 0.996, 0.365, 0.149, 1  # Orange color in RGBA format
        Image:
            source: "logo.png"
            pos_hint: {"center_x": .5, "center_y": .70}
            size_hint: .5, .5

        MDFloatLayout:
            size_hint: .9 , .07
            pos_hint: {"center_x": .5, "center_y": .50}
            canvas:
                Color:
                    rgb: 250/255, 250/255, 250/255, 1
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [4]
            canvas.before:
                Color:
                    rgb: 217/255, 217/255, 217/255, 1
                Line:
                    width:1.1
                    rounded_rectangle: self.x, self.y, self.width, self.height, 4, 4, 4, 4,100
            TextInput:
                id:username
                hint_text: "Username"
                size_hint: 1, None
                pos_hint: {"center_x": .5, "center_y": .5}
                height: self.minimum_height
                background_color: 1, 1, 1, 0
                font_size: "14sp"
                hint_text_color: 170/255, 170/255, 170/255, 1
                padding: 13
                cursor_color: 0, 0, 0, 1

        MDFloatLayout:
            size_hint: .9 , .07
            pos_hint: {"center_x": .5, "center_y": .41}
            canvas:
                Color:
                    rgb: 250/255, 250/255, 250/255, 1
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [4]
            canvas.before:
                Color:
                    rgb: 217/255, 217/255, 217/255, 1
                Line:
                    width:1.1
                    rounded_rectangle: self.x, self.y, self.width, self.height, 4, 4, 4, 4,100
            TextInput:
                id:password
                hint_text: "Password"
                size_hint: 1, None
                pos_hint: {"center_x": .5, "center_y": .5}
                height: self.minimum_height
                background_color: 1, 1, 1, 0
                font_size: "14sp"
                password: True
                hint_text_color: 170/255, 170/255, 170/255, 1
                padding: 13
                cursor_color: 0, 0, 0, 1

            Button:
                text: "Login"
                size_hint: 1, 0.9
                pos_hint: {"center_x": 0.5, "center_y": -0.70}
                background_color: 128/255, 128/255, 128/255, 1
                font_size: "15sp"
                on_release: root.on_login(username,password)
                canvas.before:
                    Color:
                        rgb: 154/255, 203/255, 247/255, 1
                    RoundedRectangle:
                        size: self.size
                        pos: self.pos 
                        radius: [4]

            MDTextButton:
                text: "Sign Up"
                pos_hint:{"center_x":0.5, "center_y": -4.0}
                font_size: "13sp"
                on_release: root.on_signup()

            MDTextButton:
                text: "Forgot Password"
                pos_hint:{"center_x":0.5, "center_y": -4.6}
                font_size: "13sp"
                on_release: root.on_forgotPassword()
                
        MDLabel:
            id: error_label
            text: " "
            size_hint: None, None
            size: "250sp" , "30sp" # Adjust the size as needed
            pos_hint: {"center_x": 0.5, "center_y": 0.2}
            text_size: self.size
            halign: "center"
            valign: "middle"
            markup: True
            font_size: "13sp"

                
<SuccessScreen>:
    name: 'success'
    MDFloatLayout:
        md_bg_color: 0.996, 0.365, 0.149, 1  # Orange color in RGBA format
        Image:
            source: "logo.png"
            pos_hint: {"center_x": .5, "center_y": .70}
            size_hint: .5, .5

        Button:
            text: "Logout"
            size_hint: 1, 0.9
            pos_hint: {"center_x": 0.5, "center_y": -0.70}
            background_color: 128/255, 128/255, 128/255, 1
            font_size: "15sp"
            on_release: root.on_logout()
            canvas.before:
                Color:
                    rgb: 154/255, 203/255, 247/255, 1
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [4]
    
<SignupScreen>:
    name: 'signup'
    MDFloatLayout:
        md_bg_color: 0.996, 0.365, 0.149, 1  # Orange color in RGBA format
        Image:
            source: "logo.png"
            pos_hint: {"center_x": .5, "center_y": .70}
            size_hint: .5, .5

        MDFloatLayout:
            size_hint: .9 , .07
            pos_hint: {"center_x": .5, "center_y": .50}
            canvas:
                Color:
                    rgb: 250/255, 250/255, 250/255, 1
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [4]
            canvas.before:
                Color:
                    rgb: 217/255, 217/255, 217/255, 1
                Line:
                    width:1.1
                    rounded_rectangle: self.x, self.y, self.width, self.height, 4, 4, 4, 4,100
            TextInput:
                id:username
                hint_text: "New Username"
                size_hint: 1, None
                pos_hint: {"center_x": .5, "center_y": .5}
                height: self.minimum_height
                background_color: 1, 1, 1, 0
                font_size: "14sp"
                hint_text_color: 170/255, 170/255, 170/255, 1
                padding: 13
                cursor_color: 0, 0, 0, 1

        MDFloatLayout:
            size_hint: .9 , .07
            pos_hint: {"center_x": .5, "center_y": .41}
            canvas:
                Color:
                    rgb: 250/255, 250/255, 250/255, 1
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [4]
            canvas.before:
                Color:
                    rgb: 217/255, 217/255, 217/255, 1
                Line:
                    width:1.1
                    rounded_rectangle: self.x, self.y, self.width, self.height, 4, 4, 4, 4,100
            TextInput:
                id:password
                hint_text: "New Password"
                size_hint: 1, None
                pos_hint: {"center_x": .5, "center_y": .5}
                height: self.minimum_height
                background_color: 1, 1, 1, 0
                font_size: "14sp"
                password: True
                hint_text_color: 170/255, 170/255, 170/255, 1
                padding: 13
                cursor_color: 0, 0, 0, 1

            Button:
                text: "Create Account"
                size_hint: 1, 0.9
                pos_hint: {"center_x": 0.5, "center_y": -0.70}
                background_color: 128/255, 128/255, 128/255, 1
                on_release: app.send_data(username,password)
                font_size: "15sp"
                canvas.before:
                    Color:
                        rgb: 154/255, 203/255, 247/255, 1
                    RoundedRectangle:
                        size: self.size
                        pos: self.pos 
                        radius: [4]
                    
            MDTextButton:
                text: "Back To Login"
                pos_hint:{"center_x":0.5, "center_y": -3.5}
                font_size: "13sp"
                on_release: root.on_login()

<ForgotPasswordScreen>:
    name:'forgotPassword'
    MDFloatLayout:
        md_bg_color: 0.996, 0.365, 0.149, 1  # Orange color in RGBA format
        Image:
            source: "logo.png"
            pos_hint: {"center_x": .5, "center_y": .70}
            size_hint: .5, .5

        MDFloatLayout:
            size_hint: .9 , .07
            pos_hint: {"center_x": .5, "center_y": .50}
            canvas:
                Color:
                    rgb: 250/255, 250/255, 250/255, 1
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [4]
            canvas.before:
                Color:
                    rgb: 217/255, 217/255, 217/255, 1
                Line:
                    width:1.1
                    rounded_rectangle: self.x, self.y, self.width, self.height, 4, 4, 4, 4,100
            TextInput:
                hint_text: "Username"
                size_hint: 1, None
                pos_hint: {"center_x": .5, "center_y": .5}
                height: self.minimum_height
                background_color: 1, 1, 1, 0
                font_size: "14sp"
                hint_text_color: 170/255, 170/255, 170/255, 1
                padding: 13
                cursor_color: 0, 0, 0, 1

        MDFloatLayout:
            size_hint: .9 , .07
            pos_hint: {"center_x": .5, "center_y": .41}
            canvas:
                Color:
                    rgb: 250/255, 250/255, 250/255, 1
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [4]
            canvas.before:
                Color:
                    rgb: 217/255, 217/255, 217/255, 1
                Line:
                    width:1.1
                    rounded_rectangle: self.x, self.y, self.width, self.height, 4, 4, 4, 4,100
            TextInput:
                hint_text: "Email"
                size_hint: 1, None
                pos_hint: {"center_x": .5, "center_y": .5}
                height: self.minimum_height
                background_color: 1, 1, 1, 0
                font_size: "14sp"
                password: True
                hint_text_color: 170/255, 170/255, 170/255, 1
                padding: 13
                cursor_color: 0, 0, 0, 1

            Button:
                text: "Submit"
                size_hint: 1, 0.9
                pos_hint: {"center_x": 0.5, "center_y": -0.70}
                background_color: 128/255, 128/255, 128/255, 1
                font_size: "15sp"
                canvas.before:
                    Color:
                        rgb: 154/255, 203/255, 247/255, 1
                    RoundedRectangle:
                        size: self.size
                        pos: self.pos 
                        radius: [4]
                        
            MDTextButton:
                text: "Back To Login"
                pos_hint:{"center_x":0.5, "center_y": -3.5}
                font_size: "13sp"
                on_release: root.on_login()

                
"""
)

    
    
if __name__ == '__main__':
    Bonfire().run()
                    
