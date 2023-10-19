from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivymd.uix.list import TwoLineListItem, ThreeLineAvatarIconListItem, IconRightWidget, IconLeftWidget
import mysql.connector

Window.size = (350, 580)


class MyScreenManager(ScreenManager):
    pass


class LoginScreen(Screen):
    def send_data(self, username, password):
        self.cursor.execute(f"insert into login values('{username.text}','{password.text}')")
        self.database.commit()
        for i in self.cursor.fetchall():
            print(i[0], i[1])

    def on_login(self, username, password):
        username = self.ids.username.text
        password = self.ids.password.text

        if self.check_credentials(username, password):
            # Successful login, navigate to the next screen
            self.manager.current = 'SuccessScreen'
        else:
            # Invalid login, display an error message
            self.ids.error_label.text = "Invalid username or password"

    def check_credentials(self, username, password):
        app = MDApp.get_running_app()
        query = "select * from login where username = %s and password = %s"
        values = (username, password)
        app.cursor.execute(query, values)
        result = app.cursor.fetchone()
        if result:
            self.user_ID = result[0]
            self.current_user = username
        return result is not None


class SignupScreen(Screen):
    # def on_enter(self):
    pass


class ForgotPasswordScreen(Screen):
    # def on_enter(self):
    pass


class SuccessScreen(Screen):
    pass


class ViewMtPostScreen(Screen):
    def on_enter(self):
        db_connect = mysql.connector.connect(
            user="root",
            password="",
            host="localhost",
            database="bonfire"
        )
        # Create cursor
        c = db_connect.cursor()

        # Get stories from database
        c.execute("SELECT * FROM posts WHERE location = 'mountain'")
        stories = c.fetchall()

        # Prevent repeats
        self.ids.mt_story_container.clear_widgets()

        # Populate MDList with username and post content
        for i in stories:
            self.ids.mt_story_container.add_widget(TwoLineListItem(text=f'{i[2]}', secondary_text=f'{i[3]}'))

        db_connect.close()

    def callback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "SuccessScreen"


class ViewPtPostScreen(Screen):
    def on_enter(self):
        db_connect = mysql.connector.connect(
            user="root",
            password="",
            host="localhost",
            database="bonfire"
        )
        # Create cursor
        c = db_connect.cursor()

        # Get stories from database
        c.execute("SELECT * FROM posts WHERE location = 'piedmont'")
        stories = c.fetchall()

        # Prevent repeats
        self.ids.pt_story_container.clear_widgets()

        # Populate MDList with username and post content
        for i in stories:
            self.ids.pt_story_container.add_widget(TwoLineListItem(text=f'{i[2]}', secondary_text=f'{i[3]}'))

        db_connect.close()

    def callback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "SuccessScreen"


class ViewCtPostScreen(Screen):
    def on_enter(self):
        db_connect = mysql.connector.connect(
            user="root",
            password="",
            host="localhost",
            database="bonfire"
        )
        # Create cursor
        c = db_connect.cursor()

        # Get stories from database
        c.execute("SELECT * FROM posts WHERE location = 'coast'")
        stories = c.fetchall()

        # Prevent repeats
        self.ids.ct_story_container.clear_widgets()

        # Populate MDList with username and post content
        for i in stories:
            self.ids.ct_story_container.add_widget(TwoLineListItem(text=f'{i[2]}', secondary_text=f'{i[3]}'))
        db_connect.close()

    def callback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "SuccessScreen"


class AddMtPostScreen(Screen):
    def mt_submit(self):
        db_connect = mysql.connector.connect(
            user="root",
            password="",
            host="localhost",
            database="bonfire"
        )
        # Create cursor
        c = db_connect.cursor()

        username = self.manager.get_screen('LoginScreen').current_user
        user_ID = self.manager.get_screen('LoginScreen').user_ID

        # Add record to database
        sql_command = "INSERT INTO posts (user_ID, username, content, location) VALUES (%s, %s, %s, 'mountain')"
        values = (user_ID, username, self.ids.post_input.text,)

        # Execute command
        c.execute(sql_command, values)

        # TODO check for empty post
        # # post = self.root.ids.post_input.text
        # self.root.ids.post_input_label.text = f'{self.root.ids.post_input.text}'

        # Clear input box
        self.ids.post_input.text = ''

        # Commit changes to database
        db_connect.commit()
        db_connect.close()

        self.manager.current = 'ViewMtPostScreen'

    def callback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "SuccessScreen"


class AddPtPostScreen(Screen):
    def pt_submit(self):
        db_connect = mysql.connector.connect(
            user="root",
            password="",
            host="localhost",
            database="bonfire"
        )
        # Create cursor
        c = db_connect.cursor()
        username = self.manager.get_screen('LoginScreen').current_user
        user_ID = self.manager.get_screen('LoginScreen').user_ID

        # Add record to database
        sql_command = "INSERT INTO posts (user_ID, username, content, location) VALUES (%s, %s, %s, 'piedmont')"
        values = (user_ID, username, self.ids.post_input.text,)

        # Execute command
        c.execute(sql_command, values)

        # TODO check for empty post
        # # post = self.root.ids.post_input.text
        # self.root.ids.post_input_label.text = f'{self.root.ids.post_input.text}'

        # Clear input box
        self.ids.post_input.text = ''

        # Commit changes to database
        db_connect.commit()
        db_connect.close()

        self.manager.current = 'ViewPtPostScreen'

    def callback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "SuccessScreen"


class AddCtPostScreen(Screen):
    def ct_submit(self):
        db_connect = mysql.connector.connect(
            user="root",
            password="",
            host="localhost",
            database="bonfire"
        )
        # Create cursor
        c = db_connect.cursor()
        username = self.manager.get_screen('LoginScreen').current_user
        user_ID = self.manager.get_screen('LoginScreen').user_ID

        # Add record to database
        sql_command = "INSERT INTO posts (user_ID, username, content, location) VALUES (%s, %s, %s, 'coast')"
        values = (user_ID, username, self.ids.post_input.text,)

        # Execute command
        c.execute(sql_command, values)

        # TODO check for empty post
        # # post = self.root.ids.post_input.text
        # self.root.ids.post_input_label.text = f'{self.root.ids.post_input.text}'

        # Clear input box
        self.ids.post_input.text = ''

        # Commit changes to database
        db_connect.commit()
        db_connect.close()

        self.manager.current = 'ViewCtPostScreen'

    def callback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "SuccessScreen"


class UserPostScreen(Screen):
    def on_enter(self):
        db_connect = mysql.connector.connect(
            user="root",
            password="",
            host="localhost",
            database="bonfire"
        )
        # Create cursor
        c = db_connect.cursor()

        username = self.manager.get_screen('LoginScreen').current_user

        # Get stories from database
        sql_command = "SELECT * FROM posts JOIN login ON posts.user_ID = login.user_ID WHERE login.username = %s"
        c.execute(sql_command, (username,))
        stories = c.fetchall()

        # Prevent repeats
        self.ids.user_story_container.clear_widgets()

        for i in stories:
            story = ThreeLineAvatarIconListItem(IconLeftWidget(icon="pencil-outline"), IconRightWidget(icon="delete"))
            story.text = f'{i[2]}'
            story.secondary_text = f'{i[3]}'
            story.tertiary_text = f'Location: {i[4]}'
            story.ids.primary_key = i[0]
            # story.children[1].bind(on_press =self.remove_story)

            self.ids.user_story_container.add_widget(story)

    # TODO Fix (never reaches)
    def remove_story(self, instance):
        print("remove story")
        primary_key = instance.ids.primary_key
        self.user_story_container.remove_widget(instance)

        db_connect = mysql.connector.connect(
            user="root",
            password="",
            host="localhost",
            database="bonfire"
        )
        # Create cursor
        c = db_connect.cursor()
        sql_command = "DELETE FROM posts WHERE post_id = %s"
        c.execute(sql_command, (primary_key,))
        db_connect.commit()

        # self.ids.user_story_container.remove_widget(instance)
    def callback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "SuccessScreen"


class Bonfire(MDApp):
    database = mysql.connector.Connect(host="localhost", user="root", password="", database="bonfire")
    cursor = database.cursor()

    def build(self):
        # window icon
        self.icon = "img.png"

        Builder.load_file("post.kv")

        screen_manager = ScreenManager()
        screen_manager.add_widget(LoginScreen(name='LoginScreen'))
        screen_manager.add_widget(SuccessScreen(name='SuccessScreen'))
        screen_manager.add_widget(SignupScreen(name='SignupScreen'))
        screen_manager.add_widget(ForgotPasswordScreen(name='ForgotPasswordScreen'))
        screen_manager.add_widget(ViewMtPostScreen(name='ViewMtPostScreen'))
        screen_manager.add_widget(AddMtPostScreen(name='AddMtPostScreen'))
        screen_manager.add_widget(ViewPtPostScreen(name='ViewPtPostScreen'))
        screen_manager.add_widget(AddPtPostScreen(name='AddPtPostScreen'))
        screen_manager.add_widget(ViewCtPostScreen(name='ViewCtPostScreen'))
        screen_manager.add_widget(AddCtPostScreen(name='AddCtPostScreen'))
        screen_manager.add_widget(UserPostScreen(name='UserPostScreen'))

        return screen_manager


if __name__ == '__main__':
    Bonfire().run()




