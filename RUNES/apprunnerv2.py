from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response
import mysql.connector
from flask_mail import Mail, Message

app = Flask(__name__)

# Configure MySQL connection
db_config = {
    'user': 'runes',
    'password': 'root',
    'host': '192.168.100.66',
    'database': 'runes'
}

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'adicomp05@gmail.com'  # Sender email (must be a Gmail account)
app.config['MAIL_PASSWORD'] = 'lmao'                 # Use an App Password, not your actual password
app.config['MAIL_DEFAULT_SENDER'] = 'adicomp05@gmail.com'
mail = Mail(app)

@app.route('/send_mail', methods=['GET', 'POST'])
def send_mail():
    if request.method == 'POST':
        sender_name = request.form['name']
        sender_email = request.form['email']
        message_body = request.form['message']

        msg = Message(
            subject=f"[RUNES] Contact Form: {sender_name}",
            recipients=['runes@gmail.com'],
            body=f"Name: {sender_name}\nEmail: {sender_email}\n\nMessage:\n{message_body}"
        )

        try:
            mail.send(msg)
            return "Message sent successfully!"
        except Exception as e:
            return f"Failed to send email: {str(e)}"

@app.route('/')
def home():
    username = request.cookies.get('username')
    if username:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Fetch correctq, totalq, and subject attempts
        cursor.execute("""
            SELECT username, correctq AS C, totalq AS T, 
                phy_attempted AS phy,
                chem_attempted AS chem,
                math_attempted AS math
            FROM userdata 
            WHERE username = %s
        """, (username,))
        
        userdata = cursor.fetchone()
        cursor.close()
        conn.close()

        if not userdata:
            return "User not found", 404

        # Compute accuracy
        correct = userdata.get('C', 0) or 0
        total = userdata.get('T', 0) or 0
        accuracy = correct / total if total else 0

        # Add fields needed by template
        userdata['totalq'] = total
        userdata['acc'] = round(accuracy * 100, 2)  # in %
        userdata['phy'] = userdata.get('phy', 0)
        userdata['chem'] = userdata.get('chem', 0)
        userdata['math'] = userdata.get('math', 0)
        return render_template('index.html', username=username, userdata=userdata)
    
    return redirect(url_for('signup_page'))

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')

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

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT username, correctq AS C, totalq AS T FROM userdata WHERE username = %s", (username,))
    userdata = cursor.fetchone()

    if not userdata:
        return "User not found", 404

    # Compute accuracy and inject it into userdata
    C = userdata['C'] or 0
    T = userdata['T'] or 0
    accuracy = C / T if T else 0
    accuracy = round(accuracy * 100, 2)  
    userdata['acc'] = accuracy

    userdata['totalq'] = T

    cursor.close()
    conn.close()

    return render_template('quiz_main.html', username=username, userdata=userdata)

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

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

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

def get_user_attempt_number(username, sub):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    column_name = f"{sub.lower()}_attempted"
    print(f"[DEBUG] Fetching attempt number for user '{username}' and subject '{sub}' using column '{column_name}'")

    try:
        print("SELECT %s FROM userdata WHERE username = %s", (column_name, username))
        cursor.execute("SELECT %s FROM userdata WHERE username = %s", (column_name, username))
        result = cursor.fetchone()
        print(result)
        attempt_number = result[column_name] if result and column_name in result else None
    except mysql.connector.Error as e:
        print("[ERROR] Database error while fetching attempt number:", e)
        attempt_number = None
    finally:
        cursor.close()
        connection.close()

    return attempt_number

def get_next_question(subject, username):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT %s_attempted FROM userdata WHERE username = %s", (subject,username,))
    result = cursor.fetchone()
    current_attempt_number = result[f"{subject}_attempted"] if result and f"{subject}_attempted" in result else 0
    next_question_number = current_attempt_number + 1

    query = "SELECT * FROM questions WHERE sub = %s AND qno = %s"
    cursor.execute(query, (subject, next_question_number))
    question = cursor.fetchone()  # Not fetchall(), unless you expect multiple

    cursor.close()
    connection.close()
    return question  # Return None if not found

@app.route('/api/next-question', methods=['GET'])
def next_question():
    sub = request.args.get('subject')
    username = request.cookies.get('username')

    if not sub or not username:
        return jsonify({
            'status': 'error',
            'message': f'Subject and username are required. Got subject={sub}, username={username}'
        }), 400

    attempt_number = get_user_attempt_number(username, sub)
    if attempt_number is None:
        return jsonify({'status': 'error', 'message': f'Could not find attempt data for sub: {sub}'}), 404

    question = get_next_question(sub, username)
    if not question:
        return jsonify({'status': 'error', 'message': 'No more questions available'}), 404

    return jsonify({'status': 'success', 'data': question, 'question_number': attempt_number + 1})

@app.route('/leaderboard')
def leaderboard():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT username, correctq AS C, totalq AS T FROM userdata")
    users = cursor.fetchall()

    if not users:
        return "No user data available."

    valid_C_values = [user['C'] for user in users if user['C'] is not None]
    C_max = max(valid_C_values) if valid_C_values else 1

    for user in users:
        C = user['C'] or 0
        T = user['T'] or 0
        accuracy = C / T if T else 0
        normalized_correct = C / C_max if C_max else 0
        user['score'] = 50 * (accuracy + normalized_correct)

    users.sort(key=lambda x: x['score'], reverse=True)

    cursor.close()
    conn.close()
    return render_template('leaderboard.html', data=users)

@app.route('/trivia')
def trivia():
    subject = request.args.get('sub')
    print(f"Subject received: {subject}")
    return render_template('trivia.html', subject=subject)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)