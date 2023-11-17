from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.list import TwoLineListItem, ThreeLineListItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
from kivymd.uix.toolbar import MDTopAppBar


class UserPostScreen(MDScreen):
    def on_enter(self):
        app = MDApp.get_running_app()

        username = self.manager.get_screen('LoginScreen').current_user

        # Get stories from database
        if username == 'admin':
            self.title = "Delete Stories"
            # If the user is admin, get all posts without filtering by username
            sql_command = "SELECT * FROM posts"
            app.cursor.execute(sql_command)
            # Top Navigation Bar
            top_bar = (MDTopAppBar(title="User Stories",
                                   anchor_title="left",
                                   left_action_items=[["home", lambda x: self.callback()]],
                                   right_action_items=[["logout", lambda x: self.on_logout()]],
                                   elevation=1,
                                   md_bg_color=[248 / 255, 143 / 255, 70 / 255, 1],
                                   specific_text_color=[44 / 255, 44 / 255, 44 / 255, 1],
                                   pos_hint={"top": 1}

                                   ))
            message = MDLabel(text=f'Moderate User Stories',
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

        else:
            # If the user is not admin, get only their own posts
            self.title = "My Stories"
            sql_command = "SELECT * FROM posts JOIN login ON posts.user_ID = login.user_ID WHERE login.username = %s"
            app.cursor.execute(sql_command, (username,))
            # Top Navigation Bar
            top_bar = (MDTopAppBar(title="My Stories",
                                   anchor_title="left",
                                   left_action_items=[["home", lambda x: self.callback()]],
                                   right_action_items=[["logout", lambda x: self.on_logout()]],
                                   elevation=1,
                                   md_bg_color=[248 / 255, 143 / 255, 70 / 255, 1],
                                   specific_text_color=[44 / 255, 44 / 255, 44 / 255, 1],
                                   pos_hint={"top": 1}

                                   ))
            # Message Label
            message = MDLabel(text=f'{username}\'s Stories',
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

        stories = app.cursor.fetchall()

        scroll = MDScrollView(size_hint=(1, 0.547),
                              pos_hint={"top": 0.7})  # size_hint adjusts the container size of the scroll
        #
        layout2 = MDBoxLayout(orientation='vertical', size_hint_y=None, spacing=20)
        layout2.bind(minimum_height=layout2.setter('height'))  # Needed to dynamically add/delete from scrollview

        # Prevent repeats
        self.ids.float.clear_widgets()
        post_count = 0
        for i in stories:
            self.post_id = i[0]
            self.post_content = i[3]
            post_count += 1

            if username == 'admin':
                # If the user is admin, display a delete button for each post
                # delete_button = MDIconButton(icon="delete")
                # delete_button.bind(on_release=lambda instance, post=self.post_id: self.remove_story(post))
                # delete_button.del_id = self.post_id
                delete_button = MDIconButton(icon="delete",
                                             pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                             on_release=lambda instance, post=self.post_id: self.remove_story(post))
                delete_button.del_id = self.post_id
                # self.ids.float.add_widget(delete_button)
                ulist = ThreeLineListItem(
                    text=f'Story: {post_count}',
                    secondary_text=f'Username: {i[2]}',
                    tertiary_text=f'Location: {i[4]}',
                    bg_color=(248 / 255, 143 / 255, 70 / 255, 1),
                    pos_hint={'center_x': 0.5, 'center_y': 0.5},
                    height=delete_button.height

                )
                layout3 = MDBoxLayout(orientation="horizontal", size_hint_y=None, spacing=10,
                                      md_bg_color=(248 / 255, 143 / 255, 70 / 255, 1),
                                      height=ulist.height
                                      )
                ulist.post_id = self.post_id
                layout3.add_widget(ulist)
                layout3.add_widget(delete_button)
                # post content
                label = MDLabel(
                    text=self.post_content,
                    color=(0, 0, 0, 1),
                    size_hint_y=None,
                    size=(340, 200),
                    text_size=(450, None),  # Allow text wrapping
                    padding=(1, 1),
                    halign="left",
                    valign="top",
                )

                layout2.add_widget(layout3)
                layout2.add_widget(label)

            else:
                # If the user is not admin, display edit and delete buttons for their posts
                edit_button = MDIconButton(icon="pencil-outline",
                                           pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                           on_release=lambda instance, post=self.post_id: self.edit_story(post))
                edit_button.edit_id = self.post_id

                delete_button = MDIconButton(icon="delete",
                                             pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                             on_release=lambda instance, post=self.post_id: self.remove_story(post))
                delete_button.del_id = self.post_id

                ulist = TwoLineListItem(
                    text=f'Story: {post_count}',
                    secondary_text=f'Location: {i[4]}',
                    bg_color=(248 / 255, 143 / 255, 70 / 255, 1),
                    pos_hint={'center_x': 0.5, 'center_y': 0.5},
                    height=edit_button.height

                )
                layout3 = MDBoxLayout(orientation="horizontal", size_hint_y=None, spacing=10,
                                      md_bg_color=(248 / 255, 143 / 255, 70 / 255, 1),
                                      height=ulist.height
                                      )
                ulist.post_id = self.post_id
                layout3.add_widget(ulist)
                layout3.add_widget(edit_button)
                layout3.add_widget(delete_button)

                # post content
                label = MDLabel(
                    text=self.post_content,
                    color=(0, 0, 0, 1),
                    size_hint_y=None,
                    size=(340, 200),
                    text_size=(450, None),  # Allow text wrapping
                    padding=(1, 1),
                    halign="left",
                    valign="top",
                )

                layout2.add_widget(layout3)
                layout2.add_widget(label)

        scroll.add_widget(layout2)
        self.ids.float.add_widget(top_bar)
        self.ids.float.add_widget(message)
        self.ids.float.add_widget(scroll)

    def edit_story(self, post):
        self.new_content = MDTextField(multiline=True)
        self.dialog = MDDialog(title='Edit your story',
                               text=self.post_content,
                               type="custom",
                               content_cls=self.new_content,
                               buttons=[
                                   MDRectangleFlatButton(
                                       text="Save",
                                       on_release=lambda x: self.save_story(post))])
        self.dialog.open()

    def save_story(self, post):
        save_new_content = self.new_content.text

        app = MDApp.get_running_app()

        sql_command = "UPDATE posts SET content=%s WHERE post_id = %s"
        app.cursor.execute(sql_command, (save_new_content, post))
        app.database.commit()

        self.dialog.dismiss()
        self.on_enter()
        self.manager.current = "UserPostScreen"

    def remove_story(self, post):

        # If yes button is pressed in dialog box, item will be deleted
        def yes(instance):
            app = MDApp.get_running_app()

            sql_command = "DELETE FROM posts WHERE post_id = %s"
            app.cursor.execute(sql_command, (post,))
            app.database.commit()

            # remove ThreeLineListItem and Button
            remove_container = []
            for widget in self.ids.float.children:
                if hasattr(widget, 'post_id') and widget.post_id == post:
                    remove_container.append(widget)
                elif hasattr(widget, 'edit_id') and widget.edit_id == post:
                    remove_container.append(widget)
                elif hasattr(widget, 'del_id') and widget.del_id == post:
                    remove_container.append(widget)

            for widget in remove_container:
                # self.ids.user_story_container.remove_widget(widget)
                self.ids.float.remove_widget(widget)

            self.dialog.dismiss()
            self.on_enter()
            self.manager.current = "UserPostScreen"

        # If cancel button is pressed in dialog box, dialog box will close with no change

        def cancel(instance):
            self.dialog.dismiss()

        self.dialog = MDDialog(
            text='Are you sure you want to delete this post?',
            type="custom",
            buttons=[
                MDRectangleFlatButton(
                    text="Yes",
                    on_release=yes),
                MDRectangleFlatButton(
                    text="Cancel",
                    on_release=cancel)
            ])
        self.dialog.open()

    def callback(self):
        username = self.manager.get_screen('LoginScreen').current_user
        if username == 'admin':
            self.manager.transition.direction = "right"
            self.manager.current = "AdminScreen"
        else:
            self.manager.transition.direction = "right"
            self.manager.current = "MenuScreen"
    def on_logout(self):
        login_screen = self.manager.get_screen('LoginScreen')
        login_screen.ids.username.text = ""
        login_screen.ids.password.text = ""
        login_screen.ids.error_label.text = ""
        self.manager.current = 'LoginScreen'