import base64
import random
import webbrowser

from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivy.uix.image import Image, AsyncImage
from kivymd.uix.list import MDList, OneLineAvatarListItem, ImageLeftWidget
import time
import requests
from kivymd.uix.toolbar import MDTopAppBar

import API_key
from kivy.utils import platform
from kivy.logger import Logger
import re
from urllib.parse import urlparse

from kivymd.uix.scrollview import MDScrollView
Window.size = (350,580)

Builder.load_file("plant_search2.kv")

class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mycamera = self.ids.camera
        self.myimage = Image()
        self.response = None
        # self.resultbox =self.ids.resultbox
        # self.mybox = self.ids.mybox

    def capture(self):
        timenow = time.strftime("%Y%m%d_%H%M%S")
        image_path = "myimage_{}.png".format(timenow)
        # Get photo
        self.mycamera.export_to_png(image_path)
        self.myimage.source = image_path

        # Call plant search
        self.plant_search(image_path)

    def plant_search(self, image_path):
        with open(image_path, "rb") as file:
            images = [base64.b64encode(file.read()).decode("ascii")]

        self.response = requests.post(
            "https://api.plant.id/v2/identify",
            json={
                "images": images,
                "modifiers": ["similar_images"],
                "plant_details": ["common_names", "url"],
            },
            headers={
                "Content-Type": "application/json",
                "Api-Key": API_key.API_key,
            }
        ).json()

        suggestions_content = ""
        for suggestion in self.response["suggestions"]:
            suggestions_content += f"Scientific Name: {suggestion['plant_name']}\n"
            suggestions_content += f"Common Name: {suggestion['plant_details']['common_names']}\n"
            suggestions_content += f"URL: {suggestion['plant_details']['url']}\n"
            suggestions_content += f"Match Probability: {suggestion['probability']}\n\n"
        self.show_suggestions_popup(suggestions_content)

    def show_suggestions_popup(self, suggestions_content):
        # create layout
        # layout = MDBoxLayout(orientation='vertical', padding=(10, 10, 10, 10))
        layout = MDBoxLayout(orientation='vertical')


        # create scroll view
        # body = MDScrollView(size_hint=(1, 1)) #was working
        body = MDScrollView(size_hint=(None, None), size=(Window.width-10, Window.height-150)) #works the best
        # body = MDScrollView(size_hint=(None, None), size=(self.width, self.height))
        # body.add_widget(body_label)

        # add label to layout
        # layout.add_widget(body)
        if self.response:
            suggestion_layout = MDBoxLayout(orientation='vertical', size_hint_y=None)
            total_height= 0
            for suggestion in self.response["suggestions"]:
                suggestions_content = (
                    f"Scientific Name: {suggestion['plant_name']}\n"
                    f"Common Name: {suggestion['plant_details']['common_names']}\n"
                    f"URL: {suggestion['plant_details']['url']}\n"
                    f"Match Probability: {suggestion['probability']}\n\n"
                )
                print(suggestions_content)
                body_label = MDLabel(
                    text=suggestions_content,
                    size_hint_y=None,
                    markup=True,
                    valign="top",
                    # valign="center",
                    # padding=(10, 20)
                )
                body_label.theme_text_color = "Custom"
                body_label.text_color = (250 / 255, 237 / 255, 202 / 255, 1)
                body_label.bind(texture_size=body_label.setter('size'))
                body_label.text = re.sub(r'(https?://\S+)', r'[ref=\1]\1[/ref]', body_label.text)
                body_label.bind(on_ref_press=self.on_url_click)
                # body.add_widget(body_label)
                total_height += body_label.height
                suggestion_layout.add_widget(body_label)

                similar_images = suggestion.get("similar_images", [])
                for similar_image in similar_images:
                    url = similar_image.get("url", "")
                    image_widget = AsyncImage(source=url, size_hint_y=None)
                    # image_widget = AsyncImage(source=url, size_hint_y=None, height=150)
                    # layout.add_widget(image_widget)
                    total_height += image_widget.height
                    suggestion_layout.add_widget(image_widget)
            suggestion_layout.height = total_height
            body.add_widget(suggestion_layout)
            layout.add_widget(body)
        # create dismiss button
        dismiss_button = MDRaisedButton(text="Dismiss",
                                on_press=self.dismiss_popup,
                                size_hint=(None, None),
                                size=(100, 50),
                                pos_hint={'center_x': 0.5, 'y': 0.10})

        layout.add_widget(dismiss_button)

        float_layout = MDFloatLayout(size=(Window.width - 10, Window.height - 10))
        float_layout.add_widget(layout)

        self.suggestion = Popup(title="Your plant might be...", content=float_layout,
                                size=(Window.width - 10, Window.height - 10),
                                auto_dismiss=True)
        self.suggestion.open()

    def on_url_click(self, instance, value):
        if platform == "android":
            import android
            android.open_url(value)
        else:
            Logger.info(f"URL clicked: {value}")
            webbrowser.open(value)
    def dismiss_popup(self, instance):
        if self.suggestion:
            self.suggestion.dismiss()  # Dismiss the Popup

class MyApp(MDApp):
    def build(self):
       return HomeScreen()

if __name__ == '__main__':
    MyApp().run()
