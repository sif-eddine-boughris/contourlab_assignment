from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the Flask API!'})

@app.route('/api/greet', methods=['GET'])
def greet():
    # Get the 'name' parameter from the URL, default to "World" if not provided
    name = request.args.get('name', 'World')
    return jsonify({'message': f'Hello, {name}!'})

if __name__ == '__main__':
    # Run the application in debug mode
    app.run(debug=True)
