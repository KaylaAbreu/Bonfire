from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen


class AdminScreen(MDScreen):

    def view_users(self):
        users = self.get_users_from_database()

        # Switch to the ViewUsersScreen and pass the list of users
        view_users_screen = self.manager.get_screen('ViewUsersScreen')
        view_users_screen.display_users(users)
        self.manager.current = 'ViewUsersScreen'

    def get_users_from_database(self):
        app = MDApp.get_running_app()
        query = "SELECT username FROM login"
        app.cursor.execute(query)
        users = [user[0] for user in app.cursor.fetchall()]
        self.manager.get_screen('ViewUsersScreen').display_users(users)
        return users

    def view_posts_tips(self):
        self.manager.current = 'AdminDashScreen'

    def get_posts_from_database(self):
        app = MDApp.get_running_app()
        query = "SELECT username, content, location FROM posts"
        app.cursor.execute(query)
        posts = app.cursor.fetchall()
        return posts

    def on_logout(self):
        login_screen = self.manager.get_screen('LoginScreen')
        login_screen.ids.username.text = ""
        login_screen.ids.password.text = ""
        login_screen.ids.error_label.text = ""
        self.manager.current = 'LoginScreen'
