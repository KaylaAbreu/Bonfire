from kivy.uix.label import Label
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import OneLineRightIconListItem, ImageRightWidget, OneLineAvatarListItem, ImageLeftWidget
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar


class ViewCtPostScreen(MDScreen):
    def on_enter(self):
        story_app = MDApp.get_running_app()
        com_app = MDApp.get_running_app()

        story_app.cursor.execute("SELECT * FROM posts WHERE location = 'coast'")
        stories = story_app.cursor.fetchall()

        # Top Navigation Bar
        top_bar = (MDTopAppBar(title="Coastal Bonfire",
                               anchor_title="left",
                               left_action_items=[["home", lambda x: self.callback()]],
                               right_action_items=[["logout", lambda x: self.on_logout()]],
                               elevation=1,
                               md_bg_color=[248 / 255, 143 / 255, 70 / 255, 1],
                               specific_text_color=[44 / 255, 44 / 255, 44 / 255, 1],
                               pos_hint={"top": 1}

                               ))
        # Message Label
        message = Label(text="Check out what people are saying around the Bonfire",
                        pos_hint={"top": 0.85},  # places widget at top of parent
                        size_hint_y=None,
                        valign="top",
                        color=(0, 0, 0, 1),
                        size=(350, 100),  # Forces size of label
                        text_size=(500, None),  # Allows text to wrap
                        padding=(3, 3),
                        halign="center",
                        font_size='19sp'
                        )
        scroll = MDScrollView(size_hint=(1, 0.547),
                              pos_hint={"top": 0.7})  # size_hint adjusts the container size of the scroll

        layout2 = MDBoxLayout(orientation='vertical', size_hint_y=None, spacing=20)
        layout2.bind(minimum_height=layout2.setter('height'))  # Needed to dynamically add/delete from scrollview

        # Prevent repeats
        self.ids.float.clear_widgets()

        for i in stories:
            post_id = i[0]
            post_user = i[2]
            post_body = i[3]

            like_counter = self.get_like_count(post_id)
            dislike_counter = self.get_dislike_count(post_id)
            # Display user icon and username
            header = OneLineAvatarListItem(ImageLeftWidget(source="posts/img.png"),
                                           text=post_user,
                                           bg_color=(248 / 255, 143 / 255, 70 / 255, 1),
                                           )
            # post content
            label = Label(
                text=post_body,
                color=(0, 0, 0, 1),
                size_hint_y=None,
                size=(340, 200),
                text_size=(450, None),  # Allow text wrapping
                padding=(1, 1),
                halign="left",
                valign="top",
            )

            comment_btn = MDRectangleFlatButton(md_bg_color=(248 / 255, 143 / 255, 70 / 255, 0.5),
                                                text="Add Comment",
                                                text_color=(0, 0, 0, 1),
                                                size_hint_y=None,
                                                height=40,
                                                pos_hint={'center_x': 0.5, 'center_y': 0.1},
                                                on_release=(lambda instance, post_id=post_id,
                                                                   post_body=post_body: self.expand_story(post_id,
                                                                                                          post_body))
                                                )
            self.like_label = Label(
                text=f'{like_counter}',
                color=(0, 0, 0, 1),
                size=(20, 20),
                pos_hint={'center_x': 0.79, 'center_y': 1}
            )

            like = MDIconButton(icon="thumb-up",
                                on_release=lambda instance, post=post_id, label=self.like_label: self.like(post, label))

            self.dislike_label = Label(
                text=f'{dislike_counter}',
                color=(0, 0, 0, 1),
                size=(20, 20),
                pos_hint={'center_x': 0.93, 'center_y': 1}
            )
            dislike = MDIconButton(icon="thumb-down",
                                   on_release=lambda instance, post=post_id, label=self.dislike_label: self.dislike(
                                       post, label))

            layout = MDFloatLayout()
            layout1 = MDBoxLayout(orientation="horizontal", size_hint_y=None, spacing=0.5,
                                  md_bg_color=(248 / 255, 143 / 255, 70 / 255, 1),
                                  height=header.height
                                  )
            layout1.add_widget(header)
            layout1.add_widget(like)
            layout1.add_widget(dislike)

            layout.add_widget(self.like_label)
            layout.add_widget(self.dislike_label)

            com_app.cursor.execute("SELECT * FROM comments WHERE post_ID = %s", (post_id,))
            comments = com_app.cursor.fetchall()

            layout3 = MDBoxLayout(orientation='vertical', size_hint_y=None)
            layout3.bind(minimum_height=layout3.setter('height'))

            for c in comments:
                com_id = c[1]
                com_user = c[3]
                com_body = c[4]

                header2 = OneLineRightIconListItem(ImageRightWidget(source="posts/img.png"),
                                                   text=com_user,
                                                   bg_color=(248 / 255, 143 / 255, 70 / 255, 0.5))

                label2 = Label(
                    text=com_body,
                    size_hint_y=None,
                    color=(0, 0, 0, 1),
                    size=(300, 300),
                    text_size=(300, None),
                    padding=(5, 5),
                    halign="left",
                    valign="top"
                )

                layout3.add_widget(header2)
                layout3.add_widget(label2)

            layout2.add_widget(layout1)
            layout2.add_widget(layout)

            layout2.add_widget(label)
            layout2.add_widget(comment_btn)
            layout2.add_widget(layout3)

        scroll.add_widget(layout2)

        add_btn = MDRectangleFlatButton(md_bg_color=(248 / 255, 143 / 255, 70 / 255, 1),
                                        text="Share your story",
                                        text_color=(0, 0, 0, 1),
                                        pos_hint={'center_x': 0.5, 'center_y': 0.1},
                                        on_release=self.add_ct_story
                                        )
        # add everything to parent widget (Float Layout) in .kv file
        self.ids.float.add_widget(top_bar)
        self.ids.float.add_widget(message)
        self.ids.float.add_widget(scroll)
        self.ids.float.add_widget(add_btn)

    def get_like_count(self, post_id):
        app = MDApp.get_running_app()
        app.cursor.execute("SELECT likes from posts WHERE post_ID = %s", (post_id,))
        like_sum = app.cursor.fetchone()
        return like_sum[0] if like_sum else 0

    def get_dislike_count(self, post_id):
        app = MDApp.get_running_app()
        app.cursor.execute("SELECT dislikes from posts WHERE post_ID = %s", (post_id,))
        dislike_sum = app.cursor.fetchone()
        return dislike_sum[0] if dislike_sum else 0

    def like(self, post, label):
        like_counter = int(label.text)
        like_counter += 1

        app = MDApp.get_running_app()
        sql_command = "UPDATE posts SET likes = %s WHERE post_ID = %s"
        values = (like_counter, post)
        # Execute command
        app.cursor.execute(sql_command, values)
        # Commit changes to database
        app.database.commit()
        label.text = str(like_counter)
        self.on_enter()
        self.manager.current = "ViewCtPostScreen"

    def dislike(self, post, label):
        dislike_counter = int(label.text)
        dislike_counter += 1

        app = MDApp.get_running_app()
        sql_command = "UPDATE posts SET dislikes = %s WHERE post_ID = %s"
        values = (dislike_counter, post)
        # Execute command
        app.cursor.execute(sql_command, values)
        # Commit changes to database
        app.database.commit()
        label.text = str(dislike_counter)
        self.on_enter()
        self.manager.current = "ViewCtPostScreen"

    def add_ct_story(self, touch):
        print("add story")
        self.manager.current = "AddCtPostScreen"

    def expand_story(self, post_id, post_body):
        self.dialog = MDDialog(text=f'Story: {post_body}',
                               buttons=[
                                   MDRectangleFlatButton(
                                       text="Add Comment",
                                       pos_hint={"center_x": 0.1, "center_y": 0.5},
                                       on_release=lambda instance, post_id=post_id: self.add_ct_comment(post_id)
                                   ),
                                   MDRectangleFlatButton(
                                       text="Cancel",
                                       pos_hint={"center_x": 0.6, "center_y": 0.5},
                                       on_release=lambda x: self.dialog.dismiss()
                                   )
                               ]
                               )
        self.dialog.open()

    def add_ct_comment(self, post_id):
        self.dialog.dismiss()
        self.manager.get_screen('CtCommentScreen').post_id = post_id
        self.manager.current = "CtCommentScreen"

    def callback(self):
        self.manager.transition.direction = "right"
        self.manager.current = "MenuScreen"

