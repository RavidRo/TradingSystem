"""This class is the gateway from the client to the domain server layer.
All the api calls and data asked from the server goes here.
This class is responsible for calling the right methods in the login classes."""

from flask import Flask,request
from werkzeug.security import generate_password_hash, check_password_hash
from Backend.Domain.Authentication import authentication
app = Flask(__name__)

users = {
    'tali':'puppy',
    'sean':'messi',
    'ravid':'kiss',
    'inon':'guy',
    'omer':'cool'
}
@app.route('/' , methods=['GET'])
def main_page():
    return 'Hello, World!'

@app.route('/register', methods=['GET'])
def register():
    username = request.args.get('username')
    password = request.args.get('password')
    answer = authentication.register(username=username,password=password)
    return '''<h1>Answer is: {}</h1>'''.format(answer)

@app.route('/login', methods=['GET'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    answer = authentication.login(username=username, password=password)
    return '''<h1>Answer is: {}</h1>'''.format(answer)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


if __name__ == '__main__':
	app.run(debug=True)
