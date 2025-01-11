from flask import Flask, render_template, request, jsonify
import problem_generation
import json
import threading
import logging
import time
import os
log = logging.getLogger('werkzeug')
log.disabled = True
app = Flask(__name__)

user_states = {}

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/api", methods=["POST"])
def create_test():
    data = request.get_json()
    if not data:
        return jsonify({"error":"Invalid input"}), 400
    subject = data['subject']
    user_id = data['user_id']
    user_states[user_id] = {"currentslide": 1, "answered": False}
    problem_generation.create_question(f"Write a problem for {subject}. Do not include the solution, or any methods. Make sure that this question is at an appropriate difficulty for an {subject} student.", user_id=user_id)
    return jsonify({'message':'Received well'}), 200

@app.route('/question.txt', methods=['GET'])
def get_question():
    user_id = request.args.get('user_id')
    with open(f'{user_id}_question.txt', 'r') as txt:
        content = txt.read()
    return content, 200

@app.route("/answer", methods=['POST'])
def answer_question():
    data = request.get_json()
    if not data:
        return jsonify({"error":"Invalid input"}), 400
    answer = data['answer']
    user_id = data['user_id']
    user_states[user_id]['currentslide'] = 3
    problem_generation.set_answer(user_id, answer)
    return jsonify({'message':'Answer posted'}), 200

@app.route("/work.txt", methods=["GET"])
def get_work():
    user_id = request.args.get('user_id')
    if not user_states[user_id]['answered']:
        return "document not created yet", 200
    with open(f"{user_id}_problem_result.json", "r") as txt:
        data = json.load(txt)
        return data["work"], 200

@app.route('/correct.txt')
def get_correctness():
    user_id = request.args.get('user_id')
    if not user_states[user_id]['answered']:
        return jsonify({"error":"document not created yet"}), 200
    with open(f"{user_id}_problem_result.json", "r") as txt:
        data = json.load(txt)
        return data["result"], 200

@app.route('/sametopic', methods=["POST"])
def sametopic():
    data = request.get_json()
    if not data:
        return jsonify({"error":"Invalid input"}), 400
    subject = data['subject']
    previous_question = data['previous_question']
    user_id = data['user_id']
    user_states[user_id]['currentslide'] = 1
    problem_generation.create_question(f"Write a problem for {subject}. Do not include the solution, or any methods. Make sure that this question is at an appropriate difficulty for an {subject} student.", previous_question, "similar", user_id=user_id)
    return jsonify({'message':'Received well'}), 200

@app.route('/differenttopic', methods=["POST"])
def differenttopic():
    data = request.get_json()
    if not data:
        return jsonify({"error":"Invalid input"}), 400
    subject = data['subject']
    previous_question = data['previous_question']
    user_id = data['user_id']
    user_states[user_id]['currentslide'] = 1
    problem_generation.create_question(f"Write a problem for {subject}. Do not include the solution, or any methods. Make sure that this question is at an appropriate difficulty for an {subject} student.", previous_question, "different", user_id=user_id)
    return jsonify({'message':'Received well'}), 200    

@app.route('/easyquestion', methods=["POST"])
def easytopic():
    data = request.get_json()
    if not data:
        return jsonify({"error":"Invalid input"}), 400
    subject = data['subject']
    previous_question = data['previous_question']
    user_id = data['user_id']
    user_states[user_id]['currentslide'] = 1
    problem_generation.create_question(f"Write a problem for {subject}. Do not include the solution, or any methods. Make sure that this question is at an appropriate difficulty for an {subject} student.", previous_question, "easier", user_id=user_id)
    return jsonify({'message':'Received well'}), 200   

@app.route('/hardquestion', methods=["POST"])
def hardtopic():
    data = request.get_json()
    if not data:
        return jsonify({"error":"Invalid input"}), 400
    subject = data['subject']
    previous_question = data['previous_question']
    user_id = data['user_id']
    user_states[user_id]['currentslide'] = 1
    problem_generation.create_question(f"Write a problem for {subject}. Do not include the solution, or any methods. Make sure that this question is at an appropriate difficulty for an {subject} student.", previous_question, "harder", user_id=user_id)
    return jsonify({'message':'Received well'}), 200   

@app.route("/frame.txt", methods=["POST"])
def returnframe():
    user_id = request.args.get('user_id')
    return str(user_states[user_id]['currentslide']), 200

@app.route("/delete", methods=["POST"])
def deleteuser():
    data = request.get_json()
    user_id = data.get("user_id")
    if user_id in user_states:
        del user_states[user_id]
    if user_id in problem_generation.user_answers:
        del problem_generation.user_answers[user_id]
    if user_id in problem_generation.user_answered:
        del problem_generation.user_answered[user_id]
    if os.path.exists(f"{user_id}_question.txt"):
        os.remove(f"{user_id}_question.txt")
    if os.path.exists(f"{user_id}_problem_result.json"):
        os.remove(f"{user_id}_problem_result.json")
    if os.path.exists(f"LLamaInteraction/LLMInput_{user_id}"):
        os.rmdir(f"LLamaInteraction/LLMInput_{user_id}")
    return "Deleted", 200

def moveonfromloading():
    while True:
        for user_id, state in user_states.items():
            if state['currentslide'] == 1:
                if os.path.exists(f"{user_id}_question.txt"):
                    with open(f"{user_id}_question.txt", "r") as txt:
                        if txt.read() != "":
                            state['currentslide'] = 2
            if state['currentslide'] == 3 and state['answered']:
                state['currentslide'] = 4
        time.sleep(0.1)

if __name__ == "__main__":
    threading.Thread(target=moveonfromloading, daemon=True).start()
    app.run(debug=False, port=8080)