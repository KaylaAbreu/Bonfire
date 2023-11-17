from datetime import datetime

import mysql.connector
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.list import TwoLineListItem, ThreeLineAvatarIconListItem, IconRightWidget, IconLeftWidget, \
    ThreeLineListItem

Window.size = (350, 580)


class RootWidget(ScreenManager):
    pass

class AllTips(Screen):
    def on_enter(self):
        db_connect = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            # password="SoSweet.47",
            # database="bonfire_tips_db"
            database="bonfire"
        )
        # Create cursor
        c = db_connect.cursor()

        # Get all tips from database
        c.execute("SELECT * FROM tips")
        entries = c.fetchall()

        tips = ''
       # for i in entries:
       #     self.ids.show_all_tips.add_widget(
        #        ThreeLineListItem(text=f'{i[2]}',secondary_text=f'{i[3]}', tertiary_text=f'{i[3]}')
           # )

        db_connect.close()

    def all_tips(self):
        self.manager.current = 'allTips'

    def mountainTips(self):
        self.manager.current = 'mountainTips'

    def piedmontTips(self):
        self.manager.current = 'piedmontTips'

    def coastTips(self):
        self.manager.current = 'coastTips'

    def add_tip(self):
        self.manager.current = 'addTips'

        # View all tips


class MountainTips(Screen):

    def all_tips(self):
        self.manager.current = 'allTips'

    def mountainTips(self):
        self.manager.current = 'mountainTips'

    def piedmontTips(self):
        self.manager.current = 'piedmontTips'

    def coastTips(self):
        self.manager.current = 'coastTips'

    def add_tip(self):
        self.manager.current = 'addTips'

        # View mountain tips

    def show_mountain_tips(self):
        self.manager.current = ''
        db_connect = mysql.connector.connect(
            user="root",
            password="",
            # password="SoSweet.47",
            host="localhost",
            # database="bonfire_tips_db"
            database="bonfire"
        )
        # Create cursor
        c = db_connect.cursor()

        # Get entries from database
        c.execute("SELECT * FROM tips WHERE category = 'mountains'")
        entries = c.fetchall()

        # tips = ''
        #for entries in entries:
          #  tips = f'{tips}\n{entries[1]}'
          #  self.root.ids.show_mountain_tips.text = f'{tips}'

        db_connect.close()


class PiedmontTips(Screen):
    def all_tips(self):
        self.manager.current = 'allTips'

    def mountainTips(self):
        self.manager.current = 'mountainTips'

    def piedmontTips(self):
        self.manager.current = 'piedmontTips'

    def coastTips(self):
        self.manager.current = 'coastTips'

    def add_tip(self):
        self.manager.current = 'addTips'

    def show_piedmont_tips(self):
        self.manager.current = ''
        db_connect = mysql.connector.connect(
            user="root",
            password="",
            # password="SoSweet.47",
            host="localhost",
            # database="bonfire_tips_db"
            database="bonfire"
        )
        # Create cursor
        c = db_connect.cursor()

        # Get entries from database
        c.execute("SELECT * FROM tips WHERE category = 'piedmont'")
        entries = c.fetchall()

        # tips = ''
        #for entries in entries:
         #   tips = f'{tips}\n{entries[1]}'
          #  self.root.ids.show_cost_tips.text = f'{tips}'

        db_connect.close()


class CoastTips(Screen):
    def all_tips(self):
        self.manager.current = 'allTips'

    def mountainTips(self):
        self.manager.current = 'mountainTips'

    def piedmontTips(self):
        self.manager.current = 'piedmontTips'

    def add_tip(self):
        self.manager.current = 'addTips'

    def coastTips(self):
        self.manager.current = 'coastTips'

    def show_coast_tips(self):
        self.manager.current = ''
        db_connect = mysql.connector.connect(
            user="root",
            # password="SoSweet.47",
            password="",
            host="localhost",
            database="bonfire"
            # database="bonfire_tips_db"
        )
        # Create cursor
        c = db_connect.cursor()

        # Get entries from database
        c.execute("SELECT * FROM tips WHERE category = 'coast'")
        entries = c.fetchall()

        # tips = ''
       # for entries in entries:
        #    tips = f'{tips}\n{entries[1]}'
         #   self.root.ids.show_cost_tips.text = f'{tips}'

        db_connect.close()


class AddTips(Screen):
    def all_tips(self):
        self.manager.current = 'allTips'

    def mountainTips(self):
        self.manager.current = 'mountainTips'

    def piedmontTips(self):
        self.manager.current = 'piedmontTips'

    def coastTips(self):
        self.manager.current = 'coastTips'


class Bonfire(MDApp, ScreenManager):
    def build(self):  # construct app
        self.icon = "img.png"

        return Builder.load_file('tips.kv')

    # Add post
    # TODO Hide info

    def submit(self):
        # Connect to database
        db_connect = mysql.connector.connect(
            user="root",
            # password="SoSweet.47",
            password="",
            host="localhost",
            # database="bonfire_tips_db"
            database="bonfire"
        )
        # Create cursor
        c = db_connect.cursor()

        # Add tip to database
        sql_command = "INSERT INTO tips (title) VALUES (%s)"
        values = (self.root.ids.tips_title_input.text,)
        # Execute command
        c.execute(sql_command, values)

        sql_command = "INSERT INTO tips (content) VALUES (%s)"
        values = (self.root.ids.tips_content_input.text,)
        c.execute(sql_command, values)

        sql_command = "INSERT INTO tips (category) VALUES (%s)"
        values = (self.root.ids.tips_category_input.text,)
        c.execute(sql_command, values)

        # sql_command = "INSERT INTO tips (updated) VALUES (%s)"
        # values = (datetime.now(),)
        # c.execute(sql_command, values)

        # TODO check for empty tip entries
        # post = self.root.ids.tip_input.text
        self.root.ids.tips_title_label.text = f'{self.root.ids.tips_title_input.text}'
        self.root.ids.tips_content_label.text = f'{self.root.ids.tips_content_input.text}'
        self.root.ids.tips_categoy_label.text = f'{self.root.ids.tips_category_input.text}'

        # Clear input boxes
        self.root.ids.tips_title_input.text = ''
        self.root.ids.tips_content_input.text = ''
        self.root.ids.tips_category_input.text = ''

        # Commit changes to database
        db_connect.commit()

        db_connect.close()


if __name__ == "__main__":
    Bonfire().run()