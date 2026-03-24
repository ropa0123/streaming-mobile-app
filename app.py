import webbrowser
import urllib.parse
import hashlib
import json
import os
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition # Python Import
from kivy.core.audio import SoundLoader 
from kivy.clock import Clock 
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget

# ---------- DATABASE LOGIC ----------
DB_FILE = "users.json"

def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {"admin": hash_pass("1234")}

def save_users(users):
    with open(DB_FILE, "w") as f:
        json.dump(users, f)

# ---------- SCREEN CLASSES ----------
class SplashScreen(Screen):
    pass

class LoginScreen(Screen):
    pass

class SignupScreen(Screen):
    pass

class DashboardScreen(Screen):
    pass

# ---------- PREMIUM KV UI ----------
# Note the #:import line at the top—this fixes your NameError
KV = '''
#:import FadeTransition kivy.uix.screenmanager.FadeTransition

ScreenManager:
    transition: FadeTransition()
    SplashScreen:
    LoginScreen:
    SignupScreen:
    DashboardScreen:

<SplashScreen>:
    name: 'splash'
    md_bg_color: 0, 0, 0, 1
    MDBoxLayout:
        orientation: 'vertical'
        padding: "20dp"
        MDLabel:
            text: "TECH HUB SOLUTIONS"
            halign: "center"
            font_style: "H4"
            theme_text_color: "Custom"
            text_color: 0, 0.47, 1, 1
            bold: True
        MDLabel:
            text: "Innovation in Every Wave"
            halign: "center"
            font_style: "Subtitle2"
            theme_text_color: "Hint"
        MDProgressBar:
            type: "indeterminate"
            size_hint_x: .5
            pos_hint: {"center_x": .5}

<LoginScreen>:
    name: 'login'
    md_bg_color: 0.05, 0.05, 0.05, 1
    MDBoxLayout:
        orientation: 'vertical'
        padding: "40dp"
        spacing: "20dp"
        MDLabel:
            text: "TECH HUB"
            halign: "center"
            font_style: "H3"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            bold: True
        MDTextField:
            id: user_login
            hint_text: "Username"
            mode: "fill"
        MDTextField:
            id: pass_login
            hint_text: "Password"
            password: True
            mode: "fill"
        MDRaisedButton:
            text: "LOGIN"
            size_hint_x: 1
            on_release: app.check_login(user_login.text, pass_login.text)
        MDFlatButton:
            text: "Don't have an account? Sign Up"
            pos_hint: {"center_x": .5}
            on_release: root.manager.current = 'signup'

<SignupScreen>:
    name: 'signup'
    md_bg_color: 0.05, 0.05, 0.05, 1
    MDBoxLayout:
        orientation: 'vertical'
        padding: "40dp"
        spacing: "20dp"
        MDLabel:
            text: "JOIN THE HUB"
            halign: "center"
            font_style: "H4"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
        MDTextField:
            id: new_user
            hint_text: "Choose Username"
            mode: "fill"
        MDTextField:
            id: new_pass
            hint_text: "Choose Password"
            password: True
            mode: "fill"
        MDRaisedButton:
            text: "CREATE ACCOUNT"
            size_hint_x: 1
            on_release: app.register_user(new_user.text, new_pass.text)
        MDFlatButton:
            text: "Back to Login"
            pos_hint: {"center_x": .5}
            on_release: root.manager.current = 'login'

<DashboardScreen>:
    name: 'dashboard'
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.02, 0.02, 0.02, 1
        MDTopAppBar:
            title: "Tech Hub Solutions"
            elevation: 0
            md_bg_color: 0, 0, 0, 1
            right_action_items: [["logout", lambda x: app.logout()]]
        MDBottomNavigation:
            panel_color: 0.05, 0.05, 0.05, 1
            MDBottomNavigationItem:
                name: 'live'
                text: 'Live'
                icon: 'play-circle'
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: "20dp"
                    spacing: "15dp"
                    MDCard:
                        size_hint: None, None
                        size: "240dp", "240dp"
                        pos_hint: {"center_x": .5}
                        radius: 20
                        md_bg_color: 0.1, 0.1, 0.1, 1
                        MDIcon:
                            id: live_icon
                            icon: "radio-tower"
                            font_size: "80sp"
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: 0, 0.47, 1, 1
                    MDFillRoundFlatIconButton:
                        id: stream_btn
                        icon: "play"
                        text: "START LISTENING"
                        pos_hint: {"center_x": .5}
                        on_release: app.toggle_stream()
            MDBottomNavigationItem:
                name: 'news'
                text: 'News'
                icon: 'newspaper-variant'
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: "10dp"
                    ScrollView:
                        MDGridLayout:
                            id: news_list
                            cols: 1
                            adaptive_height: True
                            spacing: "12dp"
            MDBottomNavigationItem:
                name: 'events'
                text: 'Events'
                icon: 'instagram'
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: "10dp"
                    ScrollView:
                        MDList:
                            id: event_list
            MDBottomNavigationItem:
                name: 'contact'
                text: 'Chat'
                icon: 'whatsapp'
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: "30dp"
                    spacing: "20dp"
                    MDTextField:
                        id: wa_message
                        hint_text: "Message the Studio..."
                        mode: "rectangle"
                        multiline: True
                    MDRaisedButton:
                        text: "SEND"
                        icon: "whatsapp"
                        pos_hint: {"center_x": .5}
                        on_release: app.whatsapp_contact(wa_message.text)
'''

class TechHubApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.users = load_users()
        self.sound = None 
        return Builder.load_string(KV)

    def on_start(self):
        Clock.schedule_once(self.switch_to_login, 3)
        self.fetch_news()
        self.load_events()

    def switch_to_login(self, *args):
        self.root.current = 'login'

    def register_user(self, u, p):
        if not u or not p:
            toast("Fill all fields")
            return
        self.users[u] = hash_pass(p)
        save_users(self.users)
        toast("Account created!")
        self.root.current = 'login'

    def check_login(self, u, p):
        if u in self.users and self.users[u] == hash_pass(p):
            self.root.current = 'dashboard'
        else:
            toast("Invalid credentials")

    def logout(self):
        self.root.current = 'login'

    def toggle_stream(self):
        stream_url = "https://stream.zeno.fm/2634b6n4qy8uv"
        btn = self.root.get_screen('dashboard').ids.stream_btn
        icon = self.root.get_screen('dashboard').ids.live_icon

        if not self.sound:
            toast("Buffering...")
            self.sound = SoundLoader.load(stream_url)
            
        if not self.sound:
            toast("Error: Install ffpyplayer")
            return

        if self.sound.state == 'stop':
            self.sound.play()
            btn.text = "STOP LISTENING"
            btn.icon = "stop"
            icon.text_color = [0, 1, 0, 1]
        else:
            self.sound.stop()
            self.sound.unload()
            self.sound = None
            btn.text = "START LISTENING"
            btn.icon = "play"
            icon.text_color = [0, 0.47, 1, 1]

    def fetch_news(self):
        news_data = [{"title": "Tech Hub 2026", "desc": "Premium features unlocked."}]
        container = self.root.get_screen('dashboard').ids.news_list
        container.clear_widgets()
        for article in news_data:
            card = MDCard(orientation='vertical', padding="15dp", size_hint_y=None, height="110dp", md_bg_color=(0.1, 0.1, 0.1, 1), radius=15)
            card.add_widget(MDLabel(text=article["title"], font_style="Subtitle1", bold=True))
            card.add_widget(MDLabel(text=article["desc"], font_style="Caption", theme_text_color="Hint"))
            container.add_widget(card)

    def load_events(self):
        container = self.root.get_screen('dashboard').ids.event_list
        container.clear_widgets()
        item = OneLineIconListItem(text="Friday Night Live", on_release=lambda x: webbrowser.open("https://instagram.com/techhub"))
        item.add_widget(IconLeftWidget(icon="instagram"))
        container.add_widget(item)

    def whatsapp_contact(self, message):
        content = message if message else "Hi Tech Hub!"
        webbrowser.open(f"https://wa.me/263774460100?text={urllib.parse.quote(content)}")

    def on_stop(self):
        if self.sound:
            self.sound.stop()
            self.sound.unload()

if __name__ == '__main__':
    TechHubApp().run()