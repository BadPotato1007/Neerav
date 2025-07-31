from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/questions', methods=['GET'])
def get_questions():
    return "yeah"

@app.route('/api/details', methods=['GET'])
def get_details():
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Missing username in query parameters"}), 401
    user = "hello"
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

if __name__ == '__main__':
    app.run(debug=True)