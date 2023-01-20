import argparse
from flask import Flask, jsonify, request
import json


#trie implemet
class TrieNode:
    def __init__(self):
        self.children = {}
        self.value = None

trie = TrieNode()
app = Flask(__name__)
data = {}



@app.route('/put', methods=['PUT'])
def put_value():
    key = request.json['key']
    value = request.json['value']
    curr = trie
    for char in key:
        if char not in curr.children:
            curr.children[char] = TrieNode()
        curr = curr.children[char]
    curr.value = value
    return jsonify({'status': 'OK'})

@app.route('/get/<key>', methods=['GET'])
def get_value(key):
    curr = trie
    for char in key:
        if char not in curr.children:
            return jsonify({'error': 'Key not found'})
        curr = curr.children[char]
    if curr.value:
        return jsonify({'___': curr.value})
    else:
        return jsonify({'error': 'Key not found'})

@app.route('/delete/<key>', methods=['DELETE'])
def delete_value(key):
    curr = trie
    stack = []
    for char in key:
        if char not in curr.children:
            return jsonify({'error': 'Key not found'})
        stack.append((curr, char))
        curr = curr.children[char]
    if curr.value:
        curr.value = None
        for curr, char in reversed(stack):
            del curr.children[char]
            if curr.children or curr.value:
                return jsonify({'status': 'OK'})
            else:
                return jsonify({'error': 'Key not found'})

def get_top_value(key):
    curr = trie
    for char in key:
        if char not in curr.children:
            return jsonify({'error': 'Key not found'})
        curr = curr.children[char]
    if curr.value:
        return str(curr.value)
    else:
        return jsonify({'error': 'Key not found'})


@app.route('/query/<path:key>', methods=['GET'])
def query_value(key):
    keys = key.split('.')
    top_key = str(keys[:1])
    top_key = top_key[2:-2]
    trie_value = str(get_top_value(top_key))
    if trie_value == jsonify({'error': 'Key not found'}):
        return jsonify({'error': 'Top_key requested not found'})
    trie_value=trie_value.replace("'", '"')
    value = json.loads(trie_value)
    requested_value=value
    for k in keys[1:]:
       requested_value = requested_value.get(k)
       if not value:
            return jsonify({'error': 'Subkey not found'})
    return {'value': requested_value}

@app.route('/compute/<key>', methods=['GET'])
def compute(key):
    value = query_value(key)
    if 'error' in value:
        return jsonify({'error': value})
    return {'value': value['value']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--host', default='127.0.0.1', help='host IP address')
    parser.add_argument('-p', '--port', default=5001, type=int, help='server port')
    args = parser.parse_args()
    #store servers IP and port
    with open("server_list.txt", "r") as f:
        lines = f.readlines()
        if f'{args.host} {args.port}\n' not in lines:
            with open("server_list.txt", "a") as f:
                f.write(f'{args.host} {args.port}\n')
    app.run(host=args.host, port=args.port, debug=True)


  






