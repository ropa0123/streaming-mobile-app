import webbrowser
import urllib.parse
import hashlib
import json
import os
from bs4 import BeautifulSoup
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest
from ffpyplayer.player import MediaPlayer
from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivymd.uix.button import MDFillRoundFlatButton

# ---------- DATABASE ----------
DB_FILE = "users.json"

def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except:
            return {"admin": hash_pass("1234")}
    return {"admin": hash_pass("1234")}

def save_users(users):
    with open(DB_FILE, "w") as f:
        json.dump(users, f)

# ---------- SCREENS ----------
class SplashScreen(Screen): pass
class LoginScreen(Screen): pass
class SignupScreen(Screen): pass
class DashboardScreen(Screen): pass
class NewsReaderScreen(Screen):
    news_title = "Loading..."
    def on_enter(self):
        self.ids.reader_title.text = self.news_title

# ---------- KV UI DESIGN ----------
KV = '''
#:import FadeTransition kivy.uix.screenmanager.FadeTransition

ScreenManager:
    transition: FadeTransition()
    SplashScreen:
    LoginScreen:
    SignupScreen:
    DashboardScreen:
    NewsReaderScreen:

<NewsReaderScreen>:
    name: 'news_reader'
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.05, 0.05, 0.05, 1
        MDTopAppBar:
            title: "Article View"
            elevation: 0
            left_action_items: [["arrow-left", lambda x: app.back_to_dashboard()]]
            md_bg_color: 0.05, 0.05, 0.05, 1
        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                adaptive_height: True
                padding: "20dp"
                spacing: "15dp"
                MDLabel:
                    id: reader_title
                    text: ""
                    font_style: "H5"
                    bold: True
                MDSeparator:
                MDLabel:
                    text: "Full content loading from Skyz Metro servers..."
                    theme_text_color: "Secondary"

<SplashScreen>:
    name: 'splash'
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0, 0, 0, 1
        padding: "50dp"
        Image:
            source: 'Skyz Metro Logo2.png'
            size_hint: (0.5, 0.5)
            pos_hint: {"center_x": .5}

<LoginScreen>:
    name: 'login'
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.05, 0.05, 0.05, 1
        padding: "40dp"
        spacing: "20dp"
        Widget:
            size_hint_y: 0.1
        Image:
            source: 'Skyz Metro Logo2.png'
            size: ("150dp", "150dp")
            size_hint: (None, None)
            pos_hint: {"center_x": .5}
        MDLabel:
            text: "Skyz Metro FM"
            halign: "center"
            font_style: "H5"
            bold: True
        MDTextField:
            id: user_login
            hint_text: "Username"
            mode: "rectangle"
        MDTextField:
            id: pass_login
            hint_text: "Password"
            password: True
            mode: "rectangle"
        MDFillRoundFlatButton:
            text: "LOG IN"
            size_hint_x: 1
            md_bg_color: 0.11, 0.73, 0.33, 1
            on_release: app.check_login(user_login.text, pass_login.text)
        MDFlatButton:
            text: "CREATE ACCOUNT"
            pos_hint: {"center_x": .5}
            on_release: root.manager.current = 'signup'
        Widget:

<SignupScreen>:
    name: 'signup'
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.05, 0.05, 0.05, 1
        padding: "40dp"
        spacing: "20dp"
        MDTopAppBar:
            title: "Create Account"
            left_action_items: [["arrow-left", lambda x: app.logout()]]
            md_bg_color: 0.05, 0.05, 0.05, 1
            elevation: 0
        MDTextField:
            id: new_user
            hint_text: "Username"
            mode: "rectangle"
        MDTextField:
            id: new_pass
            hint_text: "Password"
            password: True
            mode: "rectangle"
        MDRaisedButton:
            text: "SIGN UP"
            size_hint_x: 1
            on_release: app.register_user(new_user.text, new_pass.text)
        Widget:

<DashboardScreen>:
    name: 'dashboard'
    md_bg_color: 0.05, 0.05, 0.05, 1

    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "Tech Hub Solutions"
            elevation: 0
            md_bg_color: 0.05, 0.05, 0.05, 1
            right_action_items: [["logout", lambda x: app.logout()]]

        MDBottomNavigation:
            panel_color: 0.08, 0.08, 0.08, 1
            text_color_active: 0.11, 0.73, 0.33, 1

            MDBottomNavigationItem:
                name: 'live'
                text: 'Home'
                icon: 'home-variant'
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: ["30dp", "10dp", "30dp", "30dp"]
                    spacing: "15dp"
                    MDCard:
                        size_hint: (1, 1)
                        radius: [25,]
                        elevation: 4
                        md_bg_color: 0.1, 0.1, 0.1, 1
                        FitImage:
                            source: 'Skyz Metro Logo2.png'
                            radius: [25,]
                    MDBoxLayout:
                        orientation: 'vertical'
                        adaptive_height: True
                        MDLabel:
                            text: "Skyz Metro FM"
                            font_style: "H4"
                            bold: True
                            halign: "center"
                        MDLabel:
                            text: "Bulawayo's Number One"
                            theme_text_color: "Secondary"
                            halign: "center"

                    MDBoxLayout:
                        orientation: 'horizontal'
                        adaptive_height: True
                        spacing: "10dp"
                        MDIcon:
                            icon: "volume-high"
                        MDSlider:
                            id: volume_slider
                            min: 0
                            max: 100
                            value: 80
                            on_value: app.adjust_volume(self.value)

                    MDIconButton:
                        id: stream_btn
                        icon: "play-circle"
                        user_font_size: "80sp"
                        pos_hint: {"center_x": .5}
                        theme_text_color: "Custom"
                        text_color: 0.11, 0.73, 0.33, 1
                        on_release: app.toggle_stream()

            MDBottomNavigationItem:
                name: 'news'
                text: 'News'
                icon: 'magnify'
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: "15dp"
                    spacing: "10dp"
                    MDLabel:
                        text: "Skyz Metro News"
                        font_style: "H5"
                        bold: True
                    ScrollView:
                        MDBoxLayout:
                            id: news_list
                            orientation: 'vertical'
                            adaptive_height: True
                            spacing: "10dp"

            MDBottomNavigationItem:
                name: 'events'
                text: 'Events'
                icon: 'calendar-star'
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: "20dp"
                    MDLabel:
                        text: "Upcoming Socials"
                        font_style: "H5"
                        bold: True
                    ScrollView:
                        MDList:
                            id: event_list

            MDBottomNavigationItem:
                name: 'contact'
                text: 'Chat'
                icon: 'message-text-outline'
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: "20dp"
                    spacing: "20dp"
                    MDLabel:
                        text: "Studio Chat"
                        font_style: "H5"
                        bold: True
                    MDTextField:
                        id: wa_message
                        hint_text: "Say something to the DJ..."
                        mode: "rectangle"
                        multiline: True
                    MDFillRoundFlatButton:
                        text: "SEND MESSAGE"
                        pos_hint: {"center_x": .5}
                        on_release: app.whatsapp_contact(wa_message.text)
                    Widget:
'''

class TechHubApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        self.users = load_users()
        self.player = None
        return Builder.load_string(KV)

    def on_start(self):
        Clock.schedule_once(self.switch_to_login, 2)
        self.fetch_news()
        self.load_events()

    def switch_to_login(self, *args):
        self.root.current = 'login'

    def back_to_dashboard(self):
        self.root.current = 'dashboard'

    def logout(self, *args):
        self.stop_stream()
        self.root.current = 'login'
        toast("Logged out successfully")

    def adjust_volume(self, value):
        if self.player:
            self.player.set_volume(value / 100.0)

    def toggle_stream(self):
        url = "https://stream.zeno.fm/2634b6n4qy8uv"
        btn = self.root.get_screen('dashboard').ids.stream_btn
        vol = self.root.get_screen('dashboard').ids.volume_slider.value
        if self.player is None:
            try:
                self.player = MediaPlayer(url)
                self.player.set_volume(vol / 100.0)
                btn.icon = "pause-circle"
            except:
                toast("Stream connection error")
        else:
            self.stop_stream()

    def stop_stream(self):
        if self.player:
            self.player.close_player()
            self.player = None
        try:
            self.root.get_screen('dashboard').ids.stream_btn.icon = "play-circle"
        except: pass

    def fetch_news(self):
        UrlRequest("https://skyzmetroradio.co.zw/", on_success=self.parse_news)

    def parse_news(self, request, result):
        soup = BeautifulSoup(result, 'html.parser')
        container = self.root.get_screen('dashboard').ids.news_list
        container.clear_widgets()
        articles = soup.find_all('h3', limit=10)
        for item in articles:
            title = item.get_text().strip()
            if title:
                card = MDCard(
                    orientation='vertical', padding="15dp", size_hint_y=None, height=dp(90),
                    radius=[15,], ripple_behavior=True, md_bg_color= [0.1, 0.1, 0.1, 1],
                    on_release=lambda x, t=title: self.open_news(t)
                )
                card.add_widget(MDLabel(text=title, font_style="Subtitle1", bold=True))
                container.add_widget(card)

    def open_news(self, title):
        reader = self.root.get_screen('news_reader')
        reader.news_title = title
        self.root.current = 'news_reader'

    def load_events(self):
        container = self.root.get_screen('dashboard').ids.event_list
        container.clear_widgets()
        links = [
            ("Instagram", "instagram", "https://www.instagram.com/skyzmetrofmbulawayo/"),
            ("Facebook", "facebook", "https://www.facebook.com/SkyzMetroFM/"),
            ("X (Twitter)", "twitter", "https://twitter.com/SkyzMetroFM")
        ]
        for name, icon, url in links:
            item = OneLineIconListItem(text=f"Follow us on {name}", on_release=lambda x, u=url: webbrowser.open(u))
            item.add_widget(IconLeftWidget(icon=icon))
            container.add_widget(item)

    def whatsapp_contact(self, message):
        msg = message if message else "Hi Skyz Metro!"
        webbrowser.open(f"https://wa.me/263774460100?text={urllib.parse.quote(msg)}")

    def check_login(self, u, p):
        if u in self.users and self.users[u] == hash_pass(p):
            self.root.current = 'dashboard'
        else:
            toast("Invalid credentials")

    def register_user(self, u, p):
        if u and p:
            self.users[u] = hash_pass(p)
            save_users(self.users)
            toast("Account created")
            self.root.current = 'login'

    def on_stop(self):
        if self.player: self.player.close_player()

if __name__ == "__main__":
    TechHubApp().run()