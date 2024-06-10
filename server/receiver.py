# receiver_server.py
from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
import base64
import json
from liotbchain.blockchain import Blockchain
from liotbchain.utils import InvalidChainError
import logging
import time

app = Flask(__name__)
swagger = Swagger(app)
blockchain = Blockchain()

@app.route('/receive_data', methods=['POST'])
@swag_from({
    'summary': 'Receive data from the sender server',
    'description': 'Verifies the signature and adds the data to the blockchain',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'data': {
                            'type': 'object',
                            'properties': {
                                'device': {
                                    'type': 'string',
                                    'example': 'Raspberry Pi 1'
                                },
                                'distance': {
                                    'type': 'integer',
                                    'example': 120
                                },
                                'timestamp': {
                                    'type': 'number',
                                    'format': 'float',
                                    'example': time.time()
                                }
                            }
                        },
                        'signature': {
                            'type': 'string',
                            'example': 'base64_encoded_signature'
                        },
                        'public_key': {
                            'type': 'string',
                            'example': '-----BEGIN PUBLIC KEY-----...-----END PUBLIC KEY-----'
                        }
                    }
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Success',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'message': {'type': 'string'}
                }
            }
        }
    }
})
def receive_data():
    payload = request.json
    if not isinstance(payload, list):
        return jsonify({"message": "Payload should be a list of items", "status": "error"}), 400

    for item in payload:
        if 'data' not in item or 'signature' not in item or 'public_key' not in item:
            return jsonify({'status': 'error', 'message': 'Invalid payload structure'}), 400

        data = json.dumps(item['data']).encode('utf-8')
        encoded_signature = item['signature']
        signature = base64.b64decode(encoded_signature)
        public_key_pem = item['public_key'].encode('utf-8')

        # Load the public key from the PEM format
        public_key = serialization.load_pem_public_key(public_key_pem)

        # Verify the signature
        try:
            public_key.verify(
                signature,
                data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            # Add the data to the blockchain
            blockchain.add_transaction(item['data'])
        except Exception as e:
            return jsonify({'status': 'error', 'message': f'Invalid signature for item: {item["data"]}'}), 400

    return jsonify({"status": "success", "message": "Data added to blockchain"}), 200

@app.route('/get_chain', methods=['GET'])
@swag_from({
    'summary': 'Get the full blockchain',
    'description': 'Returns the entire blockchain',
    'responses': {
        '200': {
            'description': 'Success',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'timestamp': {'type': 'integer'},
                        'index': {'type': 'integer'},
                        'data': {'type': 'array', 'items': {'type': 'object'}},
                        'nonce': {'type': 'integer'},
                        'hash': {'type': 'string'},
                        'previous hash': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def get_chain():
    chain_data = []
    for block in blockchain.get_chain():
        chain_data.append({
            'timestamp': block.timestamp,
            'index': block.index,
            'data': block.data,
            'nonce': block.nonce,
            'hash': block.hash,
            'previous hash': block.previous_hash
        })
    return jsonify(chain_data)

if __name__ == "__main__":
    app.run(port=5001)
