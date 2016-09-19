from flask import Flask, jsonify, Response
from os import listdir
from os.path import isfile, join
from flask_cors import CORS, cross_origin
import xml.etree.ElementTree

from flask import Flask
app = Flask(__name__)
CORS(app)

@app.route("/api/v1/blockdiagrams", methods=['GET'])
def getblockdiagrams():
    names = []
    for f in listdir('saved-bds'):
        if isfile(join('saved-bds', f)) and f.endswith('.xml'):
            names.append(xml.etree.ElementTree.parse(join('saved-bds', f)).getroot().find('designName').text)
    return jsonify(result=names)

@app.route("/api/v1/blockdiagrams/<string:id>", methods=['GET'])
def getblockdiagram(id):
    id = id.replace(" ", "_").replace(".", "_")
    bd = [f for f in listdir('saved-bds') if isfile(join('saved-bds', f)) and id in f]
    with open(join('saved-bds',bd[0]), 'r') as content_file:
        content = content_file.read()
    return Response(content, mimetype="text/xml")

if __name__ == "__main__":
    app.run(debug=True)
