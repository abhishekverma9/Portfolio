from flask import Flask, request
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash

app = Flask(__name__)
CORS(app)  # Enables cross-origin requests from your HTML page

# --- Database Connection Function ---
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Abhi@9648",  # your MySQL password
            database="user_registration"
        )
        return conn
    except Error as e:
        print("❌ Database connection failed:", e)
        return None

# --- Register API ---
@app.route('/register', methods=['POST'])
def register():
    conn = get_db_connection()
    if conn is None:
        return "❌ Could not connect to database.", 500

    try:
        cursor = conn.cursor()

        userid = request.form.get('userid')
        mobile = request.form.get('mobile')
        password = request.form.get('password')

        if not userid or not mobile or not password:
            return "⚠️ All fields are required!", 400

        hashed_password = generate_password_hash(password)

        # Insert user record
        sql = "INSERT INTO users (userid, mobile, password) VALUES (%s, %s, %s)"
        cursor.execute(sql, (userid, mobile, hashed_password))
        conn.commit()

        return "✅ Registration successful!"
    
    except mysql.connector.Error as db_err:
        return f"❌ Database error: {db_err}"
    
    except Exception as e:
        return f"❌ Unexpected error: {e}"

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# --- Run Flask App ---
if __name__ == '__main__':
    app.run(debug=True)
