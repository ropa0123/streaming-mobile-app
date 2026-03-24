from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
import webbrowser
import urllib.parse
import requests

# --- KV Design Language (The Layout) ---
# NOTE: Ensure there are NO extra spaces at the start of lines in this string.
KV = '''
ScreenManager:
    LoginScreen:
    SignupScreen:
    DashboardScreen:

<LoginScreen>:
    name: 'login'
    MDBoxLayout:
        orientation: 'vertical'
        padding: "20dp"
        spacing: "15dp"
        MDLabel:
            text: "TECH HUB RADIO"
            halign: "center"
            font_style: "H4"
        MDTextField:
            id: user_login
            hint_text: "Username"
            mode: "rectangle"
        MDTextField:
            id: pass_login
            hint_text: "Password"
            password: True
            mode: "rectangle"
        MDRaisedButton:
            text: "LOGIN"
            pos_hint: {"center_x": .5}
            on_release: app.check_login(user_login.text, pass_login.text)
        MDFlatButton:
            text: "Create Account"
            pos_hint: {"center_x": .5}
            on_release: root.manager.current = 'signup'

<SignupScreen>:
    name: 'signup'
    MDBoxLayout:
        orientation: 'vertical'
        padding: "20dp"
        spacing: "15dp"
        MDLabel:
            text: "SIGN UP"
            halign: "center"
            font_style: "H5"
        MDTextField:
            id: new_user
            hint_text: "Choose Username"
        MDTextField:
            id: new_pass
            hint_text: "Choose Password"
            password: True
        MDRaisedButton:
            text: "REGISTER"
            pos_hint: {"center_x": .5}
            on_release: app.register_user(new_user.text, new_pass.text)
        MDFlatButton:
            text: "Back to Login"
            pos_hint: {"center_x": .5}
            on_release: root.manager.current = 'login'

<DashboardScreen>:
    name: 'dashboard'
    MDBoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Tech Hub Dashboard"
            right_action_items: [["logout", lambda x: app.logout()]]
        
        MDBottomNavigation:
            # TAB 1: PROFILE
            MDBottomNavigationItem:
                name: 'profile'
                text: 'User'
                icon: 'account'
                MDLabel:
                    id: welcome_text
                    text: "Welcome to Tech Hub"
                    halign: "center"

            # TAB 2: LIVE STREAM
            MDBottomNavigationItem:
                name: 'live'
                text: 'Live'
                icon: 'radio'
                MDRaisedButton:
                    text: "LISTEN LIVE"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    on_release: app.open_stream()

            # TAB 3: NEWS (Your API Feature)
            MDBottomNavigationItem:
                name: 'news'
                text: 'News'
                icon: 'newspaper'
                MDBoxLayout:
                    orientation: 'vertical'
                    padding: "10dp"
                    MDRaisedButton:
                        text: "Load Tech News"
                        on_release: app.fetch_news()
                    MDLabel:
                        id: news_display
                        text: "Headlines will load here..."
                        halign: "center"

            # TAB 4: EVENTS
            MDBottomNavigationItem:
                name: 'events'
                text: 'Events'
                icon: 'calendar'
                MDLabel:
                    text: "Oct 25: Radio Auction\\nNov 02: Code Workshop"
                    halign: "center"

            # TAB 5: CONTACT (Your WhatsApp Feature)
            MDBottomNavigationItem:
                name: 'contact'
                text: 'Contact'
                icon: 'whatsapp'
                MDRaisedButton:
                    text: "WhatsApp the DJ"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    on_release: app.whatsapp_contact()
'''

class LoginScreen(Screen): pass
class SignupScreen(Screen): pass
class DashboardScreen(Screen): pass

class TechHubApp(MDApp):
    # Database starts with your admin credentials
    users = {"admin": "1234"}

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        # Using a try block here catches syntax errors in your KV string
        try:
            return Builder.load_string(KV)
        except Exception as e:
            print(f"KV Syntax Error: {e}")

    # --- AUTH LOGIC ---
    def register_user(self, u, p):
        if u and p:
            self.users[u] = p
            self.root.current = 'login'

    def check_login(self, u, p):
        if u in self.users and self.users[u] == p:
            self.root.current = 'dashboard'
            # Update the welcome text after login
            self.root.get_screen('dashboard').ids.welcome_text.text = f"Logged in as: {u}"
        else:
            print("Login Failed")

    def logout(self):
        self.root.current = 'login'

    # --- LIVE STREAM ---
    def open_stream(self):
        webbrowser.open("https://stream.zeno.fm/2634b6n4qy8uv")

    # --- NEWS API (Restored) ---
    def fetch_news(self):
        api_key = "721f0f277845475b8d5b5b0ecf40bebc"
        url = f"https://newsapi.org/v2/top-headlines?category=technology&language=en&apiKey={api_key}"
        try:
            r = requests.get(url, timeout=5)
            data = r.json()
            # Extract first 3 headlines
            titles = [f"• {art['title']}" for art in data['articles'][:3]]
            self.root.get_screen('dashboard').ids.news_display.text = "\\n\\n".join(titles)
        except Exception as e:
            self.root.get_screen('dashboard').ids.news_display.text = "Error: Check Internet Connection"

    # --- WHATSAPP (Restored) ---
    def whatsapp_contact(self):
        station_number = "0774460100"
        text = urllib.parse.quote("Hi DJ! I'm messaging from the Tech Hub Radio App.")
        webbrowser.open(f"https://wa.me/{station_number}?text={text}")

if __name__ == '__main__':
    TechHubApp().run()