from flask import Flask, jsonify, Response, request, redirect
from os import listdir
from os.path import isfile, join
from flask_cors import CORS, cross_origin
import xml.etree.ElementTree

app = Flask(__name__)
CORS(app)

@app.route('/api/v1/blockdiagrams', methods=['GET'])
def getblockdiagrams():
    names = []
    for f in listdir('saved-bds'):
        if isfile(join('saved-bds', f)) and f.endswith('.xml'):
            names.append(xml.etree.ElementTree.parse(join('saved-bds', f)).getroot().find('designName').text)
    return jsonify(result=names)

@app.route('/api/v1/blockdiagrams', methods=['POST'])
def saveblockdiagram():
    designName = request.form['designName'].replace(' ', '_').replace('.', '_')
    bdString = request.form['bdString']
    root = xml.etree.ElementTree.Element("root")

    xml.etree.ElementTree.SubElement(root, 'designName').text = designName
    xml.etree.ElementTree.SubElement(root, 'bd').text = bdString

    tree = xml.etree.ElementTree.ElementTree(root)
    tree.write('saved-bds/' + designName + '.xml')
    return redirect(request.url)

@app.route('/api/v1/blockdiagrams/<string:id>', methods=['GET'])
def getblockdiagram(id):
    id = id.replace(' ', '_').replace('.', '_')
    bd = [f for f in listdir('saved-bds') if isfile(join('saved-bds', f)) and id in f]
    with open(join('saved-bds',bd[0]), 'r') as content_file:
        content = content_file.read()
    return Response(content, mimetype='text/xml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
