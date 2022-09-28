import hashlib
import logging
import sys
import time
import utils
import hashlib
import json

Mining_DIFFCULTY = 3
MINING_SENDER = 'n23n3b3b4(Senders adress on network)'
Mining_REWARD = 1.3

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

class Blockchain(object):
    '''
    Blockchain class
    ----------
    transaction_pool : list
        Store the list of transaction
        When next block is crearted the infomation inside
        the poool is stored in next block and the pool is empty.
    chain : list
        store the list of block(s)
        [block] -> [block] -> [block]
    '''
    def __init__(self, blockchain_address = None):
        self.transaction_pool = []
        self.chain = []
        self.create_block(0, self.hash({}))
        self.blockchain_address = blockchain_address

    def create_block(self, nonce, previous_hash):
        block = utils.sorted_dict_by_key({
            'timestamp': time.time(),
            'transactions': self.transaction_pool,
            'nonce': nonce,
            'previous_hash': previous_hash
        })
        self.chain.append(block)
        self.transaction_pool = []
        return block

    def hash(self, block):
        sorted_block = json.dumps(block, sort_keys= True)
        return hashlib.sha256(sorted_block.encode()).hexdigest()

    def add_transaction(self, sender_blockchain_address,
                    receipient_blockchain_address, value):
        transaction = utils.sorted_dict_by_key({
            'sender_blockchain_address': sender_blockchain_address,
            'receipient_blockchain_address': receipient_blockchain_address,
            'value': float(value)
        })
        self.transaction_pool.append(transaction)
        return True

    def valid_proof(self, transactions,previous_hash,
                    nonce, difficulty= Mining_DIFFCULTY):
        '''This fucntion calcualte the nonce.

        '''
        guess_block =utils.sorted_dict_by_key({
            'timestamp': time.time(),
            'transactions': transactions,
            'nonce': nonce,
            'previous_hash': previous_hash
        })
        guess_hash = self.hash(guess_block)
        return guess_hash[:difficulty] == '0'*difficulty

    def proof_of_work(self):
        """The fucntion calculates nonce
            untill it matchs given length of first digit of number.

        Returns:
            [type]: [description]
        """
        transactions = self.transaction_pool.copy()
        previous_hash = self.hash(self.chain[-1])
        nonce = 0
        while self.valid_proof(transactions, previous_hash, nonce) is False:
            nonce +=1
        return nonce

    def mining(self):
        """Function that register address in server and recive rewards when
        mining is over
        """
        self.add_transaction(
            sender_blockchain_address= MINING_SENDER,
            receipient_blockchain_address = self.blockchain_address,
            value= Mining_REWARD
        )
        nonce = self.proof_of_work()
        previous_hash = self.hash(self.chain[-1])
        self.create_block(nonce, previous_hash)
        logger.info({"action":'mining', 'status':'sucess'})
        return True


    def calculate_total_amount(self, blockchain_address):
        total_amount = 0.0
        for block in self.chain:
            for transaction in block['transactions']:
                value = float(transaction['value'])
                if blockchain_address == transaction['receipient_blockchain_address']:
                    total_amount += value
                if blockchain_address == transaction['sender_blockchain_address']:
                    total_amount -= value
        return total_amount


if __name__ == '__main__':
    my_blockchain_address = '3njr36v9w3(your address)'
    block_chain = Blockchain(blockchain_address=my_blockchain_address)
    utils.pprint(block_chain.chain)

    block_chain.add_transaction('A-san','b-san', 1.0)
    block_chain.mining()
    utils.pprint(block_chain.chain)
    #print("現在の hash "+ block_chain.hash(block_chain.chain[0]))

    block_chain.add_transaction('c-san','f-san', 2.0)
    block_chain.add_transaction('X','Y', 3.0)
    block_chain.mining()
    #print("現在の hash "+ block_chain.hash(block_chain.chain[-2]))
    utils.pprint(block_chain.chain)

    print('my', block_chain.calculate_total_amount(my_blockchain_address))
    print('C', block_chain.calculate_total_amount('c-san'))
    print('D', block_chain.calculate_total_amount('f-san'))
