from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen


class AdminScreen(MDScreen):

    def view_users(self):
        # Gets users from database
        users = self.get_users_from_database()

        # Switches to the ViewUsersScreen and passes the list of users
        view_users_screen = self.manager.get_screen('ViewUsersScreen')
        view_users_screen.display_users(users)
        self.manager.current = 'ViewUsersScreen'

    def get_users_from_database(self):
        # Accesses running Kivy app
        app = MDApp.get_running_app()

        # SQL query to fetch username from login table
        query = "SELECT username FROM login"
        app.cursor.execute(query)

        # Get usernames from query
        users = [user[0] for user in app.cursor.fetchall()]

        # Display users
        self.manager.get_screen('ViewUsersScreen').display_users(users)
        return users

    def view_posts_tips(self):
        # Switches to AdminDashScreen so admin can view posts and tips
        self.manager.current = 'AdminDashScreen'

    def get_posts_from_database(self):
        # Accesses running Kivy app
        app = MDApp.get_running_app()

        # SQL query to fetch username, content, and location from posts table
        query = "SELECT username, content, location FROM posts"
        app.cursor.execute(query)

        # Takes all the posts from the query
        posts = app.cursor.fetchall()
        return posts

    def on_logout(self):
        # Switches to LoginScreen and erases any leftover content for username, password, and error text
        login_screen = self.manager.get_screen('LoginScreen')
        login_screen.ids.username.text = ""
        login_screen.ids.password.text = ""
        login_screen.ids.error_label.text = ""
        self.manager.current = 'LoginScreen'
