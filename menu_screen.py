from kivymd.uix.screen import MDScreen


class MenuScreen(MDScreen):
    def on_logout(self):
        # Switches to LoginScreen and erases any leftover content for username, password, and error text
        clear_login = self.manager.get_screen('LoginScreen')
        clear_login.ids.username.text = ""
        clear_login.ids.password.text = ""
        self.manager.current = 'LoginScreen'