# Creating a blockchain >>>

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# imports
import datetime # for dates blocks are created
import hashlib # to hash the blocks
import json # to encode the blocks before hashing
from flask import Flask, jsonify # to create an object of Flask class and jsonify 

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Building a blockchain - build blockchain class

class Blockchain:
    
    # Constructor
    def __init__(self):
        self.chain = [] # list of blocks - no blocks in it atm 
        self.create_block(proof = 1, previous_hash = '0') # create the genesis block
    
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof':proof,
                 'previous_hash': previous_hash}

        self.chain.append(block) # attach block to the chain
        return block

    def get_previous_block(self): # self as we need to grab the chain
        return self.chain[-1]

    # method to get proof of work - miners will need to solve this problem
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False # Sets to true when you find the solution
        
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
            
    def hash(self, block): # returns the cryptographic has of a block
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
        
    def is_chain_valid(self, chain):
        previous_block = chain[0] # get first block
        block_index = 1
        
        while block_index < len(chain): # go through the whole chain
            block = chain[block_index] # current block
            
            if block['previous_hash'] != self.hash(previous_block): # means previous hash doesnt match hash of previous block -  block is invalid!
                return False 
           
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            
            if hash_operation[:4] != '0000': # means first 4 chars of the hash isnt 0000
                return False
            
            previous_block = block
            block_index += 1
            
        return True # if no problems the chain is valid
            

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Create the web app - Flask
app = Flask(__name__)
    
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Create a blockchain - create instance of it
blockchain = Blockchain()


# Mining a new block
@app.route('/mine_block', methods=['GET']) # full URL = "http://127.0.0.1:5000/" according to flask documents - check on postman
# method for this part of the app
def mine_block():
    prev_block = blockchain.get_previous_block() #get prev block
    prev_proof = prev_block['proof'] # get prev proof of work
    proof = blockchain.proof_of_work(prev_proof) # current proof 
    prev_hash = blockchain.hash(prev_block)
    current_block = blockchain.create_block(proof, prev_hash) # block is appended and returned
    
    # create the response to return
    response = {'message': "Naisu! Block added to the chain!",
                'index': current_block['index'],
                'timestamp': current_block['timestamp'],
                'proof': current_block['proof'],
                'prev_hash': current_block['previous_hash']
                }
    
    return jsonify(response), 200
    
# get the blockchain
@app.route('/get_blockchain', methods=['GET'])
def get_full_blockchain():
    response = {'chain': blockchain.chain,
                'chain_length': len(blockchain.chain)}
    
    return jsonify(response), 200

@app.route('/is_valid', methods=['GET'])
def is_blockchain_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    response = {'is_valid': is_valid}
    return jsonify(response), 200

# Run the app - just copy-past from documentation for now - figure out something else later
app.run(host = '0.0.0.0', port = '5000')





