from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import TwoLineListItem, ThreeLineListItem
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton
from kivy.uix.button import Button
import requests
import mysql.connector
from kivymd.uix.textfield import MDTextField
from kivy.uix.scrollview import ScrollView

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
    # pass
    def callback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "MenuScreen"


class Alerts():
    def __init__(self):
        self.headline1 = None
        self.headline2 = None
        self.headline3 = None

    def alerts(self):
        state = "NC"
        response = requests.get(f'https://api.weather.gov/alerts/active?area={state}').json()
        mountains = ['Cherokee;', 'Graham;', 'Clay;', 'Macon;', 'Swain;', 'Jackson;', 'Haywood;', 'Transylvania;',
                     'Henderson;',
                     'Buncombe;', 'Madison;', 'Yancey;', 'Mitchell;', 'McDowell;', 'Rutherford;', 'Polk;', 'Burke;',
                     'Caldwell;',
                     'Avery;', 'Watauga;', 'Ashe;', 'Wilkes;', 'Alleghany;']
        piedmont = ['Cleveland;', 'Gaston;', 'Lincoln;', 'Catawba;', 'Alexander;', 'Iredell;', 'Mecklenburg;', 'Union;',
                    'Anson;', 'Richmond;', 'Montgomery;', 'Stanly;', 'Cabarrus;', 'Rowan;', 'Moore;', 'Lee;',
                    'Chatham;',
                    'Randolph;', 'Davidson;', 'Davie;', 'Yadkin;', 'Forsyth;', 'Guilford;', 'Orange;', 'Wake;',
                    'Franklin;',
                    'Durham;', 'Orange;', 'Alamance;', 'Surry;', 'Stokes;', 'Rockingham;', 'Caswell;', 'Person;',
                    'Granville;',
                    'Vance;', 'Warren;']
        coast = ['Brunswick;', 'Columbus;', 'Robeson;', 'Scotland;', 'Hoke;', 'Bladen;', 'Cumberland;', 'Harnett;',
                 'Sampson;',
                 'Pender;', 'Duplin;', 'Onslow;', 'Jones;', 'Carteret;', 'Craven;', 'Lenior;', 'Wayne;', 'Johnston;',
                 'Wilson;',
                 'Nash;', 'Edgecombe;', 'Pitt;', 'Greene;', 'Pamlico;', 'Hyde;', 'Beaufort;', 'Dare;', 'Tyrrell;',
                 'Washington;',
                 'Martin;', 'Bertie;', 'Halifax;', 'Northampton;', 'Hertford;', 'Gates;', 'Currituck;', 'Camden;',
                 'Pasquotank;',
                 'Perquimans;', 'Chowan;']

        found_county = ['']
        for county in mountains:
            for i in response['features']:
                area_desc = i['properties']['areaDesc']
                if county in area_desc:
                    found_county = county
                    self.headline1 = i['properties']['headline']
                    # print(i['properties']['areaDesc'])
                    # print(i['properties']['description'])
                    break
            if found_county:
                break
        if found_county is None:
            print("none")

        for county in piedmont:
            for i in response['features']:
                area_desc = i['properties']['areaDesc']
                if county in area_desc:
                    found_county = county
                    self.headline2 = i['properties']['headline']
                    # print(i['properties']['areaDesc'])
                    # print(i['properties']['description'])
                    break
            if found_county:
                break
        if found_county is None:
            print("none")

        for county in coast:
            for i in response['features']:
                area_desc = i['properties']['areaDesc']
                if county in area_desc:
                    found_county = county
                    self.headline3 = i['properties']['headline']
                    # print(i['properties']['areaDesc'])
                    # print(i['properties']['description'])
                    break
            if found_county:
                break
        if found_county is None:
            print("none")


class MenuScreen(Screen):
    pass


class AllTips(Screen):
    def on_enter(self):
        app = MDApp.get_running_app()
        app.cursor.execute("SELECT * FROM tips")
        tips = app.cursor.fetchall()

        # Clear tips from previous load
        self.ids.all_tips_container.clear_widgets()

        for i in tips:
            tip_title = i[0]
            tip_category = i[2]
            tip_body = i[1]

            tips_display = TwoLineListItem(
                text=tip_title,
                secondary_text=tip_category,
                # tertiary_text=tip_body,
                on_release=lambda x, tip_title=tip_title: self.expand_tip(tip_title, tip_body),
            )

            self.ids.all_tips_container.add_widget(tips_display)

    def expand_tip(self, title, tip):

        app = MDApp.get_running_app()
        app.cursor.execute("SELECT * FROM tips WHERE title = %s", (title,))
        content = app.cursor.fetchall()

        for i in content:
            tip_content = i[1]

        #create layout
        layout = BoxLayout(orientation='vertical', padding=(10, 10, 10, 10))

        #create label for scrollview
        body_label=MDLabel(text=tip_content, size_hint_y=None, markup=True, valign="top", padding=(10,20))
        body_label.theme_text_color = "Custom"
        body_label.text_color = (250/255, 237/255, 202/255, 1 )
        body_label.bind(texture_size=body_label.setter('size'))


        #create scroll view
        body = ScrollView(size_hint=(1, 1))
        body.add_widget(body_label)

        #add label to layout
        layout.add_widget(body)

        #create dismiss button
        dismiss_button = Button(text="Dismiss",
                                on_press=self.dismiss_popup,
                                size_hint=(None, None),
                                size=(100, 50),
                                pos_hint={'center_x': 0.5, 'y': 0.10})

        layout.add_widget(dismiss_button)

        float_layout = FloatLayout(size=(Window.width - 10, Window.height - 10))
        float_layout.add_widget(layout)


        self.fulltip = Popup(title=title, content=float_layout, size=(Window.width-10, Window.height-10), auto_dismiss=True)
        self.fulltip.open()



    def dismiss_popup(self, instance):
        if self.fulltip:
            self.fulltip.dismiss()  # Dismiss the Popup

    def allTips(self):
        self.manager.current = 'AllTips'

    def mountainTips(self):
        self.manager.current = 'MountainTips'

    def piedmontTips(self):
        self.manager.current = 'PiedmontTips'

    def coastTips(self):
        self.manager.current = 'CoastTips'

    def callback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "MenuScreen"


class MountainTips(Screen):
    def on_enter(self):
        app = MDApp.get_running_app()
        app.cursor.execute("SELECT * FROM tips WHERE category = 'mountain'")
        tips = app.cursor.fetchall()

        # Clear tips from previous load
        self.ids.mountain_tips_container.clear_widgets()

        for i in tips:
            tip_title = i[0]
            tip_category = i[2]
            tip_body = i[1]

            tips_display = TwoLineListItem(
                text=tip_title,
                secondary_text=tip_category,
                # tertiary_text=tip_body,
                on_release=lambda x, tip_title=tip_title: self.expand_tip(tip_title, tip_body),
            )

            self.ids.mountain_tips_container.add_widget(tips_display)

    def expand_tip(self, title, tip):

        app = MDApp.get_running_app()
        app.cursor.execute("SELECT * FROM tips WHERE title = %s", (title,))
        content = app.cursor.fetchall()

        for i in content:
            tip_content = i[1]

        # create layout
        layout = BoxLayout(orientation='vertical', padding=(10, 10, 10, 10))

        # create label for scrollview
        body_label = MDLabel(text=tip_content, size_hint_y=None, markup=True, valign="top", padding=(10, 20))
        body_label.theme_text_color = "Custom"
        body_label.text_color = (250 / 255, 237 / 255, 202 / 255, 1)
        body_label.bind(texture_size=body_label.setter('size'))

        # create scroll view
        body = ScrollView(size_hint=(1, 1))
        body.add_widget(body_label)

        # add label to layout
        layout.add_widget(body)

        # create dismiss button
        dismiss_button = Button(text="Dismiss",
                                on_press=self.dismiss_popup,
                                size_hint=(None, None),
                                size=(100, 50),
                                pos_hint={'center_x': 0.5, 'y': 0.10})

        layout.add_widget(dismiss_button)

        float_layout = FloatLayout(size=(Window.width - 10, Window.height - 10))
        float_layout.add_widget(layout)

        self.fulltip = Popup(title=title, content=float_layout, size=(Window.width - 10, Window.height - 10),
                             auto_dismiss=True)
        self.fulltip.open()

    def dismiss_popup(self, instance):
        if self.fulltip:
            self.fulltip.dismiss()  # Dismiss the Popup

    def allTips(self):
        self.manager.current = 'AllTips'

    def mountainTips(self):
        self.manager.current = 'MountainTips'

    def piedmontTips(self):
        self.manager.current = 'PiedmontTips'

    def coastTips(self):
        self.manager.current = 'CoastTips'

    def callback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "MenuScreen"


class PiedmontTips(Screen):
    def on_enter(self):
        app = MDApp.get_running_app()
        app.cursor.execute("SELECT * FROM tips WHERE category = 'piedmont'")
        tips = app.cursor.fetchall()

        # Clear tips from previous load
        self.ids.piedmont_tips_container.clear_widgets()

        for i in tips:
            tip_title = i[0]
            tip_category = i[2]
            tip_body = i[1]

            tips_display = TwoLineListItem(
                text=tip_title,
                secondary_text=tip_category,
                # tertiary_text=tip_body,
                on_release=lambda x, tip_title=tip_title: self.expand_tip(tip_title, tip_body),
            )

            self.ids.piedmont_tips_container.add_widget(tips_display)

    def expand_tip(self, title, tip):

        app = MDApp.get_running_app()
        app.cursor.execute("SELECT * FROM tips WHERE title = %s", (title,))
        content = app.cursor.fetchall()

        for i in content:
            tip_content = i[1]

        # create layout
        layout = BoxLayout(orientation='vertical', padding=(10, 10, 10, 10))

        # create label for scrollview
        body_label = MDLabel(text=tip_content, size_hint_y=None, markup=True, valign="top", padding=(10, 20))
        body_label.theme_text_color = "Custom"
        body_label.text_color = (250 / 255, 237 / 255, 202 / 255, 1)
        body_label.bind(texture_size=body_label.setter('size'))

        # create scroll view
        body = ScrollView(size_hint=(1, 1))
        body.add_widget(body_label)

        # add label to layout
        layout.add_widget(body)

        # create dismiss button
        dismiss_button = Button(text="Dismiss",
                                on_press=self.dismiss_popup,
                                size_hint=(None, None),
                                size=(100, 50),
                                pos_hint={'center_x': 0.5, 'y': 0.10})

        layout.add_widget(dismiss_button)

        float_layout = FloatLayout(size=(Window.width - 10, Window.height - 10))
        float_layout.add_widget(layout)

        self.fulltip = Popup(title=title, content=float_layout, size=(Window.width - 10, Window.height - 10),
                             auto_dismiss=True)
        self.fulltip.open()

    def dismiss_popup(self, instance):
        if self.fulltip:
            self.fulltip.dismiss()  # Dismiss the Popup

    def allTips(self):
        self.manager.current = 'AllTips'

    def mountainTips(self):
        self.manager.current = 'MountainTips'

    def piedmontTips(self):
        self.manager.current = 'PiedmontTips'

    def coastTips(self):
        self.manager.current = 'CoastTips'

    def callback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "MenuScreen"


class CoastTips(Screen):

    def on_enter(self):
        app = MDApp.get_running_app()
        app.cursor.execute("SELECT * FROM tips WHERE category = 'coast'")
        tips = app.cursor.fetchall()

        # Clear tips from previous load
        self.ids.coast_tips_container.clear_widgets()

        for i in tips:
            tip_title = i[0]
            tip_category = i[2]
            tip_body = i[1]

            tips_display = TwoLineListItem(
                text=tip_title,
                secondary_text=tip_category,
                # tertiary_text=tip_body,
                on_release=lambda x, tip_title=tip_title: self.expand_tip(tip_title, tip_body),
            )

            self.ids.coast_tips_container.add_widget(tips_display)

    def expand_tip(self, title, tip):

        app = MDApp.get_running_app()
        app.cursor.execute("SELECT * FROM tips WHERE title = %s", (title,))
        content = app.cursor.fetchall()

        for i in content:
            tip_content = i[1]

        # create layout
        layout = BoxLayout(orientation='vertical', padding=(10, 10, 10, 10))

        # create label for scrollview
        body_label = MDLabel(text=tip_content, size_hint_y=None, markup=True, valign="top", padding=(10, 20))
        body_label.theme_text_color = "Custom"
        body_label.text_color = (250 / 255, 237 / 255, 202 / 255, 1)
        body_label.bind(texture_size=body_label.setter('size'))

        # create scroll view
        body = ScrollView(size_hint=(1, 1))
        body.add_widget(body_label)

        # add label to layout
        layout.add_widget(body)

        # create dismiss button
        dismiss_button = Button(text="Dismiss",
                                on_press=self.dismiss_popup,
                                size_hint=(None, None),
                                size=(100, 50),
                                pos_hint={'center_x': 0.5, 'y': 0.10})

        layout.add_widget(dismiss_button)

        float_layout = FloatLayout(size=(Window.width - 10, Window.height - 10))
        float_layout.add_widget(layout)

        self.fulltip = Popup(title=title, content=float_layout, size=(Window.width - 10, Window.height - 10),
                             auto_dismiss=True)
        self.fulltip.open()

    def dismiss_popup(self, instance):
        if self.fulltip:
            self.fulltip.dismiss()  # Dismiss the Popup

    def allTips(self):
        self.manager.current = 'AllTips'

    def mountainTips(self):
        self.manager.current = 'MountainTips'

    def piedmontTips(self):
        self.manager.current = 'PiedmontTips'

    def coastTips(self):
        self.manager.current = 'CoastTips'

    def callback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "MenuScreen"


class WelcomeMtScreen(Screen):
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
        self.manager.current = "SuccessScreen"


class WelcomePtScreen(Screen):
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
        self.manager.current = "SuccessScreen"


class WelcomeCtScreen(Screen):
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
        self.manager.current = "SuccessScreen"


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
            expand_button.bind(
                on_release=lambda instance, post_id=post_id, post_body=post_body: self.expand_story(post_id, post_body))
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
                                       pos_hint={"center_x": 0.5, "center_y": 0.5},
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
        self.manager.current = "SuccessScreen"


class MtCommentScreen(Screen):
    post_id = None

    def mt_comment_submit(self):
        app = MDApp.get_running_app()

        username = self.manager.get_screen('LoginScreen').current_user
        user_ID = self.manager.get_screen('LoginScreen').user_ID
        # post_ID = self.manager.get_screen('ViewMtPostScreen').post_id

        print(self.post_id)
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

        # # Prevent repeats
        # self.ids.mt_comment_container.clear_widgets()
        #
        # # Populate MDList with username and post content
        # for i in stories:
        #     expand_button = MDRectangleFlatButton(text="More",
        #                                           pos_hint={'center_x': 0.8},
        #                                           text_color="black")
        #     expand_button.bind(on_release=lambda instance, post=i[3]: self.expand_story(post))
        #     self.ids.mt_comment_container.add_widget(expand_button)
        #     self.ids.mt_comment_container.add_widget(TwoLineListItem(text=f'{i[2]}', secondary_text=f'{i[3]}'))
        #
        # db_connect.close()

    def callback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "SuccessScreen"


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
            expand_button = MDRectangleFlatButton(text="More",
                                                  pos_hint={'center_x': 0.8},
                                                  text_color="black")
            expand_button.bind(on_release=lambda instance, post=i[3]: self.expand_story(post))
            self.ids.pt_story_container.add_widget(expand_button)
            self.ids.pt_story_container.add_widget(TwoLineListItem(text=f'{i[2]}', secondary_text=f'{i[3]}'))

    def expand_story(self, post):
        dialog = MDDialog(text=post)
        dialog.open()

    def callback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "SuccessScreen"


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
            expand_button = MDRectangleFlatButton(text="More",
                                                  pos_hint={'center_x': 0.8},
                                                  text_color="black")
            expand_button.bind(on_release=lambda instance, post=i[3]: self.expand_story(post))
            self.ids.ct_story_container.add_widget(expand_button)
            self.ids.ct_story_container.add_widget(TwoLineListItem(text=f'{i[2]}', secondary_text=f'{i[3]}'))

    def expand_story(self, post):
        dialog = MDDialog(text=post)
        dialog.open()

    def callback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "SuccessScreen"


class AddMtPostScreen(Screen):
    def mt_submit(self):
        app = MDApp.get_running_app()

        username = self.manager.get_screen('LoginScreen').current_user
        user_ID = self.manager.get_screen('LoginScreen').user_ID

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
        self.manager.current = "SuccessScreen"


class AddPtPostScreen(Screen):
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
        self.manager.current = "SuccessScreen"


class AddCtPostScreen(Screen):
    def ct_submit(self):
        app = MDApp.get_running_app()

        username = self.manager.get_screen('LoginScreen').current_user
        user_ID = self.manager.get_screen('LoginScreen').user_ID

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
        self.manager.current = "SuccessScreen"


class UserPostScreen(Screen):
    def on_enter(self):
        app = MDApp.get_running_app()

        username = self.manager.get_screen('LoginScreen').current_user

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

            ulist = ThreeLineListItem(text=f'{i[2]}', secondary_text=f'{i[3]}', tertiary_text=f'Location: {i[4]}')
            ulist.post_id = self.post_id
            self.ids.user_story_container.add_widget(ulist)

    def edit_story(self, post):
        self.new_content = MDTextField(multiline=True)
        self.dialog = MDDialog(title='Edit your story',
                               text=self.post_content,
                               type="custom",
                               # content_cls=self.new_content,
                               content_cls=self.new_content,
                               # size_hint=[.5, None],
                               buttons=[MDRectangleFlatButton(text="Save", on_release=lambda x: self.save_story(post))])
        self.dialog.open()

    def save_story(self, post):
        save_new_content = self.new_content.text

        app = MDApp.get_running_app()

        sql_command = "UPDATE posts SET content=%s WHERE post_id = %s"
        app.cursor.execute(sql_command, (save_new_content, post))
        app.database.commit()

        self.dialog.dismiss()
        self.on_enter()
        self.manager.current = "UserPostScreen"

    def remove_story(self, post):
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
        self.manager.current = "UserPostScreen"

    def callback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "SuccessScreen"


class PlantSearch(Screen):
    # self.camera = Camera(resolution=(640, 480), play=False, permission='camera')

    def capture(self):
        if self.camera.texture:
            self.camera.export_to_png("search.png")

    def callback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "MenuScreen"


class Bonfire(MDApp):
    database = mysql.connector.Connect(host="localhost",
                                       user="root",
                                       password="",
                                       database="bonfire_tips_db")
    cursor = database.cursor()

    def build(self):
        # window icon
        self.icon = "piedmont.png"

        Builder.load_file("tips.kv")

        screen_manager = ScreenManager()
        screen_manager.add_widget(LoginScreen(name='LoginScreen'))
        screen_manager.add_widget(SuccessScreen(name='SuccessScreen'))
        screen_manager.add_widget(SignupScreen(name='SignupScreen'))
        screen_manager.add_widget(ForgotPasswordScreen(name='ForgotPasswordScreen'))
        screen_manager.add_widget(MenuScreen(name='MenuScreen'))
        screen_manager.add_widget(ViewMtPostScreen(name='ViewMtPostScreen'))
        screen_manager.add_widget(AddMtPostScreen(name='AddMtPostScreen'))
        screen_manager.add_widget(ViewPtPostScreen(name='ViewPtPostScreen'))
        screen_manager.add_widget(AddPtPostScreen(name='AddPtPostScreen'))
        screen_manager.add_widget(ViewCtPostScreen(name='ViewCtPostScreen'))
        screen_manager.add_widget(AddCtPostScreen(name='AddCtPostScreen'))
        screen_manager.add_widget(UserPostScreen(name='UserPostScreen'))
        screen_manager.add_widget(MtCommentScreen(name='MtCommentScreen'))
        screen_manager.add_widget(WelcomeMtScreen(name='WelcomeMtScreen'))
        screen_manager.add_widget(WelcomePtScreen(name='WelcomePtScreen'))
        screen_manager.add_widget(WelcomeCtScreen(name='WelcomeCtScreen'))
        screen_manager.add_widget(AllTips(name='AllTips'))
        screen_manager.add_widget(MountainTips(name='MountainTips'))
        screen_manager.add_widget(PiedmontTips(name='PiedmontTips'))
        screen_manager.add_widget(CoastTips(name='CoastTips'))
        screen_manager.add_widget(PlantSearch(name='PlantSearch'))

        return screen_manager


if __name__ == '__main__':
    Bonfire().run()
