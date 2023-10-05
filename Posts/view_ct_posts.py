import mysql.connector
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.factory import Factory
from kivymd.uix.list import TwoLineListItem
Window.size = (350,580)

class CoastPosts(MDApp):
    def build(self):  # construct app
        self.theme_cls.theme_style = "Dark"
        self.icon="img.png"

        return Builder.load_file('view_ct_posts.kv')

    def on_start(self):
        db_connect = mysql.connector.connect(
            user="root",
            password="",
            host="localhost",
            database="bonfire_db"
        )
        # Create cursor
        c = db_connect.cursor()

        # Get stories from database
        c.execute("SELECT * FROM coast_posts")
        stories = c.fetchall()

        for i in stories:
            self.root.ids.story_container.add_widget(TwoLineListItem(text = f'{i[2]}', secondary_text=f'{i[3]}'))

if __name__ == "__main__":
    CoastPosts().run()