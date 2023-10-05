import mysql.connector
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window

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
            database="bonfire_db"
        )
        # Create cursor
        c = db_connect.cursor()

        # Add record to database
        sql_command = "INSERT INTO posts (post_body) VALUES (%s)"
        values = (self.root.ids.post_input.text,)

        #Execute command
        c.execute(sql_command, values)

        #TODO check for empty post
        # post = self.root.ids.post_input.text
        self.root.ids.post_label.text = f'{self.root.ids.post_input.text}'

        # Clear input box
        self.root.ids.post_input.text = ''

        #Commit changes to database
        db_connect.commit()

        db_connect.close()


    # View all posts
    def show_posts(self):
        db_connect = mysql.connector.connect(
            user="root",
            password="",
            host="localhost",
            database="bonfire_db"
        )
        # Create cursor
        c = db_connect.cursor()

        # Get records from database
        c.execute("SELECT * FROM posts")
        records = c.fetchall()

        post = ''
        for record in records:
            post = f'{post}\n{record[1]}'
            self.root.ids.post_label.text = f'{post}'

        db_connect.close()


if __name__ == "__main__":
    Bonfire().run()




