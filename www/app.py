from flask import Flask, jsonify, Response
from os import listdir
from os.path import isfile, join
from flask_cors import CORS, cross_origin

from flask import Flask
app = Flask(__name__)
CORS(app)

@app.route("/api/v1/blockdiagrams", methods=['GET'])
def getblockdiagrams():
    files = [f for f in listdir('saved-bds') if isfile(join('saved-bds', f))]
    return jsonify(result=files)

@app.route("/api/v1/blockdiagrams/<string:id>", methods=['GET'])
def getblockdiagram(id):
    print id
    bd = [f for f in listdir('saved-bds') if isfile(join('saved-bds', f)) and id in f]
    print bd[0]
    print join('saved-bds',bd[0])
    with open(join('saved-bds',bd[0]), 'r') as content_file:
        content = content_file.read()
    print content
    return Response(content, mimetype="text/xml")

if __name__ == "__main__":
    app.run(debug=True)
