from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen

from alerts.alerts import Alerts


class WelcomePtScreen(MDScreen):
    # Get alert headline from Alerts() and display in pop up
    def on_enter(self):
        alert_headline = Alerts()
        alert_headline.alerts()
        self.dialog = MDDialog(
            title="Alert for the Piedmont Region",
            text=alert_headline.headline2,
            buttons=[MDRectangleFlatButton(text="Close", on_release=self.close)]
        )
        self.dialog.open()

    def close(self, *args):
        self.dialog.dismiss()

    def callback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "MenuScreen"

    def on_logout(self):
        # Switches to LoginScreen and erases any leftover content for username, password, and error text
        login_screen = self.manager.get_screen('LoginScreen')
        login_screen.ids.username.text = ""
        login_screen.ids.password.text = ""
        login_screen.ids.error_label.text = ""
        self.manager.current = 'LoginScreen'