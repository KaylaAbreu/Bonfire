import base64
import re
import time
import webbrowser
import requests
from kivy import Logger, platform
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image, AsyncImage
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window

import API_key

class PlantSearch(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.myimage = Image()
        self.response = None

    def capture(self):
        timenow = time.strftime("%Y%m%d_%H%M%S")
        image_path = "myimage_{}.png".format(timenow)
        # Get photo
        self.ids.camera.export_to_png(image_path)
        self.myimage.source = image_path

        # Call plant search
        self.plant_search(image_path)
    def plant_search(self, image_path):
        with open(image_path, "rb") as file:
            images = [base64.b64encode(file.read()).decode("ascii")]

        # dummy similar images for debugging

        # dummy_similar_images = [
        #     {"url": "https://hips.hearstapps.com/hmg-prod/images/close-up-of-tulips-blooming-in-field-royalty-free-image-1584131603.jpg?crop=1xw:0.89656xh;center,top&resize=1200:*"},
        #     {"url": "https://images.pexels.com/photos/931177/pexels-photo-931177.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"},
        # ]

        self.response = requests.post("https://api.plant.id/v2/identify",
            json={
                "images": images,
                "modifiers": ["similar_images"],
                "plant_details": ["common_names", "url"],
            },
            headers={
                "Content-Type": "application/json",
                "Api-Key": API_key.API_key,
            }).json()

        # dummy response for debugging

        # dummy_response_data = {
        #     "suggestions": [
        #         {
        #             "plant_name": "Dummy Plant 1",
        #             "plant_details": {
        #                 "common_names": "Dummy Common Name 1",
        #                 "url": "https://dummyplant1.com",
        #             },
        #             "probability": 0.85,
        #         },
        #         {
        #             "plant_name": "Dummy Plant 2",
        #             "plant_details": {
        #                 "common_names": "Dummy Common Name 2",
        #                 "url": "https://dummyplant2.com",
        #             },
        #             "probability": 0.75,
        #             "similar_images": dummy_similar_images,
        #         },
        #     ]
        # }
        # debugging

        # self.response = dummy_response_data

        suggestions_content = ""

        for suggestion in self.response["suggestions"]:
            print("plant name: ",suggestion["plant_name"])
            print("plant details: ",suggestion["plant_details"]["common_names"])
            print("url: ", suggestion["plant_details"]["url"])
            print("probability: ",  suggestion["probability"])

        self.show_suggestions_popup(suggestions_content)
    def show_suggestions_popup(self, suggestions_content):
        scroll_view = ScrollView(size_hint=(1, 1))
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=(0,10))

        for suggestion in self.response["suggestions"]:
            suggestions_content = (
                f"Scientific Name: {suggestion['plant_name']}\n"
                f"Common Name: {suggestion['plant_details']['common_names']}\n"
                f"URL: {suggestion['plant_details']['url']}\n"
                f"Match Probability: {suggestion['probability']}\n\n"
            )
            # create label for scrollview
            body_label = MDLabel(
                text=suggestions_content,
                size_hint_y=None,
                markup=True,
                valign="top",
                padding=(10, 20)
            )
            body_label.theme_text_color = "Custom"
            body_label.text_color = (250 / 255, 237 / 255, 202 / 255, 1)
            body_label.bind(texture_size=body_label.setter('size'))
            body_label.text = re.sub(r'(https?://\S+)', r'[ref=\1]\1[/ref]', body_label.text)
            body_label.bind(on_ref_press=self.on_url_click)
            layout.add_widget(body_label)

            similar_images = suggestion.get("similar_images", [])
            for similar_image in similar_images:
                url = similar_image.get("url", "")
                image_widget = AsyncImage(source=url, size_hint_y=None, height=150)
                layout.add_widget(image_widget)
        layout.bind(minimum_height=layout.setter('height'))
        scroll_view.add_widget(layout)


        # create dismiss button
        dismiss_button = Button(text="Dismiss",
                                on_press=self.dismiss_popup,
                                size_hint=(None, None),
                                size=(100, 50),
                                pos_hint={'center_x': 0.5, 'y': 0.10})



        float_layout = FloatLayout(size=(Window.width - 10, Window.height - 10))
        float_layout.add_widget(scroll_view)
        float_layout.add_widget(dismiss_button)

        self.fulltip = Popup(title="Your plant might be", content=float_layout, size=(Window.width - 10, Window.height - 10),
                             auto_dismiss=True)
        self.fulltip.open()

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

    def callback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "MenuScreen"

    def on_logout(self):
        # Switches to LoginScreen and erases any leftover content for username, password, and error text
        login_screen = self.manager.get_screen('LoginScreen')
        login_screen.ids.username.text = ""
        login_screen.ids.password.text = ""
        login_screen.ids.error_label.text = ""
        self.manager.current = 'LoginScreen'