from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView


class ConfirmDeleteUserDialog(BoxLayout):
    pass

class ViewUsersScreen(Screen):

    def display_users(self, users):
        user_list = self.ids.user_list
        user_list.clear_widgets()

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

            user_list.add_widget(user_label)
            user_list.add_widget(delete_button)

    def show_confirmation_dialog(self, user):
        def yes(instance):
            app = MDApp.get_running_app()

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
        self.manager.transition.direction = "left"
        self.manager.current = "AdminScreen"
