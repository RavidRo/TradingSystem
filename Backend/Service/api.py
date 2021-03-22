"""this class if the gateway from the client to the domain server layer
all the api calls and data asked from the server goes here
this class is responsible for calling the right methods in the login classes"""

from flask import Flask,request
from Backend.Service import trading_system
app = Flask(__name__)

@app.route('/' , methods=['GET'])
def main_page():
    return 'Hello, World!'

@app.route('/register', methods=['GET'])
def register():
    username = request.args.get('username')
    password = request.args.get('password')
    answer = trading_system.register(username=username,password=password)
    return '''<h1>Answer is: {}</h1>'''.format(answer)

@app.route('/login', methods=['GET'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    answer = trading_system.login(username=username, password=password)
    return '''<h1>Answer is: {}</h1>'''.format(answer)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


if __name__ == '__main__':
	app.run(debug=True)
