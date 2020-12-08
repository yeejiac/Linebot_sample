from flask import Flask, jsonify
from runserver.locationTransfer import get_nearby_restaurant
import json

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/getlocationInfo', methods=['GET'])
def getlocationInfo():
    list_res = get_nearby_restaurant(25.042363209943446, 121.56481611369205)
    return jsonify({'result': list_res})

if __name__ == '__main__':
    app.run(debug=True)