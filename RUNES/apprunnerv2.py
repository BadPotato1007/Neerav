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
    print(f"[DEBUG] Fetching attempt number for user '{username}' and subject '{sub}' using column '{column_name}'")
    query = ("SHOW COLUMNS FROM userdata LIKE %s")
    cursor.execute(query, (column_name,))
    query = ("SELECT %s FROM userdata WHERE username = %s", (column_name, username,))

    try:
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        attempt_number = result[column_name] if result and column_name in result else None
    except mysql.connector.Error as e:
        print("[ERROR] Database error while fetching attempt number:", e)
        attempt_number = None
        print("[DB Error]:", e)
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
        print("[DEBUG]", query, (subject, next_question_number,))
        execute_query = cursor.execute(query, (subject, next_question_number,))
        print("[DEBUG] Query executed successfully:", execute_query)
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







from flask import Flask, render_template_string
import mysql.connector

app = Flask(__name__)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Leaderboard | RUNES</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@300..700&display=swap" rel="stylesheet" />
  <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet" />
  <style>
    @font-face {
      font-family: 'norse';
      src: url('/static/fonts/norse.otf') format('opentype');
    }

    body {
      background: linear-gradient(135deg, rgba(75, 0, 130, 0.8), rgba(0, 0, 255, 0.5));
      font-family: 'Quicksand', sans-serif;
      background-image: url('https://i.ibb.co/9mf6y34K/1111-Photoroom.png');
      background-size: cover;
      background-position: center;
      background-attachment: fixed;
    }

    .frosted {
      backdrop-filter: blur(70px);
      background: rgba(255, 255, 255, 0.1);
      border-radius: 15px;
      border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .frostednav {
      backdrop-filter: blur(70px);
      background: rgba(255, 255, 255, 0.1);
    }

    .customfont {
      font-family: 'norse', sans-serif;
    }
  </style>
</head>
<body class="text-white">

  <!-- Navbar -->
  <nav class="w-full px-6 py-4 bg-transparent flex justify-between items-center frostednav fixed top-0 shadow-md z-10">
    <div class="flex items-center space-x-4">
      <img src="https://i.ibb.co/F1CK3wq/logo.png" alt="Runes Logo" class="w-12 h-12 shadow-md" />
      <span class="text-3xl text-white customfont">R U N E S</span>
    </div>
  </nav>

  <!-- Leaderboard Section -->
  <div class="pt-24 max-w-4xl mx-auto px-4">
    <div class="frosted p-6 shadow-lg">
      <h1 class="text-3xl font-bold text-center mb-6">🏆 Leaderboard</h1>
      <div class="overflow-x-auto rounded-lg">
        <table class="w-full text-left border-collapse text-white">
          <thead class="bg-purple-700 bg-opacity-30">
            <tr>
              <th class="p-4">S. No</th>
              <th class="p-4">Username</th>
              <th class="p-4">Score</th>
            </tr>
          </thead>
          <tbody>
            {% for user in data %}
            <tr class="border-b border-white border-opacity-10 hover:bg-white hover:bg-opacity-10 transition">
              <td class="p-4">{{ loop.index }}</td>
              <td class="p-4">{{ user.username }}</td>
              <td class="p-4">{{ '%.2f' % user.score }}</td>
            </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </div>
  </div>

</body>
</html>"""

@app.route('/leaderboard')
def leaderboard():
    # Connect to MySQL
    conn = mysql.connector.connect(
        host='192.168.100.82',
        user='runes',       # 🔁 Replace with your MySQL username
        password='root',    # 🔁 Replace with your MySQL password
        database='runes'    # 🔁 Replace with your MySQL database name
    )
    cursor = conn.cursor(dictionary=True)

    # Get user data from 'userdata' table
    cursor.execute("SELECT username, correctq AS C, totalq AS T FROM userdata")
    users = cursor.fetchall()

    if not users:
        return "No user data available."

    # Calculate max correct answers to normalize
    C_max = max(user['C'] for user in users) or 1  # Prevent divide-by-zero

    # Compute scores
    for user in users:
        C = user['C']
        T = user['T']
        accuracy = C / T if T else 0
        normalized_correct = C / C_max
        user['score'] = 50 * (accuracy + normalized_correct)

    # Sort users by score descending
    users.sort(key=lambda x: x['score'], reverse=True)

    # Render the leaderboard
    cursor.close()
    conn.close()
    return render_template('leaderboard.html', data=users)





if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
