from kivymd.uix.screen import MDScreen


class SuccessScreen(MDScreen):
    def on_logout(self):
        self.manager.current = 'LoginScreen'
    def callback(self):
        username = self.manager.get_screen('LoginScreen').current_user
        if username == 'admin':
            self.manager.transition.direction = "right"
            self.manager.current = "AdminScreen"
        else:
            self.manager.transition.direction = "right"
            self.manager.current = "MenuScreen"

    def on_logout(self):
        login_screen = self.manager.get_screen('LoginScreen')
        login_screen.ids.username.text = ""
        login_screen.ids.password.text = ""
        login_screen.ids.error_label.text = ""
        self.manager.current = 'LoginScreen'