from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen


class MtCommentScreen(MDScreen):
    post_id = None
    def mt_comment_submit(self):
        app = MDApp.get_running_app()

        # Gets username and user_ID from LoginScreen
        username = self.manager.get_screen('LoginScreen').current_user
        user_ID = self.manager.get_screen('LoginScreen').user_ID

        # Check length of post
        if len(self.ids.post_input.text) == 0:
            dialog = MDDialog(text="Please add a comment")
            dialog.open()
            self.manager.current = 'MtCommentScreen'

        elif len(self.ids.post_input.text) < 255:
            # Add record to database
            sql_command = "INSERT INTO comments (post_ID, user_ID, username, content, location) VALUES (%s, %s, %s, %s, 'mountain')"
            values = (self.post_id, user_ID, username, self.ids.post_input.text,)

            # Execute command
            app.cursor.execute(sql_command, values)

            # Clear input box
            self.ids.post_input.text = ''

            # Commit changes to database
            app.database.commit()

            self.manager.current = 'ViewMtPostScreen'
        else:
            # Displays error message
            dialog = MDDialog(text="Comments must be under 255 characters")
            dialog.open()
            self.manager.current = 'MtCommentScreen'

    def callback(self):
        # Clears input from leftover text and switches to home page
        comment = self.manager.get_screen('MtCommentScreen')
        comment.ids.post_input.text = ""
        self.manager.transition.direction = "right"
        self.manager.current = "MenuScreen"

    def on_logout(self):
        # Switches to LoginScreen and erases any leftover content for username, password, and error text
        login_screen = self.manager.get_screen('LoginScreen')
        login_screen.ids.username.text = ""
        login_screen.ids.password.text = ""
        login_screen.ids.error_label.text = ""
        self.manager.current = 'LoginScreen'