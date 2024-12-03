from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/api", methods=["POST"])
def create_test():
    data = request.get_json()
    if not data:
        return jsonify({"error":"Invalid input"}), 400
    question = data['subject']
    print(question)
    return jsonify({'message':'Recieved well'}), 200


if __name__ == "__main__":
    app.run()