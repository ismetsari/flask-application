from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/message', methods=['GET'])
def message():
    return jsonify({"message": "Hello from DevOps case study"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
