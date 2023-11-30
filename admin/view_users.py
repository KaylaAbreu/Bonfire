from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton
from kivymd.uix.dialog import MDDialog


class ConfirmDeleteUserDialog(BoxLayout):
    pass


class ViewUsersScreen(Screen):

    def display_users(self, users):
        # Clears user lists to prevent repeats
        user_list = self.ids.user_list
        user_list.clear_widgets()

        # Displays each username along with delete button
        for index, user in enumerate(users, start=1):
            user_label = Label(
                text=f"{index}. {user}",
                font_size='16sp',
                size_hint=(None, None),
                size=('150dp', '30dp'),
                color=(0, 0, 0, 1)
            )
            delete_button = MDIconButton(
                icon="delete",
                size_hint=(None, None),
                size=('50dp', '40dp'),
                on_release=lambda instance, user=user: self.show_confirmation_dialog(user)
            )
            # Adds user_label and delete_button to user_list widget
            user_list.add_widget(user_label)
            user_list.add_widget(delete_button)

    def show_confirmation_dialog(self, user):
        # Deletes user if admin selects 'yes' in dialog box
        def yes(instance):
            # Accesses running Kivy app
            app = MDApp.get_running_app()

            # SQL DELETE query to remove user from login table
            query = "DELETE FROM login WHERE username = %s"
            app.cursor.execute(query, (user,))
            app.database.commit()
            self.dialog.dismiss()

            # Retrieve the updated user list directly from the database
            app.cursor.execute("SELECT username FROM login")
            updated_users = [row[0] for row in app.cursor.fetchall()]

            # Display the updated user list on the screen
            self.display_users(updated_users)

        # If cancel button is pressed in dialog box, dialog box will close with no change
        def cancel(instance):
            self.dialog.dismiss()

        # Creates dialog box to confirm deletion of users
        self.dialog = MDDialog(
            text='Are you sure you want to delete this user?',
            type="custom",
            buttons=[
                MDRectangleFlatButton(
                    text="Yes",
                    on_release=yes),
                MDRectangleFlatButton(
                    text="Cancel",
                    on_release=cancel)
            ])
        self.dialog.open()

    def on_back(self):
        # Returns to AdminScreen
        self.manager.transition.direction = "left"
        self.manager.current = "AdminScreen"

    def on_logout(self):
        # Switches to LoginScreen and erases any leftover content for username, password, and error text
        login_screen = self.manager.get_screen('LoginScreen')
        login_screen.ids.username.text = ""
        login_screen.ids.password.text = ""
        login_screen.ids.error_label.text = ""
        self.manager.current = 'LoginScreen'
