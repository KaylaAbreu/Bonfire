from kivymd.uix.screen import MDScreen


class AdminDashScreen(MDScreen):
    def callback (self):
        # Switches back to AdminScreen
        self.manager.transition.direction = "right"
        self.manager.current = "AdminScreen"

    def on_logout(self):
        # Switches to LoginScreen and erases any leftover content for username, password, and error text
        login_screen = self.manager.get_screen('LoginScreen')
        login_screen.ids.username.text = ""
        login_screen.ids.password.text = ""
        login_screen.ids.error_label.text = ""
        self.manager.current = 'LoginScreen'