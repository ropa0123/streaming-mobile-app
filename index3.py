from flask import Flask, render_template, request, redirect, url_for, session
import requests
import urllib.parse

app = Flask(__name__)
app.secret_key = 'tech_hub_secret_key'

# --- Database ---
users = {"admin": "1234"}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        if user and pwd:
            users[user] = pwd
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        if user in users and users[user] == pwd:
            session['user'] = user
            return redirect(url_for('dashboard'))
        return "Invalid Credentials"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Fetch News for the Dashboard
    api_key = "721f0f277845475b8d5b5b0ecf40bebc"
    news_url = f"https://newsapi.org/v2/top-headlines?category=technology&language=en&apiKey={api_key}"
    articles = []
    try:
        r = requests.get(news_url, timeout=5)
        articles = r.json().get('articles', [])[:5]
    except:
        pass

    # WhatsApp Link
    station_number = "0774460100"
    msg = urllib.parse.quote("Hi Tech Hub Radio! I'm listening via the web app.")
    whatsapp_url = f"https://wa.me/{station_number}?text={msg}"

    return render_template('dashboard.html', user=session['user'], articles=articles, whatsapp_url=whatsapp_url)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)