from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response
import mysql.connector

app = Flask(__name__)

# Configure MySQL connection 
db_config = {
    'user': 'runes',
    'password': 'root',         # Set your MySQL root pass1 here if you have one
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
    if not username or not pass1:
        return jsonify({'error': 'Missing username or password'}), 400

    hashed_pass1 = (pass1)
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO userdata (username, pass) VALUES (%s, %s)", (username, hashed_pass1))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'User created successfully!'})
    except mysql.connector.IntegrityError:
        return jsonify({'error': 'Username already exists'}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    pass1 = data.get('pass1')
    if not username or not pass1:
        return jsonify({'error': 'Missing username or pass'}), 400

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(buffered=True)
    cursor.execute("SELECT pass FROM userdata WHERE username = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        stored_hash = result[0]
        if not stored_hash:
            return jsonify({'error': 'Invalid username or password'}), 401
        if isinstance(stored_hash, bytes):
            pass  # No decoding or hashing needed since passwords are stored in plain text
        if check_password_hash(stored_hash, pass1):
            resp = make_response(jsonify({'message': 'Login successful'}))
            resp.set_cookie('username', username)
            return resp
    return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('login_page')))
    resp.delete_cookie('username')
    return resp

# Example protected API endpoint
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
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)