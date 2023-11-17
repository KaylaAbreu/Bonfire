from kivymd.uix.screen import MDScreen


class SuccessScreen(MDScreen):
    def on_logout(self):
        self.manager.current = 'LoginScreen'
    def callback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "MenuScreen"
