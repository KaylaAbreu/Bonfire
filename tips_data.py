import mysql.connector
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from datetime import datetime

Window.size = (350,580)

class Bonfire(MDApp):
    def build(self):  # construct app
        self.icon="img.png"

        return Builder.load_file('post.kv')

    # Add post
    #TODO Hide info
    def submit(self):
        db_connect = mysql.connector.connect(
            user="root",
            password="",
            host="localhost",
            database="bonfire_tips_db"
        )
        # Create cursor
        c = db_connect.cursor()

        #create columns
        sql_command = "ALTER TABLE tips ADD title VARCHAR(200)"
        c.execute(sql_command)
        db_connect.commit()

        sql_command = "ALTER TABLE tips ADD content VARCHAR(100000)"
        c.execute(sql_command)
        db_connect.commit()

        sql_command = "ALTER TABLE tips ADD category VARCHAR(100)"
        c.execute(sql_command)
        db_connect.commit()

        sql_command = "ALTER TABLE tips ADD updated VARCHAR(100)"
        c.execute(sql_command)
        db_connect.commit()


        # Add info to database
        sql_command = "INSERT INTO tips (title) VALUES (%s)"
        values = (self.root.ids.tips_title_input.text,)
        #Execute command
        c.execute(sql_command, values)

        sql_command = "INSERT INTO tips (content) VALUES (%s)"
        values = (self.root.ids.tips_content_input.text,)
        c.execute(sql_command, values)

        sql_command = "INSERT INTO tips (category) VALUES (%s)"
        values = (self.root.ids.tips_category_input.text,)
        c.execute(sql_command, values)

        sql_command = "INSERT INTO tips (updated) VALUES (%s)"
        values = (datetime.now(),)
        c.execute(sql_command, values)
        

        #TODO check for empty tip entries
        # post = self.root.ids.tip_input.text
        self.root.ids.tips_title_label.text = f'{self.root.ids.tips_title_input.text}'
        self.root.ids.tips_content_label.text = f'{self.root.ids.tips_content_input.text}'
        self.root.ids.tips_categoy_label.text = f'{self.root.ids.tips_category_input.text}'



        # Clear input boxes
        self.root.ids.tips_title_input.text = ''
        self.root.ids.tips_content_input.text = ''
        self.root.ids.tips_category_input.text = ''

        #Commit changes to database
        db_connect.commit()
        db_connect.close()


    # View all tips
    def show_tips(self):
        db_connect = mysql.connector.connect(
            user="root",
            password="",
            host="localhost",
            database="bonfire_tips_db"
        )
        # Create cursor
        c = db_connect.cursor()

        # Get entries from database
        c.execute("SELECT * FROM tips")
        entries = c.fetchall()

        tips = ''
        for entries in entries:
            tips = f'{tips}\n{entries[1]}'
            self.root.ids.tips_label.text = f'{tips}'

        db_connect.close()


if __name__ == "__main__":
    Bonfire().run()
