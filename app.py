from flask import Flask, render_template, request, jsonify
import problem_generation

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/api", methods=["POST"])
def create_test():
    data = request.get_json()
    if not data:
        return jsonify({"error":"Invalid input"}), 400
    subject = data['subject']
    problem_generation.create_question(subject)
    return jsonify({'message':'Recieved well'}), 200

@app.route('/question.txt', methods=['GET'])
def get_question():
    with open('question.txt', 'r') as txt:
        content = txt.read()
    return content, 200

@app.route("/answer", methods=['Post'])
def answer_question():
    data = request.get_json()
    if not data:
        return jsonify({"error":"Invalid input"}), 400
    answer = data['answer']
    problem_generation.answer = answer
    return jsonify({'message':'Answer posted'}), 200


if __name__ == "__main__":
    app.run()