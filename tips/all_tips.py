from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView


class AllTips(MDScreen):
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
        layout = MDBoxLayout(orientation='vertical', padding=(10, 10, 10, 10))

        #create label for scrollview
        body_label=MDLabel(text=tip_content, size_hint_y=None, markup=True, valign="top", padding=(10,20))
        body_label.theme_text_color = "Custom"
        body_label.text_color = (250/255, 237/255, 202/255, 1 )
        body_label.bind(texture_size=body_label.setter('size'))


        #create scroll view
        body = MDScrollView(size_hint=(1, 1))
        body.add_widget(body_label)

        #add label to layout
        layout.add_widget(body)

        #create dismiss button
        dismiss_button = MDRectangleFlatButton(text="Dismiss",
                                on_press=self.dismiss_popup,
                                size_hint=(None, None),
                                size=(100, 50),
                                pos_hint={'center_x': 0.5, 'y': 0.10})

        layout.add_widget(dismiss_button)

        float_layout = MDFloatLayout(size=(Window.width - 10, Window.height - 10))
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

    def on_logout(self):
        login_screen = self.manager.get_screen('LoginScreen')
        login_screen.ids.username.text = ""
        login_screen.ids.password.text = ""
        login_screen.ids.error_label.text = ""
        self.manager.current = 'LoginScreen'