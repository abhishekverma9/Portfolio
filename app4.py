from flask import Flask, request, send_from_directory
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Abhi@9648",
    database="user_registration"
)

@app.route('/register', methods=['POST'])
def register():
    try:
        userid = request.form['userid']
        mobile = request.form['mobile']
        password = request.form['password']

        hashed_password = generate_password_hash(password)
        cursor = db.cursor(buffered=True)
        cursor.execute("INSERT INTO users (userid, mobile, password) VALUES (%s, %s, %s)",
                       (userid, mobile, hashed_password))
        db.commit()
        cursor.close()

        return "✅ Registration successful!"
    except Exception as e:
        return f"❌ Error: {e}"

@app.route('/login', methods=['POST'])
def login():
    try:
        userid = request.form['userid']
        password = request.form['password']

        cursor = db.cursor(buffered=True)
        cursor.execute("SELECT password FROM users WHERE userid=%s", (userid,))
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return "❌ User not found!"

        stored_hash = result[0]
        if check_password_hash(stored_hash, password):
            return "success"
        else:
            return "❌ Invalid password!"

    except Exception as e:
        return f"❌ Error: {e}"

# ✅ Serve the welcome page
@app.route('/welcome')
def welcome():
    return send_from_directory('.', 'welcome.html')  # serve the HTML file

if __name__ == '__main__':
    app.run(debug=True)
