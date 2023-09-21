from kivy.core.text import LabelBase
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window

Window.size = (350,580)

kv = """
MDFloatLayout:
    md_bg_color: 0.996, 0.365, 0.149, 1  # Orange color in RGBA format
    Image:
        source: "logo.png"
        pos_hint: {"center_x": .5, "center_y": .70}
        size_hint: .5, .5

    MDFloatLayout:
        size_hint: .9 , .07
        pos_hint: {"center_x": .5, "center_y": .50}
        canvas:
            Color:
                rgb: 250/255, 250/255, 250/255, 1
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [4]
        canvas.before:
            Color:
                rgb: 217/255, 217/255, 217/255, 1
            Line:
                width:1.1
                rounded_rectangle: self.x, self.y, self.width, self.height, 4, 4, 4, 4,100
        TextInput:
            hint_text: "Username"
            size_hint: 1, None
            pos_hint: {"center_x": .5, "center_y": .5}
            height: self.minimum_height
            background_color: 1, 1, 1, 0
            font_size: "14sp"
            hint_text_color: 170/255, 170/255, 170/255, 1
            padding: 13
            cursor_color: 0, 0, 0, 1

    MDFloatLayout:
        size_hint: .9 , .07
        pos_hint: {"center_x": .5, "center_y": .41}
        canvas:
            Color:
                rgb: 250/255, 250/255, 250/255, 1
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [4]
        canvas.before:
            Color:
                rgb: 217/255, 217/255, 217/255, 1
            Line:
                width:1.1
                rounded_rectangle: self.x, self.y, self.width, self.height, 4, 4, 4, 4,100
        TextInput:
            hint_text: "New Password"
            size_hint: 1, None
            pos_hint: {"center_x": .5, "center_y": .5}
            height: self.minimum_height
            background_color: 1, 1, 1, 0
            font_size: "14sp"
            password: True
            hint_text_color: 170/255, 170/255, 170/255, 1
            padding: 13
            cursor_color: 0, 0, 0, 1

        Button:
            text: "Submit"
            size_hint: 1, 0.9
            pos_hint: {"center_x": 0.5, "center_y": -0.70}
            background_color: 128/255, 128/255, 128/255, 1
            font_size: "15sp"
            canvas.before:
                Color:
                    rgb: 154/255, 203/255, 247/255, 1
                RoundedRectangle:
                    size: self.size
                    pos: self.pos 
                    radius: [4]
                    
        MDTextButton:
            text: "Back To Login"
            pos_hint:{"center_x":0.5, "center_y": -3.5}
            font_size: "13sp"


            
"""

class Bonfire(MDApp):

    def build(self):
        return Builder.load_string(kv)

if __name__ == '__main__':
    Bonfire().run()
