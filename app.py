from flask import Flask, render_template, request, jsonify
import problem_generation
import json
import threading

app = Flask(__name__)

currentslide = 0

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/api", methods=["POST"])
def create_test():
    global currentslide
    data = request.get_json()
    if not data:
        return jsonify({"error":"Invalid input"}), 400
    subject = data['subject']
    print("Hjere")
    currentslide=1
    problem_generation.create_question(subject)
    return jsonify({'message':'Recieved well'}), 200

@app.route('/question.txt', methods=['GET'])
def get_question():
    with open('question.txt', 'r') as txt:
        content = txt.read()
    return content, 200

@app.route("/answer", methods=['POST'])
def answer_question():
    global currentslide
    currentslide = 2
    data = request.get_json()
    if not data:
        return jsonify({"error":"Invalid input"}), 400
    answer = data['answer']
    problem_generation.answer = answer
    return jsonify({'message':'Answer posted'}), 200

#Error 999 means that the question has not been answered yet
@app.route("/work.txt", methods=["GET"])
def get_work():
    if not problem_generation.answered:
        return "document not created yet", 200
    with open("problem_result.json", "r") as txt:
        data = json.load(txt)
        return data["work"], 200

@app.route('/correct.txt')
def get_correctness():
    if not problem_generation.answered:
        return jsonify({"error":"document not created yet"}), 200
    with open("problem_result.json", "r") as txt:
        data = json.load(txt)
        return data["result"], 200
    
@app.route('/next', methods=["POST"])
def next():
    global currentslide
    currentslide=1
    create_test()

@app.route("/frame.txt", methods=["POST"])
def returnframe():
    global currentslide
    return str(currentslide), 200

def moveonfromloading():
    global currentslide
    while True:
        if currentslide == 2 and problem_generation.answered:
            currentslide = 3

if __name__ == "__main__":
    threading.Thread(target=moveonfromloading, daemon=True).start()
    app.run(debug=True, port=8080)
    