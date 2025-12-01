import os, smtplib, traceback
from email.message import EmailMessage
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from dotenv import load_dotenv
from openai import OpenAI
import mysql.connector
from apscheduler.schedulers.background import BackgroundScheduler

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev")

load_dotenv(".env.example", override=True)
openai_api_key = os.getenv("My_Test_Key")
client = OpenAI(api_key=openai_api_key)

DB_CONFIG = {
    "host": os.getenv("DB_HOST","localhost"),
    "user": os.getenv("DB_USER","root"),
    "password": os.getenv("DB_PASS",""),
    "database": os.getenv("DB_NAME","emotavia"),
    "autocommit": True
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

def get_llm_response(prompt):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",  # Ensure you're using the right model
        messages=[
            {"role": "system", "content": "You are an AI assistant who is working as an emotional consultant for Project Emotavia where you will analyzing the responses of user prompts and providing up to the point responses with solutions to improve mental health only. Your task is to provide structured, actionable advice in response to user prompts related to emotional health. Always format your answers with a clear structure and numbered steps or bullet points. When someone shares an emotional concern, respond with empathy and provide practical steps for resolving the issue."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )
    return completion.choices[0].message.content

def get_llm_response2(prompt):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",  # Ensure you're using the right model
        messages=[
            {"role": "system", "content": "You are an AI assistant who is working as an emotional consultant for Project Emotavia where you will analyzing the responses of user prompts and providing one or two words only defining the overall mood of the provided user prompt. Only provide the words don't repond with any other phrases. If you are providing one word, then make sure the word starts with first letter uppercase. If you are providing two words, then include ampersand (&) symbol in between and make sure those two words having first letter uppercase."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )
    return completion.choices[0].message.content

def send_email(to_email, subject, body):
    try:
        SMTP_HOST = os.getenv("SMTP_HOST","smtp.gmail.com")
        SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
        SMTP_USER = os.getenv("SMTP_USER","")
        SMTP_PASS = os.getenv("SMTP_PASS","")
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = SMTP_USER
        msg["To"] = to_email
        msg.set_content(body, subtype="html")
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
            s.starttls()
            s.login(SMTP_USER, SMTP_PASS)
            s.send_message(msg)
        return True
    except Exception as e:
        print("Email error:", e)
        traceback.print_exc()
        return False

# Scheduler job: send morning check-ins between 7-9 to opted-in users
def morning_check_in_job():
    try:
        db = get_db()
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT id, name, email, username FROM users")
        rows = cur.fetchall()
        for u in rows:
            link = f"http://localhost:5000/"
            body = f"""
                <p>Dear {u['name']},</p>
                <p>Welcome to Project Emotavia!</p>
                <p>If you want to check your mood now, <a href="{link}">click here to check in.</a><br>
                   If you feel heavy or anxious, click the link immediately.</p>
                <p>Best Regards,<br>
                   Project Emotavia </p>
            """
            send_email(u['email'], "Project Emotavia", body)
        cur.close()
        db.close()
    except Exception as e:
        print("Error:", e)


# --- Routes ---

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/support')
def support():
    return render_template("support.html")

# Login Route
@app.route("/userlogin", methods=["GET", "POST"])
def userlogin():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check if user exists and password matches
        db = get_db()
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        db.close()

        if user and user["password"] == password:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("user_home"))
        else:
            flash("Invalid credentials. Please try again.", "danger")
            return redirect(url_for("userlogin"))

    return render_template("userlogin.html")

# Signup Route
@app.route("/usersignup", methods=["GET", "POST"])
def usersignup():
    if request.method == "POST":
        name = request.form["name"]
        gender = request.form["gender"]
        language = request.form["language"]
        phone = request.form["phone"]
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]

        # Check if username or email already exists
        db = get_db()
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE username = %s OR email = %s OR phone = %s", (username, email, phone))
        existing_user = cur.fetchone()
        cur.close()
        db.close()

        if existing_user:
            flash("Username, Phone no. or Email ID already exists!", "danger")
            return redirect(url_for("usersignup"))

        # Store the user directly with plaintext password
        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO users (name, gender, language, phone, email, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (name, gender, language, phone, email, username, password))
        db.commit()
        cur.close()
        db.close()

        scheduler = BackgroundScheduler()
        scheduler.add_job(morning_check_in_job)
        scheduler.start()
        flash("Account created successfully! You can now log in.", "success")
        return redirect(url_for("userlogin"))

    return render_template("usersignup.html")

# Dashboard Route (Logged-in user)
@app.route("/user_home")
def user_home():
    if "user_id" not in session:
        return redirect(url_for("userlogin"))
    return render_template("user_home.html", username=session.get("username"))

@app.route('/user_about')
def user_about():
    if "user_id" not in session:
        return redirect(url_for("userlogin"))
    return render_template("user_about.html", username=session.get("username"))

@app.route('/user_contact')
def user_contact():
    if "user_id" not in session:
        return redirect(url_for("userlogin"))
    return render_template("user_contact.html", username=session.get("username"))

@app.route('/user_support')
def user_support():
    if "user_id" not in session:
        return redirect(url_for("userlogin"))
    return render_template("user_support.html", username=session.get("username"))

@app.route('/check_mood')
def check_mood():
    if "user_id" not in session:
        return redirect(url_for("userlogin"))
    return render_template("check_mood.html", username=session.get("username"))

@app.route("/peer_support")
def peer_support():
    if "user_id" not in session:
        return redirect(url_for("userlogin"))
    category = request.args.get("category", "")
    user_name = session.get("username")
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT language, gender FROM users WHERE username = %s", (user_name,))
    language_gender = cur.fetchone()
    user_language = language_gender["language"].capitalize()
    user_gender = language_gender["gender"].capitalize()
    cur.close()
    db.close()
    return render_template("peer_support.html", language=user_language, gender=user_gender, category=category, username=session.get("username"))

@app.route('/user_ai')
def user_ai():
    if "user_id" not in session:
        return redirect(url_for("userlogin"))
    return render_template('user_ai.html', username=session.get("username"))

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['message']
    ai_response = get_llm_response(user_input)
    return jsonify({'response': ai_response})

@app.route('/ask2', methods=['POST'])
def ask2():
    user_input = request.form['message']
    ai_response = get_llm_response(user_input)
    return jsonify({'response': ai_response})

@app.route('/ask3', methods=['POST'])
def ask3():
    user_input = request.form['message']
    ai_response = get_llm_response(user_input)
    return jsonify({'response': ai_response})

@app.route('/mood_summary', methods=['POST'])
def mood_summary():
    text1 = request.form.get("q1", "")
    text2 = request.form.get("q2", "")
    text3 = request.form.get("q3", "")

    combined = text1 + " " + text2 + " " + text3

    mood = get_llm_response2(combined).strip()

    return jsonify({"mood": mood})


# Logout Route
@app.route("/userlogout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("userlogin"))

# --- Running the App ---
if __name__ == "__main__":
    app.run(debug=True)

