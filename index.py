import time
import webbrowser
import requests
import urllib.parse

# --- Database ---
usernames = []
passwords = []
emails = []
phone_numbers = []

# --- Station Data ---
# Fixed the nested tuples so the loop unpacks them correctly
show_schedule = {
    "Monday": [("06:00-10:00", "Morning Drive"), ("10:00-12:00", "Tech Talk"), ("12:00-15:00", "Local News"), ("15:00-18:00", "Afternoon Vibes"), ("18:00-22:00", "Evening Mix")],
    "Tuesday": [("06:00-10:00", "Morning Drive"), ("10:00-12:00", "Tech Talk"), ("12:00-15:00", "Local News"), ("15:00-18:00", "Afternoon Vibes"), ("18:00-22:00", "Evening Mix")],
    "Wednesday": [("06:00-10:00", "Morning Drive"), ("10:00-12:00", "Tech Talk"), ("12:00-15:00", "Local News"), ("15:00-18:00", "Afternoon Vibes"), ("18:00-22:00", "Evening Mix")],
    "Thursday": [("06:00-10:00", "Morning Drive"), ("10:00-12:00", "Tech Talk"), ("12:00-15:00", "Local News"), ("15:00-18:00", "Afternoon Vibes"), ("18:00-22:00", "Evening Mix")],
    "Friday": [("06:00-10:00", "Morning Drive"), ("10:00-12:00", "Tech Talk"), ("12:00-15:00", "Local News"), ("15:00-18:00", "Afternoon Vibes"), ("18:00-22:00", "Evening Mix")],
    "Saturday": [("08:00-12:00", "Weekend Wakeup"), ("12:00-16:00", "Tech Showcase"), ("16:00-20:00", "Local Spotlight"), ("20:00-00:00", "Saturday Night Live")],
    "Sunday": [("08:00-12:00", "Weekend Wakeup"), ("12:00-16:00", "Tech Showcase"), ("16:00-20:00", "Local Spotlight"), ("20:00-00:00", "Sunday Night Chill")]
}

news_stories = [
    "Local Tech Hub expansion announced for 2026.",
    "New community park opening this Saturday!",
    "Local High School wins National Coding Championship."
]

upcoming_events = [
    {"date": "Oct 25", "event": "Annual Radio Charity Auction"},
    {"date": "Nov 02", "event": "Tech Hub Coding Workshop"},
    {"date": "Dec 12", "event": "Live Music in the Square"},
]

# --- Auth Functions ---

def signup():
    print("\n--- Sign Up for Tech Hub Radio ---")
    user = input("Create Username: ")
    if user in usernames:
        print("Username already taken!")
        return
    email = input("Enter Email: ")
    phone_number = int(input("Enter Phone Number (for WhatsApp contact): "))
    pwd = input("Create Password: ")
    
    usernames.append(user)
    emails.append(email)
    phone_numbers.append(phone_number)
    passwords.append(pwd)
    print("Account created successfully! You can now log in.")

def login():
    print("\n--- Login ---")
    user = input("Username: ")
    pwd = input("Password: ")
    
    if user in usernames:
        idx = usernames.index(user)
        if passwords[idx] == pwd:
            print(f"Login successful! Welcome back, {user}.")
            return user
        else:
            print("Incorrect password.")
    else:
        print("Username not found.")
    return None

def forgot_password():
    print("\n--- Forgot Password ---")
    email_check = input("Enter your registered email: ")
    if email_check in emails:
        idx = emails.index(email_check)
        print(f"Match found! The password for user '{usernames[idx]}' is: {passwords[idx]}")
    else:
        print("Email not found in our records.")


# --- Feature Functions ---

def view_news(): # Changed 'ef' to 'def'
    print("\n--- Latest Tech News ---")
    
    # The API key must be a string (wrapped in quotes)
    api_key = "721f0f277845475b8d5b5b0ecf40bebc" 
    url = f"https://newsapi.org/v2/top-headlines?category=technology&language=en&apiKey={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status() 
        
        data = response.json()
        articles = data.get("articles", [])

        if not articles:
            print("No news found at the moment.")
            return

        for i, story in enumerate(articles[:5], 1):
            title = story.get("title")
            source = story.get("source", {}).get("name")
            print(f"{i}. {title} (via {source})")
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")

def view_events():
    print("\n--- Upcoming Events ---")
    for item in upcoming_events:
        print(f"[{item['date']}] - {item['event']}")

def view_schedule():
    day = input("Enter day of the week: ").capitalize()
    if day in show_schedule:
        print(f"\n--- {day} Schedule ---")
        for time_slot, show in show_schedule[day]:
            print(f"[{time_slot}] - {show}")
    else:
        print("Schedule not found.")

def contact_form():
    print("\n--- Contact Tech Hub Radio via WhatsApp ---")
    name = input("Your Name: ")
    msg = input("Your Message/Request: ")
    
    # 1. The Radio Station's WhatsApp Number (Include country code, no '+')
    station_number = "0774460100" 
    
    # 2. Format the pre-filled message
    full_text = f"Hello Tech Hub Radio! My name is {name}. My message is: {msg}"
    
    # 3. Encode the text for a URL (replaces spaces with %20, etc.)
    encoded_msg = urllib.parse.quote(full_text)
    
    # 4. Create the WhatsApp 'Click to Chat' link
    whatsapp_url = f"https://wa.me/{station_number}?text={encoded_msg}"
    
    print("\nRedirecting you to WhatsApp...")
    time.sleep(1) # Brief pause for effect
    
    # 5. Open the browser/WhatsApp app
    webbrowser.open(whatsapp_url)
    
    print(f"Done! Please click 'Send' in WhatsApp to reach the DJ.")

def view_gallery():
    print("\n--- Gallery ---")
    print("This feature requires a GUI. View images at /tech-hub-radio/gallery")
# --- DASHBOARD ---

def run_dashboard(current_user):
    while True:
        print(f"\n--- Tech Hub Radio Dashboard (User: {current_user}) ---")
        print("1. View Profile      2. Listen Live       3. Read News")
        print("4. Upcoming Events   5. View Gallery      6. Show Schedule")
        print("7. Contact Us        8. Logout")
        
        cmd = input("\nSelect (1-8): ")

        if cmd == "1":
            print(f"\n[Profile] User: {current_user} | Listener Rank: Gold")
        elif cmd == "2":
            print("\nOpening Web Stream...")
            webbrowser.open("https://stream.zeno.fm/2634b6n4qy8uv") 
        elif cmd == "3":
            view_news()
        elif cmd == "4":
            view_events()
        elif cmd == "5":
            print("\n[Gallery] This feature requires a GUI. View images at /tech-hub-radio/gallery")
        elif cmd == "6":
            view_schedule()
        elif cmd == "7":
            contact_form()
        elif cmd == "8":
            print("Logging out... Goodbye!")
            break
        else:
            print("Invalid option.")

# --- MAIN PROGRAM LOOP ---

while True:
    print("\n==============================")
    print("   TECH HUB SOLUTIONS RADIO   ")
    print("==============================")
    print("1. Login")
    print("2. Sign Up")
    print("3. Forgot Password")
    print("4. Exit")
    
    choice = input("\nChoose an option: ")
    
    if choice == "1":
        active_user = login()
        if active_user:
            run_dashboard(active_user)
    elif choice == "2":
        signup()
    elif choice == "3":
        forgot_password()
    elif choice == "4":
        print("Exiting application. Stay tuned!")
        break
    else:
        print("Invalid choice, please try again.")