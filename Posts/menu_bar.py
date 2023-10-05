import mysql.connector
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.factory import Factory
from kivymd.uix.list import TwoLineListItem
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineIconListItem, MDList
from kivy.properties import ObjectProperty, StringProperty, ListProperty

Window.size = (350, 580)
KV = '''
<ItemDrawer>:
    theme_text_color: "Custom"
    on_release: self.parent.set_color_item(self)

    IconLeftWidget:
        id: icon
        icon: root.icon
        theme_text_color: "Custom"
        text_color: root.text_color

<ContentNavigationDrawer>:
    orientation: "vertical"
    padding: "8dp"
    spacing: "8dp"

    AnchorLayout:
        anchor_x: "left"
        size_hint_y: None
        height: avatar.height

        Image:
            id: avatar
            size_hint: None, None
            size: "56dp", "56dp"
            source: "img.png"

    MDLabel:
        text: "Bonfire Survival Guide"
        font_style: "Button"
        adaptive_height: True

    MDLabel:
        text: "Learn new survival tips around the Bonfire"
        font_style: "Caption"
        adaptive_height: True

    ScrollView:

        DrawerList:
            id: md_list

MDScreen:
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: "orange_gradient.png"
    MDNavigationLayout:
        ScreenManager:

            MDScreen:
                MDBoxLayout:

                    orientation: 'vertical'

                    MDTopAppBar:
                        md_bg_color: 0, 0, 0, 0.5
                        title: "Bonfire Stories"
                        specific_text_color: 227/255, 71/255, 16/255, 1
                        elevation: 10
                        left_action_items: [['menu', lambda x: nav_drawer.set_state("open")]]
                    MDFloatLayout:
                        MDRaisedButton:
                            md_bg_color: 0,0,0,0.5
                            size_hint: .6, .07
                            pos_hint: {"center_x": .5, "center_y": .4}
                            text: "Mountain Bonfire"
                            text_color: 227/255, 71/255, 16/255, 1

                        MDRaisedButton:
                            md_bg_color: 0,0,0,0.5
                            size_hint: .6, .07
                            pos_hint: {"center_x": .5, "center_y": .1}
                            text: "Piedmont Bonfire"
                            text_color: 227/255, 71/255, 16/255, 1

                        MDRaisedButton:
                            md_bg_color: 0,0,0,0.5
                            size_hint: .6, .07
                            pos_hint: {"center_x": .5, "center_y": -.2}
                            text: "Coastal Bonfire"
                            text_color: 227/255, 71/255, 16/255, 1
                    Widget:

        MDNavigationDrawer:
            id: nav_drawer

            ContentNavigationDrawer:
                id: content_drawer

'''


# class Content(BoxLayout):
#     manager = ObjectProperty()
#     nav_drawer = ObjectProperty()
class ContentNavigationDrawer(MDBoxLayout):
    pass


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))


class DrawerList(ThemableBehavior, MDList):
    pass
    # def set_color_item(self, instance_item):
    #     """Called when tap on a menu item."""
    #
    #     # Set the color of the icon and text for the menu item.
    #     for item in self.children:
    #         if item.text_color == self.theme_cls.primary_color:
    #             item.text_color = self.theme_cls.text_color
    #             break
    #     instance_item.text_color = self.theme_cls.primary_color


class ViewMtPosts(MDBoxLayout):
    pass


class TestNavigationDrawer(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        icons_item = {
            "book": "My Stories",
            "forest": "Mountain Bonfire",
            "campfire": "Piedmont Bonfire",
            "fish": "Coastal Bonfire",
            "plus": "Survival Tips",
            "lock": "Logout",
        }
        for icon_name in icons_item.keys():
            self.root.ids.content_drawer.ids.md_list.add_widget(
                ItemDrawer(icon=icon_name, text=icons_item[icon_name])
            )


if __name__ == "__main__":
    TestNavigationDrawer().run()