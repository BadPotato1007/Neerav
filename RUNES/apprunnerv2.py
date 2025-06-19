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
        return render_template('index.html')
    return redirect(url_for('signup_page'))

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

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

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    pass1 = data.get('pass1')

    if not username or not pass1:
        return jsonify({'error': 'Missing username or password'}), 400

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

@app.route('/trivia_start')
def trivia_start():
    username = request.cookies.get('username')
    if not username:
        return redirect(url_for('login_page'))
    return render_template('quiz_main.html', username=username)

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

# Get user's attempted question number
def get_user_attempt_number(username, sub):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    column_name = f"{sub.lower()}_attempted"
    query = ("SELECT %s FROM userdata WHERE username = %s", (column_name, username,))

    try:
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        attempt_number = result[column_name] if result and column_name in result else None
    except mysql.connector.Error as e:
        print("DB Error:", e)
        attempt_number = None

    cursor.close()
    connection.close()
    return attempt_number

def get_next_question(subject, current_attempt_number):
    import mysql.connector

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    # Calculate next question number
    next_question_number = current_attempt_number + 1

    # SQL query (parameters are passed separately to prevent injection)
    query = ("SELECT * FROM questions WHERE sub = %s AND qno = %s")

    # Debug logging
    print(f"[DEBUG] Fetching question → subject='{subject}', qno={next_question_number}")
    print("[DEBUG] Executing query:", query.strip())
    print("[DEBUG] With values:", (subject, next_question_number))

    try:
        cursor.execute("SELECT * FROM questions WHERE sub = %s AND qno = %s", (subject, next_question_number,))
        question = cursor.fetchall()
        print("[DEBUG] Fetched question:", question)
        return question
    except mysql.connector.Error as e:
        print("[ERROR] Database error:", e)
        return None
    finally:
        cursor.close()
        connection.close()


# Route to fetch next question
@app.route('/api/next-question', methods=['GET'])
def next_question():
    sub = request.args.get('subject')
    username = request.cookies.get('username')
    print(username)
    print("sub:", sub)
    print("Username from cookie or param:", username)

    if not sub or not username:
        return jsonify({
    'status': 'error',
    'message': f'Subject and username are required. Got subject={sub}, username={username}'}), 400


    attempt_number = get_user_attempt_number(username, sub)
    if attempt_number is None:
        return jsonify({'status': 'error', 'message': f'Could not find attempt data for sub: {sub}'}), 404

    question = get_next_question(sub, attempt_number)
    if not question:
        return jsonify({'status': 'error', 'message': 'No more questions available'}), 404

    question['question_number'] = attempt_number + 1  
    return jsonify({'status': 'success', 'data': question})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
