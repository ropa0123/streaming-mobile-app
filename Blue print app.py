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
    news_url = ""
    def on_leave(self):
        self.ids.article_title.text = "Loading..."
        self.ids.article_content.text = "Fetching full story..."

# ---------- FULL PREMIUM KV UI ----------
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
            title: "Skyz Reader"
            left_action_items: [["arrow-left", lambda x: app.back_to_dashboard()]]
            md_bg_color: 0, 0, 0, 1
        
        ScrollView:
            do_scroll_x: False
            MDBoxLayout:
                orientation: 'vertical'
                adaptive_height: True
                padding: "20dp"
                spacing: "15dp"
                
                MDLabel:
                    id: article_title
                    text: "Loading..."
                    font_style: "H5"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: 0, 0.47, 1, 1
                    adaptive_height: True
                
                MDLabel:
                    id: article_content
                    text: "Fetching full story..."
                    font_style: "Body1"
                    theme_text_color: "Secondary"
                    adaptive_height: True
                
                MDRaisedButton:
                    text: "OPEN IN BROWSER"
                    pos_hint: {"center_x": .5}
                    on_release: import webbrowser; webbrowser.open(root.news_url)

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
            text: "SKY LOGIN"
            halign: "center"
            font_style: "H3"
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
            text: "Create Account"
            pos_hint: {"center_x": .5}
            on_release: root.manager.current = 'signup'

<SignupScreen>:
    name: 'signup'
    md_bg_color: 0.05, 0.05, 0.05, 1
    MDBoxLayout:
        orientation: 'vertical'
        padding: "40dp"
        spacing: "20dp"
        MDTextField:
            id: new_user
            hint_text: "Username"
            mode: "fill"
        MDTextField:
            id: new_pass
            hint_text: "Password"
            password: True
            mode: "fill"
        MDRaisedButton:
            text: "SIGN UP"
            size_hint_x: 1
            on_release: app.register_user(new_user.text, new_pass.text)

<DashboardScreen>:
    name: 'dashboard'
    MDNavigationLayout:
        MDScreenManager:
            MDScreen:
                MDBoxLayout:
                    orientation: 'vertical'
                    md_bg_color: 0, 0, 0, 1
                    
                    MDTopAppBar:
                        title: "Skyz Metro FM"
                        md_bg_color: 0, 0, 0, 1
                        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                    
                    MDBottomNavigation:
                        id: nav_bar
                        panel_color: 0.05, 0.05, 0.05, 1
                        
                        MDBottomNavigationItem:
                            name: 'live'
                            text: 'Live'
                            icon: 'play-circle'
                            RelativeLayout:
                                Image:
                                    source: 'Skyz Metro Logo.jpg'
                                    allow_stretch: True
                                    keep_ratio: False
                                MDCard:
                                    size_hint: None, None
                                    size: "280dp", "380dp"
                                    pos_hint: {"center_x": .5, "center_y": .5}
                                    radius: 20
                                    md_bg_color: 0, 0, 0, 0.7
                                    elevation: 4
                                    padding: "20dp"
                                    MDBoxLayout:
                                        orientation: 'vertical'
                                        spacing: "15dp"
                                        Image:
                                            source: 'Skyz Metro Logo.jpg'
                                            size_hint_y: None
                                            height: "140dp"
                                        MDIcon:
                                            id: live_icon
                                            icon: "radio-tower"
                                            font_size: "60sp"
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
                                spacing: "10dp"
                                MDIconButton:
                                    icon: "refresh"
                                    pos_hint: {"right": 1}
                                    on_release: app.fetch_news()
                                ScrollView:
                                    MDGridLayout:
                                        id: news_list
                                        cols: 1
                                        adaptive_height: True
                                        spacing: "12dp"

                        MDBottomNavigationItem:
                            name: 'events'
                            text: 'Events'
                            icon: 'calendar-star'
                            MDBoxLayout:
                                orientation: 'vertical'
                                padding: "10dp"
                                ScrollView:
                                    MDList:
                                        id: event_list

                        MDBottomNavigationItem:
                            name: 'chat'
                            text: 'Chat'
                            icon: 'whatsapp'
                            MDBoxLayout:
                                orientation: 'vertical'
                                padding: "30dp"
                                MDTextField:
                                    id: wa_message
                                    hint_text: "Message the Studio..."
                                    mode: "rectangle"
                                    multiline: True
                                MDRaisedButton:
                                    text: "SEND TO SKYZ"
                                    pos_hint: {"center_x": .5}
                                    on_release: app.whatsapp_contact(wa_message.text)
                                Widget:

        MDNavigationDrawer:
            id: nav_drawer
            radius: (0, 16, 16, 0)
            MDNavigationDrawerMenu:
                MDNavigationDrawerHeader:
                    title: "Skyz Metro Menu"
                    text: "Bulawayo's Number One"
                MDNavigationDrawerItem:
                    icon: "calendar-clock"
                    text: "Program Schedule"
                    on_release: app.drawer_click("Schedule Coming Soon")
                MDNavigationDrawerItem:
                    icon: "microphone"
                    text: "Podcasts"
                    on_release: app.drawer_click("Podcasts Loading...")
                MDNavigationDrawerDivider:
                MDNavigationDrawerLabel:
                    text: "Tech Hub Solutions"
                MDNavigationDrawerItem:
                    icon: "tools"
                    text: "Book Tech Support"
                    on_release: app.whatsapp_contact("I need Tech Support for...")
                MDNavigationDrawerItem:
                    icon: "logout"
                    text: "Logout"
                    on_release: app.logout()
'''

class TechHubApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
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
        self.root.get_screen('dashboard').ids.nav_drawer.set_state("close")

    def toggle_stream(self):
        url = "https://stream.zeno.fm/2634b6n4qy8uv"
        btn = self.root.get_screen('dashboard').ids.stream_btn
        icon = self.root.get_screen('dashboard').ids.live_icon
        if self.player is None:
            try:
                self.player = MediaPlayer(url)
                btn.text = "STOP LISTENING"
                icon.text_color = [0, 1, 0, 1]
            except: toast("Stream Error")
        else:
            self.stop_stream()

    def stop_stream(self):
        if self.player: self.player.close_player(); self.player = None
        btn = self.root.get_screen('dashboard').ids.stream_btn
        icon = self.root.get_screen('dashboard').ids.live_icon
        btn.text = "START LISTENING"
        icon.text_color = [0, 0.47, 1, 1]

    def fetch_news(self):
        toast("Fetching headlines...")
        UrlRequest("https://skyzmetroradio.co.zw/", on_success=self.parse_news)

    def parse_news(self, request, result):
        soup = BeautifulSoup(result, 'html.parser')
        container = self.root.get_screen('dashboard').ids.news_list
        container.clear_widgets()
        for item in soup.find_all('h3', limit=8):
            title = item.get_text().strip()
            link = item.find('a')['href'] if item.find('a') else "https://skyzmetroradio.co.zw/"
            card = MDCard(
                orientation='vertical', padding="12dp", size_hint_y=None, height="100dp",
                radius=12, md_bg_color=(0.1, 0.1, 0.1, 1), ripple_behavior=True,
                on_release=lambda x, l=link: self.open_news(l)
            )
            card.add_widget(MDLabel(text=title, font_style="Subtitle1", bold=True))
            container.add_widget(card)

    def open_news(self, url):
        self.root.get_screen('news_reader').news_url = url
        self.root.current = 'news_reader'
        UrlRequest(url, on_success=self.parse_article_body)

    def parse_article_body(self, request, result):
        soup = BeautifulSoup(result, 'html.parser')
        # Improved targeting for WordPress/Newspaper themes
        title_tag = soup.find('h1') or soup.find('h2', {'class': 'entry-title'})
        content_div = (
            soup.find('div', {'class': 'entry-content'}) or 
            soup.find('div', {'class': 'td-post-content'}) or
            soup.find('article') or
            soup.find('div', {'id': 'content'})
        )
        
        reader = self.root.get_screen('news_reader')
        if title_tag: 
            reader.ids.article_title.text = title_tag.get_text().strip()
            
        if content_div:
            paragraphs = content_div.find_all('p')
            clean_text = [p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 15]
            if clean_text:
                reader.ids.article_content.text = "\n\n".join(clean_text)
            else:
                # Fallback to direct text grab if <p> tags are missing
                reader.ids.article_content.text = content_div.get_text(separator="\n", strip=True)
        else:
            reader.ids.article_content.text = "Text view not available for this format. Please read on the main website."

    def load_events(self):
        container = self.root.get_screen('dashboard').ids.event_list
        container.clear_widgets()
        events = [("Skyz Metro Live Events", "facebook"), ("Tech Hub Workshops", "tools")]
        for name, icon in events:
            item = OneLineIconListItem(text=name)
            item.add_widget(IconLeftWidget(icon=icon))
            container.add_widget(item)

    def whatsapp_contact(self, msg):
        webbrowser.open(f"https://wa.me/263774460100?text={urllib.parse.quote(msg or 'Hi!')}")

    def drawer_click(self, text):
        toast(text); self.root.get_screen('dashboard').ids.nav_drawer.set_state("close")

    def check_login(self, u, p):
        if u in self.users and self.users[u] == hash_pass(p): self.root.current = 'dashboard'
        else: toast("Invalid Login")

    def register_user(self, u, p):
        if u and p:
            self.users[u] = hash_pass(p); save_users(self.users)
            toast("Created!"); self.root.current = 'login'

    def on_stop(self):
        if self.player: self.player.close_player()

if __name__ == "__main__":
    TechHubApp().run()