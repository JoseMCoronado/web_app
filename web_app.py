pip install flask

from flask import Flask, render_template, jsonify
app = Flask(__name__)

@app.route("/")
def hello():
    return "Goodbye World!"


# returns an HTML webpage
@app.route("/user/<username>")
def user(username):
    return render_template('profile.html', name=username)

#returns a piece of data in JSON format
@app.route("/lotsofdata")
def people():
    my_people = {
        'alice': 25,
        'bob': 21,
        'charlie': 20,
        'doug': 28
    }
    return jsonify(my_people)

if __name__ == "__main__":
    app.run(debug=True)
