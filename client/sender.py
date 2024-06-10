# sender_server.py
from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
import requests
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
import base64
import time
import json
import random
import threading

app = Flask(__name__)
swagger = Swagger(app)

# Generate a private key for the sender
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# Generate the corresponding public key
public_key = private_key.public_key()

# Save the keys to PEM format
def save_keys():
    with open("private_key.pem", "wb") as private_file:
        private_file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        )
    with open("public_key.pem", "wb") as public_file:
        public_file.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

save_keys()

# Default values for the number of items in the payload and the interval time
number_of_items_to_send = 2
interval_time = 2

def generate_random_data():
    devices = [
        "Raspberry Pi 1", 
        "Raspberry Pi 2",
        "Raspberry Pi 3",
        "Nodemcu 1", 
        "Nodemcu 2"
        "Nodemcu 3"
    ]
    data = {
        "device": random.choice(devices),
        "distance": random.randint(50, 200),
        "timestamp": time.time()
    }
    return data

def send_data():
    data_list = [generate_random_data() for _ in range(number_of_items_to_send)]
    payload_list = []

    for data in data_list:
        message = json.dumps(data).encode('utf-8')

        # Sign the data
        signature = private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        # Base64 encode the signature for transmission
        encoded_signature = base64.b64encode(signature).decode('utf-8')

        # Encode the public key to PEM format
        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

        payload = {
            'data': data,
            'signature': encoded_signature,
            'public_key': public_key_pem
        }

        payload_list.append(payload)

    # Send the signed data to the blockchain server
    response = requests.post('http://localhost:5001/receive_data', json=payload_list)
    print(response.json())

def start_sending_data():
    while True:
        send_data()
        time.sleep(interval_time)

@app.route('/start_sending', methods=['POST'])
@swag_from({
    'summary': 'Start sending data to the blockchain server',
    'description': 'Starts generating and sending data to the blockchain server every specified interval time',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'number_of_items_to_send': {
                        'type': 'integer',
                        'example': 2
                    },
                    'interval_time': {
                        'type': 'integer',
                        'example': 2
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
def start_sending():
    global number_of_items_to_send, interval_time
    data = request.json
    number_of_items_to_send = data.get('number_of_items_to_send', 1)
    interval_time = data.get('interval_time', 2)
    
    threading.Thread(target=start_sending_data).start()
    return jsonify({"status": "success", "message": f"Started sending {number_of_items_to_send} items every {interval_time} seconds"}), 200

if __name__ == "__main__":
    app.run(port=5000)
