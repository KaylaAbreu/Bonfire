from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang import Builder
from posts.mountains.welcome_mt import WelcomeMtScreen
from posts.mountains.view_mt_post import ViewMtPostScreen
from posts.mountains.add_mt_post import AddMtPostScreen
from posts.piedmont.add_pt_post import AddPtPostScreen
from posts.coast.add_ct_post import AddCtPostScreen
from posts.piedmont.view_pt_post import ViewPtPostScreen
from posts.coast.view_ct_post import ViewCtPostScreen
from posts.piedmont.welcome_pt import WelcomePtScreen
from posts.coast.welcome_ct import WelcomeCtScreen
from login.login import LoginScreen
from login.signup import SignupScreen
from login.forgot_password import ForgotPasswordScreen
from login.change_password import ChangePasswordScreen
from admin.admin import AdminScreen
from admin.view_users import ViewUsersScreen
from success import SuccessScreen
from menu_screen import MenuScreen
from posts.user_post import UserPostScreen
from tips.all_tips import AllTips
from tips.mt_tips import MountainTips
from tips.pt_tips import PiedmontTips
from tips.ct_tips import CoastTips
from admin.admin_dash import AdminDashScreen
from plant import PlantSearch
import mysql.connector


Window.size = (350, 580)


class MyScreenManager(ScreenManager):
    pass


class Bonfire(MDApp):
    database = mysql.connector.Connect(host="localhost", user="root", password="", database="bonfire")
    cursor = database.cursor()

    def build(self):
        Builder.load_file("main.kv")
        Builder.load_file("success.kv")
        Builder.load_file("menu_screen.kv")
        Builder.load_file("plant.kv")
        Builder.load_file("posts/mountains/welcome_mt.kv")
        Builder.load_file("posts/mountains/view_mt_post.kv")
        Builder.load_file("posts/mountains/add_mt_post.kv")
        Builder.load_file("posts/piedmont/add_pt_post.kv")
        Builder.load_file("posts/coast/add_ct_post.kv")
        Builder.load_file("posts/piedmont/view_pt_post.kv")
        Builder.load_file("posts/coast/view_ct_post.kv")
        Builder.load_file("posts/piedmont/welcome_pt.kv")
        Builder.load_file("posts/coast/welcome_ct.kv")
        Builder.load_file("posts/user_post.kv")
        Builder.load_file("login/login.kv")
        Builder.load_file("login/signup.kv")
        Builder.load_file("login/forgot_password.kv")
        Builder.load_file("login/change_password.kv")
        Builder.load_file("admin/admin.kv")
        Builder.load_file("admin/admin_dash.kv")
        Builder.load_file("admin/view_users.kv")
        Builder.load_file("tips/all_tips.kv")
        Builder.load_file("tips/mt_tips.kv")
        Builder.load_file("tips/pt_tips.kv")

        return MyScreenManager()


if __name__ == '__main__':
    Bonfire().run()
