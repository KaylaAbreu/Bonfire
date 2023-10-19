from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.text import LabelBase
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
import mysql.connector
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets
import string

Window.size = (350, 580)


class LoginScreen(Screen):
    def on_signup(self):
        # Switch to the SignupScreen
        self.manager.current = 'signup'

    def on_forgotPassword(self):

        self.manager.current = 'forgotPassword'

    def on_login(self, username, password):
        username = self.ids.username.text
        password = self.ids.password.text

        if self.check_credentials(username, password):

            self.manager.current = 'success'
        else:

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

        self.manager.current = 'login'


class SignupScreen(Screen):
    def on_login(self):
        self.manager.current = 'login'

    def send_data(self, username, password, email):
        app = MDApp.get_running_app()

        # Check if the username already exists in the database
        username_exists = self.check_username_exists(username.text)

        if username_exists:

            self.ids.error_label.text = "Username already taken."
        else:

            self.ids.error_label.text = ""

            # Insert the new user into the database
            app.cursor.execute(
                f"INSERT INTO login (username, password, email) VALUES ('{username.text}', '{password.text}', '{email.text}')")
            app.database.commit()
            print(f"User {username.text} registered")

            self.manager.current = 'login'


    def check_username_exists(self, username):
        app = MDApp.get_running_app()

        # Query the database to check if the username already exists
        query = "SELECT username FROM login WHERE username = %s"
        app.cursor.execute(query, (username,))
        result = app.cursor.fetchone()

        return result is not None



class ForgotPasswordScreen(Screen):
    def on_login(self):

        self.manager.current = 'login'

    def store_reset_code(self, username, reset_code):
            app = MDApp.get_running_app()
            try:

                query = "SELECT * FROM login WHERE username = %s"
                app.cursor.execute(query, (username,))
                result = app.cursor.fetchone()

                if result:

                    update_query = "UPDATE login SET reset_code = %s WHERE username = %s"
                    app.cursor.execute(update_query, (reset_code, username))
                    app.database.commit()
                    self.ids.message_label.text = "Reset code updated successfully."
                else:

                    self.ids.error_label.text = "User not found."
            except Exception as e:
                print("Error updating reset code:", str(e))

    def send_reset_code(self, username):
        # Retrieve the user's email address from the database based on the username
        username = self.ids.username.text

        user_email = self.get_user_email(username)
        if user_email:
            # Generate a reset code (you can use a random code generator)
            reset_code = self.generate_random_code(5)

            # Send and store the reset code via email

            self.store_reset_code(username, reset_code)

            self.send_reset_email(user_email, reset_code)

            self.manager.current = 'changePassword'

        else:

            self.ids.error_label.text = "User not found."

    def generate_random_code(self, length):
        characters = string.digits
        code = ''.join(secrets.choice(characters) for _ in range(length))
        return code

    def get_user_email(self, username):
        app = MDApp.get_running_app()
        query = "SELECT email FROM login WHERE username = %s"
        app.cursor.execute(query, (username,))
        result = app.cursor.fetchone()
        if result:
            return result[0]
        return None

    def send_reset_email(self, recipient_email, reset_code):
        # Sender's and recipient's email addresses
        sender_email = "editorforbonfire01@gmail.com"
        sender_password = "uafj tgqa acjz odil"
        subject = "Bonfire Password Reset Code"
        message = f"Your password reset code is: {reset_code}"

        # Create an email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # Connect to the SMTP server and send the email
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            server.quit()
        except Exception as e:
            print("Email could not be sent. Error:", str(e))


class ChangePasswordScreen(Screen):
    def change_password(self, username, reset_code, new_password):
        # Verify the reset code
        if self.verify_reset_code(username, reset_code):
            # Change the password
            self.change_user_password(username, new_password)
            self.manager.current = 'login'
        else:
            self.ids.error_label.text = "Invalid reset code."

    def verify_reset_code(self, username, reset_code):
        # Check if the provided reset code matches the one in the database
        app = MDApp.get_running_app()
        query = "SELECT reset_code FROM login WHERE username = %s"
        app.cursor.execute(query, (username,))
        result = app.cursor.fetchone()

        if result and result[0] == reset_code:
            return True
        return False

    def change_user_password(self, username, new_password):
        # Update the user's password
        app = MDApp.get_running_app()
        query = "UPDATE login SET password = %s WHERE username = %s"
        values = (new_password, username)
        app.cursor.execute(query, values)
        app.database.commit()
        # Clear the reset code after changing the password
        app.cursor.execute("UPDATE login SET reset_code = NULL WHERE username = %s", (username,))
        app.database.commit()

class Bonfire(MDApp):
    database = mysql.connector.Connect(host="localhost", user="root", password="admin321", database="bonfire")
    cursor = database.cursor()
    cursor.execute("select * from login")
    for i in cursor.fetchall():
        print(i[0], i[1])


    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string("""

ScreenManager:
    LoginScreen:
    SignupScreen:
    ForgotPasswordScreen:
    SuccessScreen:
    ChangePasswordScreen:

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
            pos_hint: {"center_x": 0.5, "center_y": 0.4}
            text_size: self.size
            halign: "center"
            valign: "middle"
            markup: True
            font_size: "13sp"
            theme_text_color: "Error"
            

                
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
                
        MDFloatLayout:
            size_hint: .9 , .07
            pos_hint: {"center_x": .5, "center_y": .315}
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
                id:email
                hint_text: "Email"
                size_hint: 1, None
                pos_hint: {"center_x": .5, "center_y": .5}
                height: self.minimum_height
                background_color: 1, 1, 1, 0
                font_size: "14sp"
                hint_text_color: 170/255, 170/255, 170/255, 1
                padding: 13
                cursor_color: 0, 0, 0, 1
                
            Button:
                text: "Create Account"
                size_hint: 1, 0.9
                pos_hint: {"center_x": 0.5, "center_y": -0.70}
                background_color: 128/255, 128/255, 128/255, 1
                on_release: root.send_data(username,password,email)
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
                
            MDLabel:
                id: error_label
                text: " "
                size_hint: None, None
                size: "250sp" , "30sp" # Adjust the size as needed
                pos_hint: {"center_x": 0.5, "center_y": 3}
                text_size: self.size
                halign: "center"
                valign: "middle"
                markup: True
                font_size: "13sp"
                theme_text_color: "Error"
                
            

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

        
            Button:
                text: "Send Code to Email"
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
                on_release: root.send_reset_code(self)
                        
            MDTextButton:
                text: "Back To Login"
                pos_hint:{"center_x":0.5, "center_y": -3.5}
                font_size: "13sp"
                on_release: root.on_login()
                
            
            MDLabel:
                id: error_label
                text: ""
                size_hint: None, None
                size: "250sp", "30sp"
                pos_hint: {"center_x": 0.5, "center_y": 0.2}
                text_size: self.size
                halign: "center"
                valign: "middle"
                markup: True
                font_size: "13sp"
                theme_text_color: "Error"
                
<ChangePasswordScreen>:
    name:'changePassword'
    MDFloatLayout:
        md_bg_color: 0.996, 0.365, 0.149, 1  # Orange color in RGBA format
        Image:
            source: "logo.png"
            pos_hint: {"center_x": .5, "center_y": .70}
            size_hint: .5, .5
            
        MDFloatLayout:
            size_hint: .9 , .07
            pos_hint: {"center_x": .5, "center_y": .5}
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
                id: username
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
                id: reset_code
                hint_text: "Enter Code"
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
            pos_hint: {"center_x": .5, "center_y": .315}
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
                id: new_password
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
                on_release: root.change_password(username.text, reset_code.text, new_password.text)
                                
            MDLabel:
                id: error_label
                text: " "
                size_hint: None, None
                size: "250sp" , "30sp" # Adjust the size as needed
                pos_hint: {"center_x": 0.5, "center_y": 2}
                text_size: self.size
                halign: "center"
                valign: "middle"
                markup: True
                font_size: "13sp"
                theme_text_color: "Error"
            

                
"""
)


if __name__ == '__main__':
    Bonfire().run()
