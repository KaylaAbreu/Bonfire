from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen


class SignupScreen(MDScreen):
    def on_login(self):
        self.manager.current = 'LoginScreen'

    def send_data(self, username, password, email):
        app = MDApp.get_running_app()

        # Check if any of the input fields are empty
        if not username.text or not password.text or not email.text:
            self.ids.error_label.text = "Please fill in all the fields."
        else:
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

                self.manager.current = 'LoginScreen'

    def check_username_exists(self, username):
        app = MDApp.get_running_app()

        # Query the database to check if the username already exists
        query = "SELECT username FROM login WHERE username = %s"
        app.cursor.execute(query, (username,))
        result = app.cursor.fetchone()

        return result is not None

