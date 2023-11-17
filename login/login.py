from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

class LoginScreen(MDScreen):

    def on_signup(self):
        # Switch to the SignupScreen
        self.manager.current = 'SignupScreen'

    def on_forgotPassword(self):

        self.manager.current = 'ForgotPasswordScreen'

    def on_login(self, username, password):
        username = self.ids.username.text
        password = self.ids.password.text

        if self.check_credentials(username, password):
            if username == "admin":
                self.manager.current = 'AdminScreen'
            else:
                self.manager.current = 'MenuScreen'
        else:

            self.ids.error_label.text = "Invalid username or password"

    def check_credentials(self, username, password):
        app = MDApp.get_running_app()
        # Query the database to check if the credentials are valid
        query = "select * from login where username = %s and password = %s"
        values = (username, password)
        app.cursor.execute(query, values)
        result = app.cursor.fetchone()
        if result:
            self.user_ID = result[0]
            self.current_user = username
        return result is not None