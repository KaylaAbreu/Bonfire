from kivymd.uix.menu import MDDropdownMenu
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import TwoLineListItem, ThreeLineAvatarIconListItem, IconRightWidget, IconLeftWidget, \
    ThreeLineListItem
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton
import requests
import mysql.connector
from kivymd.uix.textfield import MDTextField
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets
import string
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

Window.size = (350, 580)


class MyScreenManager(ScreenManager):
    pass


class LoginScreen(Screen):

    def on_signup(self):
        # Switch to the SignupScreen
        self.manager.current = 'signup'

    def on_forgotPassword(self):

        self.manager.current = 'forgotPassword'

    def on_login(self, username, password):
        username = self.ids.username.text
        password = self.ids.password.text

        if self.check_credentials(username, password):
            if username == "admin":
                self.manager.current = 'admin'
            else:
                self.manager.current = 'success'
        else:

            self.ids.error_label.text = "Invalid username or password"

    def check_credentials(self, username, password):
        app = MDApp.get_running_app()
        # Query the database to check if the credentials are valid
        query = "select * from login where username = %s and password = %s"
        values = (username, password)
        app.cursor.execute(query, values)
        result = app.cursor.fetchone()
        if result:
            self.user_ID = result[0]
            self.current_user = username
        return result is not None

class AdminScreen(Screen):

    def view_users(self):
        users = self.get_users_from_database()

        # Switch to the ViewUsersScreen and pass the list of users
        view_users_screen = self.manager.get_screen('viewUsers')
        view_users_screen.display_users(users)
        self.manager.current = 'viewUsers'

    def get_users_from_database(self):
        app = MDApp.get_running_app()
        query = "SELECT username FROM login"
        app.cursor.execute(query)
        users = [user[0] for user in app.cursor.fetchall()]
        self.manager.get_screen('viewUsers').display_users(users)
        return users

    def delete_posts(self):
        posts = self.get_posts_from_database()
        delete_posts_screen = self.manager.get_screen('deletePosts')
        delete_posts_screen.display_posts(posts)
        self.manager.current = 'deletePosts'

    def get_posts_from_database(self):
        app = MDApp.get_running_app()
        query = "SELECT username, content, location FROM posts"
        app.cursor.execute(query)
        posts = app.cursor.fetchall()
        return posts

    def on_logout(self):
        self.manager.current = 'login'


class ViewUsersScreen(Screen):

    def display_users(self, users):
        user_list = self.ids.user_list
        user_list.clear_widgets()

        for index, user in enumerate(users, start=1):
            user_layout = BoxLayout(orientation='horizontal')
            user_label = Label(
                text=f"{index}. {user}",
                font_size='20sp',
                size_hint=(None, None),
                size=('150dp', '30dp')
            )
            delete_button = MDIconButton(
                icon="delete",
                size_hint=(None, None),
                size=('50dp', '40dp')
            )

            user_list.add_widget(user_layout)
            user_layout.add_widget(user_label)
            user_layout.add_widget(delete_button)

    def on_back(self):
        self.manager.current = 'admin'

class DeletePostsScreen(Screen):
    def display_posts(self, posts):
        posts_list = self.ids.posts_list
        posts_list.clear_widgets()

        for posts in posts:
            post_label = Label(text=f"Username: {posts[0]}\nContent: {posts[1]}\nLocation: {posts[2]}",
                               font_size='15sp')
            posts_list.add_widget(post_label)

    def on_back(self):
        self.manager.current = 'admin'


class SignupScreen(Screen):
    def on_login(self):
        self.manager.current = 'login'

    def send_data(self, username, password, email):
        app = MDApp.get_running_app()

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

            self.manager.current = 'login'

    def check_username_exists(self, username):
        app = MDApp.get_running_app()

        # Query the database to check if the username already exists
        query = "SELECT username FROM login WHERE username = %s"
        app.cursor.execute(query, (username,))
        result = app.cursor.fetchone()

        return result is not None


class ForgotPasswordScreen(Screen):
    def on_login(self):

        self.manager.current = 'login'

    def store_reset_code(self, username, reset_code):
        app = MDApp.get_running_app()
        try:

            query = "SELECT * FROM login WHERE username = %s"
            app.cursor.execute(query, (username,))
            result = app.cursor.fetchone()

            if result:

                update_query = "UPDATE login SET reset_code = %s WHERE username = %s"
                app.cursor.execute(update_query, (reset_code, username))
                app.database.commit()
                self.ids.message_label.text = "Reset code updated successfully."
            else:

                self.ids.error_label.text = "User not found."
        except Exception as e:
            print("Error updating reset code:", str(e))

    def send_reset_code(self, username):
        # Retrieve the user's email address from the database based on the username
        username = self.ids.username.text

        user_email = self.get_user_email(username)
        if user_email:
            # Generate a reset code (you can use a random code generator)
            reset_code = self.generate_random_code(5)

            # Send and store the reset code via email

            self.store_reset_code(username, reset_code)

            self.send_reset_email(user_email, reset_code)

            self.manager.current = 'changePassword'

        else:

            self.ids.error_label.text = "User not found."

    def generate_random_code(self, length):
        characters = string.digits
        code = ''.join(secrets.choice(characters) for _ in range(length))
        return code

    def get_user_email(self, username):
        app = MDApp.get_running_app()
        query = "SELECT email FROM login WHERE username = %s"
        app.cursor.execute(query, (username,))
        result = app.cursor.fetchone()
        if result:
            return result[0]
        return None

    def send_reset_email(self, recipient_email, reset_code):
        # Sender's and recipient's email addresses
        sender_email = "editorforbonfire01@gmail.com"
        sender_password = "uafj tgqa acjz odil"
        subject = "Bonfire Password Reset Code"
        message = f"Your password reset code is: {reset_code}"

        # Create an email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # Connect to the SMTP server and send the email
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            server.quit()
        except Exception as e:
            print("Email could not be sent. Error:", str(e))
class SuccessScreen(Screen):
    def on_logout(self):
        self.manager.current = 'login'

class ChangePasswordScreen(Screen):
    def change_password(self, username, reset_code, new_password):
        # Verify the reset code
        if self.verify_reset_code(username, reset_code):
            # Change the password
            self.change_user_password(username, new_password)
            self.manager.current = 'login'
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



class Alerts():
    def __init__(self):
        # Initialize headlines for dialog box in Welcome Screens
        self.headline1 = None
        self.headline2 = None
        self.headline3 = None

    def alerts(self):
        state = "NC"
        response = requests.get(f'https://api.weather.gov/alerts/active?area={state}').json()

        mountains = ['Cherokee;', 'Graham;', 'Clay;', 'Macon;', 'Swain;', 'Jackson;', 'Haywood;', 'Transylvania;',
                     'Henderson;', 'Buncombe;', 'Madison;', 'Yancey;', 'Mitchell;', 'McDowell;', 'Rutherford;', 'Polk;',
                     'Burke;', 'Caldwell;', 'Avery;', 'Watauga;', 'Ashe;', 'Wilkes;', 'Alleghany;']
        piedmont = ['Cleveland;', 'Gaston;', 'Lincoln;', 'Catawba;', 'Alexander;', 'Iredell;', 'Mecklenburg;', 'Union;',
                    'Anson;', 'Richmond;', 'Montgomery;', 'Stanly;', 'Cabarrus;', 'Rowan;', 'Moore;', 'Lee;', 'Chatham;',
                    'Randolph;', 'Davidson;', 'Davie;', 'Yadkin;', 'Forsyth;', 'Guilford;', 'Orange;', 'Wake;', 'Franklin;',
                    'Durham;', 'Orange;', 'Alamance;', 'Surry;', 'Stokes;', 'Rockingham;', 'Caswell;', 'Person;', 'Granville;',
                    'Vance;', 'Warren;']
        coast = ['Brunswick;', 'Columbus;', 'Robeson;', 'Scotland;', 'Hoke;', 'Bladen;', 'Cumberland;', 'Harnett;', 'Sampson;',
                 'Pender;', 'Duplin;', 'Onslow;', 'Jones;', 'Carteret;', 'Craven;', 'Lenior;', 'Wayne;', 'Johnston;', 'Wilson;',
                 'Nash;', 'Edgecombe;', 'Pitt;', 'Greene;', 'Pamlico;', 'Hyde;', 'Beaufort;', 'Dare;', 'Tyrrell;', 'Washington;',
                 'Martin;', 'Bertie;', 'Halifax;', 'Northampton;', 'Hertford;', 'Gates;', 'Currituck;', 'Camden;', 'Pasquotank;',
                 'Perquimans;', 'Chowan;']

        alert = False
        # Loop through mountains array and check to see if a mountain county is found in the 'areaDesc' of the JSON file
        for county in mountains:
            for i in response['features']:
                area_desc = i['properties']['areaDesc']
                if county in area_desc:
                    alert = True
                    self.headline1 = i['properties']['headline']  # brief warning
                    # print(i['properties']['areaDesc'])          # county names
                    # print(i['properties']['description'])       # What Where When Impact descriptions
                    break
                else:
                    alert = False

        if not alert:
            self.headline1 = "No Alerts at this Time"

        # Loop through piedmont array and check to see if a piedmont county is found in the 'areaDesc' of the JSON file
        for county in piedmont:
            for i in response['features']:
                area_desc = i['properties']['areaDesc']
                if county in area_desc:
                    alert = True
                    self.headline2 = i['properties']['headline']  # brief warning
                    # print(i['properties']['areaDesc'])          # county names
                    # print(i['properties']['description'])       # What Where When Impact descriptions
                    break
        if not alert:
            self.headline2 = "No Alerts at this Time"

        # Loop through coast array and check to see if a coastal county is found in the 'areaDesc' of the JSON file
        for county in coast:
            for i in response['features']:
                area_desc = i['properties']['areaDesc']
                if county in area_desc:
                    alert = True
                    # self.headline3 = i['properties']['headline']   # brief warning
                    # print(i['properties']['areaDesc'])             # county names
                    # print(i['properties']['description'])
                    self.headline3 = i['properties']['description']  # What Where When Impact descriptions
                    break

        if not alert:
            self.headline3 = "No Alerts at this Time"


class WelcomeMtScreen(Screen):
    # Get alert headline from Alerts() and display in pop up
    def on_enter(self):
        alert_headline = Alerts()
        alert_headline.alerts()
        self.dialog = MDDialog(
            title="Alert for the Mountain Region",
            text=alert_headline.headline1,
            buttons=[MDRectangleFlatButton(text="Close", on_release=self.close)]
        )
        self.dialog.open()

    def close(self, *args):
        self.dialog.dismiss()

    def callback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "success"


class WelcomePtScreen(Screen):
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
        self.manager.current = "success"


class WelcomeCtScreen(Screen):
    # Get alert headline from Alerts() and display in pop up
    def on_enter(self):
        alert_headline = Alerts()
        alert_headline.alerts()
        self.dialog = MDDialog(
            title="Alert for the Coast Region",
            text=alert_headline.headline3,
            buttons=[MDRectangleFlatButton(text="Close", on_release=self.close)]
        )
        self.dialog.open()

    def close(self, *args):
        self.dialog.dismiss()

    def callback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "success"


class ViewMtPostScreen(Screen):
    def on_enter(self):
        app = MDApp.get_running_app()
        app.cursor.execute("SELECT * FROM posts WHERE location = 'mountain'")
        stories = app.cursor.fetchall()
        # Prevent repeats
        self.ids.mt_story_container.clear_widgets()
        for i in stories:
            post_id = i[0]
            post_user = i[2]
            post_body = i[3]

            post_display = TwoLineListItem(
                text=post_user,
                secondary_text=post_body,
                on_release=lambda x, post_id=post_id: self.open_comments(post_id),
            )
            expand_button = MDRectangleFlatButton(text="View Story",
                                                  pos_hint={'center_x': 0.8},
                                                  text_color="black")
            expand_button.bind(on_release=lambda instance, post_id=post_id, post_body=post_body: self.expand_story(post_id, post_body))
            self.ids.mt_story_container.add_widget(expand_button)
            self.ids.mt_story_container.add_widget(post_display)

    def open_comments(self, post_id):
        app = MDApp.get_running_app()
        app.cursor.execute("SELECT * FROM comments WHERE post_ID = %s", (post_id,))
        comments = app.cursor.fetchall()

        menu_posts = [
            {
                "viewclass": "TwoLineListItem",
                "text": comment[3],
                "secondary_text": comment[4],
                "on_release": lambda x=comment[4]: dropdown.dismiss(),
            }
            for comment in comments
        ]
        dropdown = MDDropdownMenu(
            caller=self.ids.mt_story_container,
            items=menu_posts,
            width_mult=10,
            position="center",
        )
        dropdown.open()

    def menu_callback(self, instance):
        instance.dismiss()

    def expand_story(self, post_id, post_body):
        self.dialog = MDDialog(text=post_body,
            buttons=[
                MDRectangleFlatButton(
                    text="Add Comment",
                    pos_hint={"center_x":0.5, "center_y":0.5},
                    on_release=lambda instance, post_id=post_id: self.add_mt_comment(post_id)
                )
            ]
        )
        self.dialog.open()

    def add_mt_comment(self, post_id):
        self.dialog.dismiss()
        self.manager.get_screen('MtCommentScreen').post_id = post_id
        self.manager.current = "MtCommentScreen"

    def callback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "success"


class MtCommentScreen(Screen):
    post_id = None
    def mt_comment_submit(self):
        app = MDApp.get_running_app()

        username = self.manager.get_screen('login').current_user
        user_ID = self.manager.get_screen('login').user_ID
        # post_ID = self.manager.get_screen('ViewMtPostScreen').post_id

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
            dialog = MDDialog(text="Posts must be under 255 characters")
            dialog.open()
            self.manager.current = 'MtCommentScreen'

    def callback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "success"

class PtCommentScreen(Screen):
    post_id = None

    def pt_comment_submit(self):
        app = MDApp.get_running_app()

        username = self.manager.get_screen('login').current_user
        user_ID = self.manager.get_screen('login').user_ID
        # post_ID = self.manager.get_screen('ViewMtPostScreen').post_id

        # Check length of post
        if len(self.ids.post_input.text) == 0:
            dialog = MDDialog(text="Please add a comment")
            dialog.open()
            self.manager.current = 'PtCommentScreen'

        elif len(self.ids.post_input.text) < 255:
            # Add record to database
            sql_command = "INSERT INTO comments (post_ID, user_ID, username, content, location) VALUES (%s, %s, %s, %s, 'piedmont')"
            values = (self.post_id, user_ID, username, self.ids.post_input.text,)

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
            self.manager.current = 'PtCommentScreen'

    def callback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "success"


class CtCommentScreen(Screen):
    post_id = None

    def ct_comment_submit(self):
        app = MDApp.get_running_app()

        username = self.manager.get_screen('login').current_user
        user_ID = self.manager.get_screen('login').user_ID
        # post_ID = self.manager.get_screen('ViewMtPostScreen').post_id

        # Check length of post
        if len(self.ids.post_input.text) == 0:
            dialog = MDDialog(text="Please add a comment")
            dialog.open()
            self.manager.current = 'CtCommentScreen'

        elif len(self.ids.post_input.text) < 255:
            # Add record to database
            sql_command = "INSERT INTO comments (post_ID, user_ID, username, content, location) VALUES (%s, %s, %s, %s, 'coast')"
            values = (self.post_id, user_ID, username, self.ids.post_input.text,)

            # Execute command
            app.cursor.execute(sql_command, values)

            # Clear input box
            self.ids.post_input.text = ''

            # Commit changes to database
            app.database.commit()

            self.manager.current = 'ViewCtPostScreen'
        else:
            dialog = MDDialog(text="Posts must be under 255 characters")
            dialog.open()
            self.manager.current = 'CtCommentScreen'

    def callback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "success"


class ViewPtPostScreen(Screen):
    def on_enter(self):
        app = MDApp.get_running_app()
        # Get stories from database
        app.cursor.execute("SELECT * FROM posts WHERE location = 'piedmont'")
        stories = app.cursor.fetchall()

        # Prevent repeats
        self.ids.pt_story_container.clear_widgets()

        # Populate MDList with username and post content
        for i in stories:
            post_id = i[0]
            post_user = i[2]
            post_body = i[3]

            post_display = TwoLineListItem(
                text=post_user,
                secondary_text=post_body,
                on_release=lambda x, post_id=post_id: self.open_comments(post_id),
            )
            expand_button = MDRectangleFlatButton(text="View Story",
                                                  pos_hint={'center_x': 0.8},
                                                  text_color="black")
            expand_button.bind(
                on_release=lambda instance, post_id=post_id, post_body=post_body: self.expand_story(post_id, post_body))
            self.ids.pt_story_container.add_widget(expand_button)
            self.ids.pt_story_container.add_widget(post_display)
            # expand_button = MDRectangleFlatButton(text="More",
            #                                       pos_hint={'center_x': 0.8},
            #                                       text_color="black")
            # expand_button.bind(on_release=lambda instance, post=i[3]: self.expand_story(post))
            # self.ids.pt_story_container.add_widget(expand_button)
            # self.ids.pt_story_container.add_widget(TwoLineListItem(text=f'{i[2]}', secondary_text=f'{i[3]}'))

    def open_comments(self, post_id):
        app = MDApp.get_running_app()
        app.cursor.execute("SELECT * FROM comments WHERE post_ID = %s", (post_id,))
        comments = app.cursor.fetchall()

        menu_posts = [
            {
                "viewclass": "TwoLineListItem",
                "text": comment[3],
                "secondary_text": comment[4],
                "on_release": lambda x=comment[4]: dropdown.dismiss(),
            }
            for comment in comments
        ]
        dropdown = MDDropdownMenu(
            caller=self.ids.pt_story_container,
            items=menu_posts,
            width_mult=4,
        )
        dropdown.open()

    def menu_callback(self, instance):
        instance.dismiss()

    def expand_story(self, post_id, post_body):
        self.dialog = MDDialog(text=post_body,
                               buttons=[
                                   MDRectangleFlatButton(
                                       text="Add Comment",
                                       pos_hint={"center_x":0.5, "center_y":0.5},
                                       on_release=lambda instance, post_id=post_id: self.add_pt_comment(post_id)
                                   )
                               ]
                               )
        self.dialog.open()

    def add_pt_comment(self, post_id):
        self.dialog.dismiss()
        self.manager.get_screen('PtCommentScreen').post_id = post_id
        self.manager.current = "PtCommentScreen"

    def callback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "success"


class ViewCtPostScreen(Screen):
    def on_enter(self):
        app = MDApp.get_running_app()

        # Get stories from database
        app.cursor.execute("SELECT * FROM posts WHERE location = 'coast'")
        stories = app.cursor.fetchall()

        # Prevent repeats
        self.ids.ct_story_container.clear_widgets()

        # Populate MDList with username and post content
        for i in stories:
            post_id = i[0]
            post_user = i[2]
            post_body = i[3]

            post_display = TwoLineListItem(
                text=post_user,
                secondary_text=post_body,
                on_release=lambda x, post_id=post_id: self.open_comments(post_id),
            )
            expand_button = MDRectangleFlatButton(text="View Story",
                                                  pos_hint={'center_x': 0.8},
                                                  text_color="black")
            expand_button.bind(
                on_release=lambda instance, post_id=post_id, post_body=post_body: self.expand_story(post_id, post_body))
            self.ids.ct_story_container.add_widget(expand_button)
            self.ids.ct_story_container.add_widget(post_display)
            # expand_button = MDRectangleFlatButton(text="More",
            #                                pos_hint={'center_x': 0.8},
            #                                text_color="black")
            # expand_button.bind(on_release=lambda instance, post=i[3]: self.expand_story(post))
            # self.ids.ct_story_container.add_widget(expand_button)
            # self.ids.ct_story_container.add_widget(TwoLineListItem(text=f'{i[2]}', secondary_text=f'{i[3]}'))

    def open_comments(self, post_id):
        app = MDApp.get_running_app()
        app.cursor.execute("SELECT * FROM comments WHERE post_ID = %s", (post_id,))
        comments = app.cursor.fetchall()

        menu_posts = [
            {
                "viewclass": "TwoLineListItem",
                "text": comment[3],
                "secondary_text": comment[4],
                "on_release": lambda x=comment[4]: dropdown.dismiss(),
            }
            for comment in comments
        ]
        dropdown = MDDropdownMenu(
            caller=self.ids.ct_story_container,
            items=menu_posts,
            width_mult=4,
        )
        dropdown.open()

    def menu_callback(self, instance):
        instance.dismiss()

    def expand_story(self, post_id, post_body):
        self.dialog = MDDialog(text=post_body,
            buttons=[
                MDRectangleFlatButton(
                    text="Add Comment",
                    pos_hint={"center_x":0.5, "center_y":0.5},
                    on_release=lambda instance, post_id=post_id: self.add_ct_comment(post_id)
                )
            ]
        )
        self.dialog.open()

    def add_ct_comment(self, post_id):
        self.dialog.dismiss()
        self.manager.get_screen('CtCommentScreen').post_id = post_id
        self.manager.current = "CtCommentScreen"

    def callback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "success"


class AddMtPostScreen(Screen):
    def mt_submit(self):
        app = MDApp.get_running_app()

        username = self.manager.get_screen('login').current_user
        user_ID = self.manager.get_screen('login').user_ID

        # Check length of post
        if len(self.ids.post_input.text) == 0:
            dialog = MDDialog(text="Please add a story")
            dialog.open()
            self.manager.current = 'AddMtPostScreen'

        elif len(self.ids.post_input.text) < 255:
            # Add record to database
            sql_command = "INSERT INTO posts (user_ID, username, content, location) VALUES (%s, %s, %s, 'mountain')"
            values = (user_ID, username, self.ids.post_input.text,)

            # Execute command
            app.cursor.execute(sql_command, values)

            # Clear input box
            self.ids.post_input.text = ''

            # Commit changes to database
            app.database.commit()

            self.manager.current = 'ViewMtPostScreen'
        else:
            dialog = MDDialog(text="Posts must be under 255 characters")
            dialog.open()
            self.manager.current = 'AddMtPostScreen'

    def callback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "success"


class AddPtPostScreen(Screen):
    def pt_submit(self):
        app = MDApp.get_running_app()

        username = self.manager.get_screen('login').current_user
        user_ID = self.manager.get_screen('login').user_ID

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
        self.manager.current = "success"


class AddCtPostScreen(Screen):
    def ct_submit(self):
        app = MDApp.get_running_app()

        username = self.manager.get_screen('login').current_user
        user_ID = self.manager.get_screen('login').user_ID

        # Check length of post
        if len(self.ids.post_input.text) == 0:
            dialog = MDDialog(text="Please add a story")
            dialog.open()
            self.manager.current = 'AddCtPostScreen'

        elif len(self.ids.post_input.text) < 255:
            # Add record to database
            sql_command = "INSERT INTO posts (user_ID, username, content, location) VALUES (%s, %s, %s, 'coast')"
            values = (user_ID, username, self.ids.post_input.text,)

            # Execute command
            app.cursor.execute(sql_command, values)

            # Clear input box
            self.ids.post_input.text = ''

            # Commit changes to database
            app.database.commit()

            self.manager.current = 'ViewCtPostScreen'
        else:
            dialog = MDDialog(text="Posts must be under 255 characters")
            dialog.open()
            self.manager.current = 'AddCtPostScreen'



    def callback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "success"


class UserPostScreen(Screen):
    def on_enter(self):
        app = MDApp.get_running_app()

        username = self.manager.get_screen('login').current_user

        # Get stories from database
        sql_command = "SELECT * FROM posts JOIN login ON posts.user_ID = login.user_ID WHERE login.username = %s"
        app.cursor.execute(sql_command, (username,))
        stories = app.cursor.fetchall()

        # Prevent repeats
        self.ids.user_story_container.clear_widgets()

        for i in stories:
            self.post_id = i[0]
            self.post_content = i[3]

            edit_button = MDIconButton(icon="pencil-outline")
            edit_button.bind(on_release=lambda instance, post=self.post_id: self.edit_story(post))
            edit_button.edit_id = self.post_id
            self.ids.user_story_container.add_widget(edit_button)

            delete_button = MDIconButton(icon="delete")
            delete_button.bind(on_release=lambda instance, post=self.post_id: self.remove_story(post))
            delete_button.del_id = self.post_id
            self.ids.user_story_container.add_widget(delete_button)

            ulist = ThreeLineListItem(
                text=f'{i[2]}',
                secondary_text=f'{i[3]}',
                tertiary_text=f'Location: {i[4]}')
            ulist.post_id = self.post_id
            self.ids.user_story_container.add_widget(ulist)


    def edit_story(self, post):
        self.new_content=MDTextField(multiline=True)
        self.dialog = MDDialog(title='Edit your story',
                               text=self.post_content,
                               type="custom",
                               content_cls=self.new_content,
                               buttons=[
                                   MDRectangleFlatButton(
                                       text="Save",
                                       on_release=lambda x: self.save_story(post))])
        self.dialog.open()

    def save_story(self,post):
        save_new_content = self.new_content.text

        app = MDApp.get_running_app()

        sql_command = "UPDATE posts SET content=%s WHERE post_id = %s"
        app.cursor.execute(sql_command, (save_new_content,post))
        app.database.commit()

        self.dialog.dismiss()
        self.on_enter()
        self.manager.current = "UserPostScreen"

    def remove_story(self, post):
        # If yes button is pressed in dialog box, item will be deleted
        def yes(instance):
            app = MDApp.get_running_app()

            sql_command = "DELETE FROM posts WHERE post_id = %s"
            app.cursor.execute(sql_command, (post,))
            app.database.commit()

            # remove TwoListItem and Button
            remove_container = []
            for widget in self.ids.user_story_container.children:
                if hasattr(widget, 'post_id') and widget.post_id == post:
                    remove_container.append(widget)
                elif hasattr(widget, 'edit_id') and widget.edit_id == post:
                    remove_container.append(widget)
                elif hasattr(widget, 'del_id') and widget.del_id == post:
                    remove_container.append(widget)
            for widget in remove_container:
                self.ids.user_story_container.remove_widget(widget)

            self.dialog.dismiss()
            self.on_enter()
            self.manager.current = "UserPostScreen"

        # If cancel button is pressed in dialog box, dialog box will close with no change
        def cancel(instance):
            self.dialog.dismiss()

        self.dialog = MDDialog(
                               text='Are you sure you want to delete this post?',
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

    def callback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "success"


class Bonfire(MDApp):
    # database = mysql.connector.Connect(host="localhost", user="root", password="admin321", database="bonfire")
    database = mysql.connector.Connect(host="localhost", user="root", password="", database="bonfire")
    cursor = database.cursor()
    cursor.execute("select * from login")
    for i in cursor.fetchall():
        print(i[0], i[1])

    def build(self):
        # window icon
        self.icon = "img.png"

        Builder.load_file("Bonfire2.kv")

        screen_manager = ScreenManager()
        screen_manager.add_widget(LoginScreen(name='login'))
        screen_manager.add_widget(AdminScreen(name='admin'))
        screen_manager.add_widget(SuccessScreen(name='success'))
        screen_manager.add_widget(SignupScreen(name='signup'))
        screen_manager.add_widget(ForgotPasswordScreen(name='forgotPassword'))
        screen_manager.add_widget(ChangePasswordScreen(name='changePassword'))
        screen_manager.add_widget(ViewUsersScreen(name='viewUsers'))
        screen_manager.add_widget(DeletePostsScreen(name='deletePosts'))
        screen_manager.add_widget(ViewMtPostScreen(name='ViewMtPostScreen'))
        screen_manager.add_widget(AddMtPostScreen(name='AddMtPostScreen'))
        screen_manager.add_widget(ViewPtPostScreen(name='ViewPtPostScreen'))
        screen_manager.add_widget(AddPtPostScreen(name='AddPtPostScreen'))
        screen_manager.add_widget(ViewCtPostScreen(name='ViewCtPostScreen'))
        screen_manager.add_widget(AddCtPostScreen(name='AddCtPostScreen'))
        screen_manager.add_widget(UserPostScreen(name='UserPostScreen'))
        screen_manager.add_widget(MtCommentScreen(name='MtCommentScreen'))
        screen_manager.add_widget(PtCommentScreen(name='PtCommentScreen'))
        screen_manager.add_widget(CtCommentScreen(name='CtCommentScreen'))
        screen_manager.add_widget(WelcomeMtScreen(name='WelcomeMtScreen'))
        screen_manager.add_widget(WelcomePtScreen(name='WelcomePtScreen'))
        screen_manager.add_widget(WelcomeCtScreen(name='WelcomeCtScreen'))

        return screen_manager


if __name__ == '__main__':
    Bonfire().run()
