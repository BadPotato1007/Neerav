from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response
import mysql.connector as db

app = Flask(__name__)

db_config = {
    'user': 'runes',
    'password': 'root',        
    'host': '192.168.100.26',
    'database': 'runes'
}
def get_db_connection():
    try:
        connection = db.connect(**db_config)
        return connection
    except db.Error as e:
        print(f"Error connecting to database: {e}")
        return None

@app.route('/')
def index():
    username = request.cookies.get('username')
    if username:
        return render_template('index.html')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')






















if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)