from kivymd.uix.screen import MDScreen


class AdminDashScreen(MDScreen):
    def callback (self):
        self.manager.transition.direction = "right"
        self.manager.current = "AdminScreen"