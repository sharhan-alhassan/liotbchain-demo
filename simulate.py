# simulate.py

from liotbchain.blockchain import Blockchain
from liotbchain.utils import InvalidChainError
import time
from tqdm import tqdm

def main():
    # Display progress bar for initialization
    with tqdm(total=100, desc="Initializing Blockchain", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:
        my_blockchain = Blockchain()
        for _ in range(100):
            time.sleep(0.01)
            pbar.update(1)
    
    # Data from IoT devices
    iot_data = [
        {"device": "Raspberry Pi 1", "distance": 120, "timestamp": time.time()},
        {"device": "Raspberry Pi 2", "distance": 150, "timestamp": time.time()},
        {"device": "Raspberry Pi 3", "distance": 160, "timestamp": time.time()},
        {"device": "Raspberry Pi 4", "distance": 170, "timestamp": time.time()},
    ]

    # Simulate the process of receiving data and adding it as blocks to the blockchain
    for data in iot_data:
        with tqdm(total=100, desc=f"Processing {data['device']}", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:
            my_blockchain.add_transaction(data)
            for _ in range(100):
                time.sleep(0.01)
                pbar.update(1)

    # Display the blockchain
    print("\nFull Blockchain:")
    for block in my_blockchain.get_chain():
        print(f"Block {block.index}: Transactions={block.data}, Nonce={block.nonce}, Hash={block.hash}, Merkle Root={block.calculate_merkle_root()}")

    # Validate the integrity of the blockchain
    try:
        if my_blockchain.is_chain_valid():
            print("\nThe blockchain is valid.")
        else:
            print("\nThe blockchain is not valid.")
    except InvalidChainError as e:
        print(f"Blockchain validation failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
