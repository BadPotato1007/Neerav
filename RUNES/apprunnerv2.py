from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response
import mysql.connector

app = Flask(__name__)

# Configure MySQL connection
db_config = {
    'user': 'runes',
    'password': 'root',
    'host': '192.168.100.82',
    'database': 'runes'
}


@app.route('/')
def home():
    username = request.cookies.get('username')
    if username:
        return f"Hello, {username}! <a href='/logout'>Logout</a>"
    return redirect(url_for('login_page'))


@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


@app.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')


@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    pass1 = data.get('pass1')
    email = data.get('email')

    if not username or not pass1 or not email:
        return jsonify({'error': 'Missing username, email or password'}), 400

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO userdata (username, email, pass) VALUES (%s, %s, %s)", (username, email, pass1))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'User created successfully!'})
    except mysql.connector.IntegrityError:
        return jsonify({'error': 'Username already exists'}), 400


@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')  # expects 'password', not 'pass1'

    if not username or not email or not password:
        return jsonify({'error': 'Missing username, email, or password'}), 400

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO userdata (username, email, pass) VALUES (%s, %s, %s)", (username, email, password))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Registration successful!'})
    except mysql.connector.IntegrityError:
        return jsonify({'error': 'Username already exists'}), 400


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    pass1 = data.get('pass1')
    email = data.get('email')
    if not username or not pass1 or not email:
        return jsonify({'error': 'Missing username ,  email or password'}), 400

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT pass FROM userdata WHERE username = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result and result[0] == pass1:
        resp = make_response(jsonify({'message': 'Login successful'}))
        resp.set_cookie('username', username)
        return resp
    return jsonify({'error': 'Invalid username or password'}), 401


@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('login_page')))
    resp.delete_cookie('username')
    return resp


@app.route('/api/profile', methods=['GET'])
def profile():
    username = request.cookies.get('username')
    if not username:
        return jsonify({'error': 'Not logged in'}), 401

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM userdata WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        return jsonify({'username': user[0]})
    return jsonify({'error': 'User not found'}), 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
