# liotbchain demo
liotbchain is a lightweight IoT blockchain framework designed for educational and experimental purposes. It allows you to create and manage a blockchain network, add transactions, and mine blocks. This framework can be used to simulate a real-world blockchain environment.

Disclaimer: This framework is not intended for production use. It is designed for educational and experimental purposes only.

# Features
- Create and manage a blockchain network
- Add transactions and mine blocks
- Configurable difficulty and nonce limit
- Supports digital signatures for transaction verification
- Integration with PostgreSQL for persistent storage
- Installation
- You can install liotbchain via pip:

```py
pip install liotbchain

```

# Configuration
liotbchain uses environment variables for configuration. You can set these variables in a .env file or export them directly in your terminal session.

## Environment Variables
```sh
DATABASE_URL: Database URL for PostgreSQL database connection
TRANSACTIONS_PER_BLOCK: Number of transactions to be grouped into a single block (default is 1)
DIFFICULTY: Mining difficulty, the number of leading zeros required in the block hash (default is 4)
NONCE_LIMIT: Nonce limit to prevent infinite loops during the mining process (default is 1000000)
Example .env file:
```

```sh
DATABASE_URL=your_postgres_db_url
TRANSACTIONS_PER_BLOCK=2
DIFFICULTY=4
NONCE_LIMIT=1000000
```

# Usage
## Running the Receiver Server
The receiver server is responsible for receiving data, verifying signatures, and adding transactions to the blockchain. The receiver server runs a Flask application that exposes endpoints for receiving data and retrieving the blockchain.

## Install Dependencies

```sh
pip install -r requirements.txt
```

## Run the Receiver Server
```py
python3 server/receiver.py
```

## Running the Sender Client Server
The sender client server is responsible for generating and signing data, and sending it to the receiver server at specified intervals. The sender server runs a Flask application that exposes an endpoint to start sending data.

```py
python3 client/sender.py
```

# Endpoints
## Receiver Server Endpoints
1. Receive Data

- Endpoint: /receive_data
- Method: POST
- Description: Receives data from the sender client server, verifies the signature, and adds it to the blockchain.
- Request Body:

```json
{
  "data": {
    "device": "Raspberry Pi 1",
    "distance": 120,
    "timestamp": 1717979369.243414
  },
  "signature": "base64_encoded_signature",
  "public_key": "-----BEGIN PUBLIC KEY-----...-----END PUBLIC KEY-----"
}
```

2. Get Blockchain

- Endpoint: /get_chain
- Method: GET
- Description: Retrieves the full blockchain.
- Response:

```json
[
  {
    "timestamp": 1717979369.243414,
    "index": 0,
    "data": "Genesis Block",
    "nonce": 0,
    "hash": "hash_value",
    "previous hash": "previous_hash_value"
  },
  ...
]
```

3. Start Sending Data

- Endpoint: /start_sending
- Method: POST
- Description: Starts generating and sending data to the receiver server every specified interval time.

```json
{
  "number_of_items_to_send": 2,         // Two items in payload
  "interval_time": 2                    // Wait time in-between payload
}
```

# Use the Swagger UI provided by Flask-Swagger to interact with the endpoints. Open your browser and navigate to:

- Receiver Server: `http://localhost:5001/apidocs/`

- Sender Client Server: `http://localhost:5000/apidocs/`

- Use the Swagger UI to start sending data from the sender client server to the receiver server by calling the /start_sending endpoint with the desired number of items and interval time.


# License
This project is licensed under the MIT License.

# Author
Sharhan Alhassan - sharhanalhassan@gmail.com