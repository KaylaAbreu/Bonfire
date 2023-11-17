from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen


class ChangePasswordScreen(MDScreen):
    def change_password(self, username, reset_code, new_password):
        # Verify the reset code
        if self.verify_reset_code(username, reset_code):
            # Change the password
            self.change_user_password(username, new_password)
            self.manager.current = 'LoginScreen'
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