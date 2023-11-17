from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen


class AddPtPostScreen(MDScreen):
    def pt_submit(self):
        app = MDApp.get_running_app()

        username = self.manager.get_screen('LoginScreen').current_user
        user_ID = self.manager.get_screen('LoginScreen').user_ID

        # Check length of post
        if len(self.ids.post_input.text) == 0:
            dialog = MDDialog(text="Please add a story")
            dialog.open()
            self.manager.current = 'AddPtPostScreen'

        elif len(self.ids.post_input.text) < 255:
            # Add record to database
            sql_command = "INSERT INTO posts (user_ID, username, content, location) VALUES (%s, %s, %s, 'piedmont')"
            values = (user_ID, username, self.ids.post_input.text,)

            # Execute command
            app.cursor.execute(sql_command, values)

            # Clear input box
            self.ids.post_input.text = ''

            # Commit changes to database
            app.database.commit()

            self.manager.current = 'ViewPtPostScreen'
        else:
            dialog = MDDialog(text="Posts must be under 255 characters")
            dialog.open()
            self.manager.current = 'AddPtPostScreen'

    def callback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "MenuScreen"



