# Blockchain Final Project
# Bhavik Naik (100617351), 

# main file that contains the chain, security, smart contracts, etc

import os
import binascii
import hashlib
import datetime
from Crypto.PublicKey import RSA
from flask import Flask, request, json, Response
from flask_cors import CORS

# flask app
app = Flask(__name__)
CORS(app)

class Blockchain: 
    """The blockchain class that includes all of the functions for the blockchain, 
    including the smart contracts and mining process. Also, it includes the various 
    functions to check that blockchain is correct. 
    """
    
    def __init__(self):
        """The Init function to create the blockchain and make the first block, 
        with the chain, wallets, and difficulity 
        """
        self.chain = []
        self.wallets = {}
        self.difficulty = 3
        self.add()
    
    @property
    def length(self):
        """The length function that will return the length of the blockchain 
        when using the built in len function in python

        Returns:
            int: the length of the blockchain
        """
        return len(self.chain)

    def add(self, transaction={}):
        """The add function that will take in the transaction dictionary (if provided)
        and it will call the create block function that will create the block. Then it 
        will mine the block and add it to the blockchain

        Args:
            transaction (dict, optional): The transaction dictionary that
            includes the various information that will be inputed in the blockchain. This 
            will include the smart contract that will be executed by the user.
            Defaults to {}.

        Returns:
            dictionary: the final block that will be added to the chain. This includes 
            the hash, signature, the transaction on it.
        """
        block = self._create_block(transaction)
        return self._mine(block)

    def _get_last_block_hash(self):
        """Returns the hash of the previous block

        Returns:
            string: the hash value of the last block
        """
        return self.chain[-1]['hash'] if len(self.chain) > 0 else None

    def _create_block(self, transaction):
        """The create block function creates the dictionary (json) object that 
        includes the information that needs to be present on the blockchain. This will be
        the object that will be added to the chain of blocks. The basic information is added
        here like the time, previous block hash, and the number of the block. It will 
        also add the transaction dictionary to the block.

        Args:
            transaction (dictionary): the transaction dictionary that includes the 
            transaction that has taken place by the user.

        Returns:
            dictionary (json): the block dictionary that will contain all of the information 
            for the block
        """
        return {
            'header': {
                'number': len(self.chain),
                'time': datetime.datetime.now(),
                'nonce': None,
                'previous_block': self._get_last_block_hash()  
            },
            'transaction': transaction, # add the transaction to the block
            'hash': None, 
            'public_key': None, 
            'signature': None
        }
    
    def _hash_data(self, data, forSign=False):
        """The hash data function takes in data and hashes it using SHA256. It takes in 
        either a dictionary and text and determines how to hash it.

        Args:
            data (string or dict): the data that we are going to hash 
            forSign (bool, optional): If we should hash for signing data. Defaults to False.

        Returns:
            string: the hash value of the data from SHA256
        """
        
        # check if the data is a dict and we want hash it in terms of numbers
        if isinstance(data, dict) and forSign:
            return int.from_bytes(hashlib.sha256(json.dumps(data,  
            indent=2).encode('utf-8')).digest(), byteorder='big')
        # hash the dictionary regularly
        elif isinstance(data, dict): 
            return hashlib.sha256(json.dumps(data, sort_keys = True).encode("utf-8")).hexdigest()
        else:
            # otherwise, hash it as a string
            return str(hashlib.sha256(str(data).encode('utf-8')).hexdigest())

    def _mine(self, block): 
        """The mine function takes in the block from create block, and then does the proof of work to 
        verify the block. It makes sure that the hash starts with as number as 0s as the difficulity is 
        requested. It then signs the block with the user's private and public key. It then pops out the private
        key from the transaction object, and hashes the whole transaction object because we do not want 
        people seeing what type of information is being created by users. It then appends it to the chain.

        Args:
            block (dictionary): the block object created from create_block

        Returns:
            dictionary (json): the block object that is appended to the chain
        """
        while True: 
            #generate a nonce
            block['header']["nonce"] = binascii.b2a_hex(os.urandom(32)).decode('utf-8')
            # hash the data and make sure that it starts with difficulity 0s
            block['hash'] = self._hash_data(block['header'])
            if str(block['hash'])[:self.difficulty] == '0' * self.difficulty:
                break
        # make sure it isnt the first block
        if block['header']['number'] > 0: 
            # sign the data with the user's private / public key 
            block['signature'] = pow(self._hash_data(block['header'], True), block['transaction']['private_key'], 
                block['transaction']['public_key'])
            # remove the private key 
            block['transaction'].pop('private_key', None)
            # set the public key of the user who is exectuing the command 
            block['public_key'] = block['transaction']['public_key']
            # hash the transaction
            block['transaction'] = self._hash_data(block['transaction'])
        # append the block to the chain
        self.chain.append(block)
        print(block)
        return block

    def create_wallet(self, name, address, inventory):
        """The create wallet function takes in the information of the client and generates a private and 
        public key for that user. 

        Args:
            name (string): the name of the client
            address (string): the address of the client 
            inventory (dictionary): the list of inventory that the client wants to store intially 

        Returns:
            dictionary (json): the wallet's public and private keys
        """
        # generate the keypair  
        keyPair = RSA.generate(bits=1024)
        wallet = {
            'public_key': keyPair.n,
            'private_key': self._hash_data(keyPair.d), # hash the private key because we do not want people seeing it
            'name': name, 
            'address': address,
            'inventory': inventory
        }
        # add the wallet to the wallet dictionary
        self.wallets[wallet['public_key']] = wallet
        return {'publicKey':str(keyPair.n), 'privateKey': str(keyPair.d)}

    def _check_information(self, userPublic, userPrivate):
        """The check_information function makes sure that the public and private key are correct that user 
        inputted in the smart contract

        Args:
            userPublic (int): the public key that the user inputted 
            userPrivate (int): the private key that the user inputted

        Returns:
            string or boolean: returns the error or true if it is accepted
        """
        # check to make sure that public key is in the wallet   

        if userPublic in self.wallets: 
            # check to see if the private key is correct
            if self._hash_data(userPrivate) != \
            self.wallets[userPublic]['private_key']: 
                return "Private key is incorrect!"
        else: 
            return "User not found! Try public key again"
        return True

    def check_integrity(self):
        """The check integrity function loops to the chain and makes sure that hash values of the 
        blocks match the hash value of the previous block

        Returns:
            string or list: returns ok if it is fine or a list of issues if it is not
        """
        results = []
        # loop through the chain
        for block in reversed(self.chain):
            block_number = block['header']['number']
            # checks to see if the hash of the data matches the hash that is stored 
            if not block['hash'] == self._hash_data(block['header']):
                results.append(f'block-{block_number}: invalid hash')
            if block_number > 0:
                # checks to see if the previous hash matches
                previous_block = self.chain[block_number - 1]
                if not block['header']['previous_block'] == \
                previous_block['hash']:
                    results.append(f'block-{block_number}: \
                        invalid block pointer')
        return "ok" if not results else results

    def check_signatures(self): 
        """The check signatures loops through the chain and makes sure that the signature matches 
        with the block data

        Returns:
            string or list: returns ok if it is fine or a list of issues if it is not
        """
        results = []
        # loop through the chain
        for block in reversed(self.chain):
            block_number = block['header']['number']
            if block_number == 0: 
                # if it is the first one, it wont have a signature
                break
            # construct the hash of the header
            hashed_blockHeader = self._hash_data(block['header'], True)
            # verify the signature
            signHash = pow(block['signature'], 65537, block['public_key'])
            # if it doesnt match, add it to the results
            if not signHash == hashed_blockHeader:
                results.append(f'block-{block_number}: invalid signature')
        return "ok" if not results else results

    def get_all_inventory(self, publicKey, privateKey):
        """First smart contract. The user puts their private and public keys to get all of the inventory
        that they have in the system. Private key is required so that there is access control and someone 
        cannot just get the inventory for a wallet that they are not the user of.

        Args:
            publicKey (int): the public key of the user
            privateKey (int): the private key of the user

        Returns:
            dictionary: returns all of the inventory that the user has 
        """
        # make sure that user's public and private keys are correct
        verify = self._check_information(publicKey, privateKey)
        if verify and isinstance(verify, bool):
            # return the inventory
            return self.wallets[publicKey]['inventory']
        else: 
            return {'error': verify} 

    def get_inventory(self, publicKey, privateKey, item):
        """The second smart contract. The user puts their private and public keys to get the stock of a 
        single item in their inventory. Private key is required so that there is access control and someone 
        cannot just get the inventory for a wallet that they are not the user of.

        Args:
            publicKey (int): the public key of the user
            privateKey (int): the private key of the user
            item (string): the item that they want to get the stock of

        Returns:
            dictionary: returns the dictionary with the item name and the number. Or a number.
        """
        # make sure that user's public and private keys are correct
        verify = self._check_information(publicKey, privateKey)
        if verify and isinstance(verify, bool): 
            # return the dictionary with the item name the stock if it is found in the inventory
            return {item: self.wallets[publicKey]['inventory'][item]} if item in \
                self.wallets[publicKey]['inventory'] else {'error': "Item not found"} 
        else: 
            return {'error': verify} 

    def add_inventory(self, publicKey, privateKey, item, amount): 
        """The third smart contract. The user can add stock to an item in the inventory. This will then be 
        created into a transaction and then sent to be added to the blockchain. 

        Args:
            publicKey (int): the public key of the user
            privateKey (int): the private key of the user
            item (string): the item that they want to add stock to
            amount (int): the amount of stock that they want to add to the item

        Returns:
            dictionary: returns the information and the block that was created
        """
        # make sure that user's public and private keys are correct
        verify = self._check_information(publicKey, privateKey)
        if verify and isinstance(verify, bool): 
            # do the checks to make sure that amount is valid
            if not amount > 0: 
                return {"error": "Amount not valid"}
            # add the stock to the item. If the item does not exist, create it
            if item in self.wallets[publicKey]['inventory']: 
                self.wallets[publicKey]['inventory'][item] =  \
                str(int(self.wallets[publicKey]['inventory'][item]) + amount)
            else: 
                self.wallets[publicKey]['inventory'][item] = amount
            # create the transaction object with the information
            transaction = { 
                'public_key': publicKey, 
                "private_key": privateKey, 
                "contract name": 'Add Inventory',
                "amount": amount, 
                "item": item, 
                item + ' new stock': self.wallets[publicKey]['inventory'][item]
                }
            # create the block and add it to the chain
            block = self.add(transaction)
            # return the inforamtion
            return {
                'message': 'Added to blockchain', 
                'item': item, 
                'itemtotal': self.wallets[publicKey]['inventory'][item],
                'number': block['header']['number'],
                'name': self.wallets[publicKey]['name']
                }
        else: 
            return {'error': verify}

    def remove_inventory(self, publicKey, privateKey, item, amount): 
        """The fourth smart contract. The user can remove stock to an item in the inventory. This will then be 
        created into a transaction and then sent to be added to the blockchain. 

        Args:
            publicKey (int): the public key of the user
            privateKey (int): the private key of the user
            item (string): the item that they want to remove stock to
            amount (int): the amount of stock that they want to remove to the item

        Returns:
            dictionary: returns the information and the block that was created
        """
        # make sure that user's public and private keys are correct
        verify = self._check_information(publicKey, privateKey)
        if verify and isinstance(verify, bool): 
            # do the checks to make sure that amount is valid
            if not amount > 0: 
                return {"error": "Amount not valid"}
            # make sure that item is in the inventory or return an error
            if item in self.wallets[publicKey]['inventory']: 
                if int(self.wallets[publicKey]['inventory'][item]) == 0: 
                    return {"error": "Item is already at 0"}
                # remove the stock to the item. 
                self.wallets[publicKey]['inventory'][item] = \
                str(int(self.wallets[publicKey]['inventory'][item]) - amount)
                # if it goes below 0, then set it 0.
                if int(self.wallets[publicKey]['inventory'][item]) < 0: 
                    self.wallets[publicKey]['inventory'][item] = 0
                # create the transaction object with the information
                transaction = { 
                'public_key': publicKey, 
                "private_key": privateKey, 
                "contract name": 'Remove Inventory',
                "amount": amount, 
                "item": item, 
                item + ' new stock': self.wallets[publicKey]['inventory'][item]
                }
                # create the block and add it to the chain
                block = self.add(transaction)
                return {
                'message': 'Added to blockchain', 
                'item': item, 
                'itemtotal': self.wallets[publicKey]['inventory'][item],
                'number': block['header']['number'],
                'name': self.wallets[publicKey]['name']
                }
            else:
                return {"error": "Item not found"}
        else: 
            return {'error': verify}

    def delete_inventory(self, publicKey, privateKey, item): 
        """The fifth smart contract. The user can delete an item in the inventory. This will then be 
        created into a transaction and then sent to be added to the blockchain. 

        Args:
            publicKey (int): the public key of the user
            privateKey (int): the private key of the user
            item (string): the item that they want to delete

        Returns:
            dictionary: returns the information and the block that was created
        """
        # make sure that user's public and private keys are correct
        verify = self._check_information(publicKey, privateKey)
        if verify and isinstance(verify, bool): 
            # make sure that item is in the inventory or return an error
            if item in self.wallets[publicKey]['inventory']: 
                # remove the item
                self.wallets[publicKey]['inventory'].pop(item)
                # create the transaction object with the information
                transaction = { 
                'public_key': publicKey, 
                "private_key": privateKey, 
                "contract name": 'Delete Inventory', 
                "item": item
                }
                # create the block and add it to the chain
                block = self.add(transaction)
                return {
                    'message': 'Added to blockchain', 
                    'number': block['header']['number'],
                    'name': self.wallets[publicKey]['name']
                }
            else: 
                return {"error": "Item not found"}
        else: 
            return {'error': verify}

# -------------------------- FLASK ROUTES ------------------------------- #

@app.route('/api/blockchain', methods=['GET'])
def get_blockchain_info():
    """The get_blockchain_info returns the various checks that are creatd to make sure that 
    the chain is still secure. This includes checking the hashes and signatures. It also returns 
    the length of the chain.

    Returns:
        Dictionary (json): the json response to running the various functions.
    """
    return Response(
        response=json.dumps({
            'length': blockchain.length,
            'validity': blockchain.check_integrity(),
            'signature_validity': blockchain.check_signatures(),
        }),
        status=200,
        mimetype='application/json'
    )

@app.route('/api/blockchain/block/<int:number>', methods=['GET'])
def get_block(number):
    """The get block function is a GET call which the user can put in the number of the block, 
    and get back the information about that block. 

    Args:
        number (int): the block number that they want to see information about

    Returns:
        json: the block dictionary gets returned 
    """
    return Response(
        response=json.dumps(
            blockchain.chain[number] if number < len(blockchain.chain) else None
        ),
        status=200,
        mimetype='application/json'
    )  

@app.route('/api/blockchain/wallet', methods=['POST'])
def add_wallet():
    """The add wallet function is used to create a wallet for the user. It first checks to 
    make sure that the required variables are there and then calls the create wallet function 
    which returns back the private and public key. 

    Returns:
        json: the wallet dictionary that includes the private and public keys
    """
    # parse the data 
    jsonData = request.get_json()
  
    return Response(
        response=json.dumps(
            # call the create wallet function with the parameters sent by the user.
            blockchain.create_wallet(
                jsonData['name'],
                jsonData['address'],
                jsonData['inventory']
            ) 
        ),
        status=200,
        mimetype='application/json'
    )
    
@app.route('/api/blockchain/getAllInventory', methods=['POST'])
def get_all_inventory():
    """The get all inventory is the first smart contract. It first checks to 
    make sure that the required variables are there and then calls the get_all_inventory function 
    which returns back all of the inventory in the wallet of that user

    Returns:
        json: the response to the get all inventory smart contract 
    """
    # parse the data  
    jsonData = request.get_json()

    return Response(
        response=json.dumps(
            # call the get_all_inventory function with the parameters sent by the user.
            blockchain.get_all_inventory(
                int(jsonData['publicKey']),
                int(jsonData['privateKey']),
            )
        ),
        status=200,
        mimetype='application/json'
    )
    
@app.route('/api/blockchain/getInventory', methods=['POST'])
def getInventory():
    """The get inventory is the second smart contract. It first checks to 
    make sure that the required variables are there and then calls the get_inventory function 
    which returns back  the inventory in the wallet of that user

    Returns:
        json: the response to the get_inventory smart contract 
    """
    # parse the data  
    jsonData = request.get_json()

    return Response(
        response=json.dumps(
            # call the get_all_inventory function with the parameters sent by the user.
            blockchain.get_inventory(
                int(jsonData['publicKey']),
                int(jsonData['privateKey']),
                jsonData['item']
            )
        ),
        status=200,
        mimetype='application/json'
    )

@app.route('/api/blockchain/addInventory', methods=['POST'])
def addInventory():
    """The add inventory is the third smart contract. It first checks to 
    make sure that the required variables are there and then calls the add inventory function 
    which creates a transaction and returns back the block and other data

    Returns:
        json: the response to the add_inventory smart contract 
    """
    # parse the data  
    jsonData = request.get_json()

    return Response(
        response=json.dumps(
            # call the get_all_inventory function with the parameters sent by the user.
            blockchain.add_inventory(
                int(jsonData['publicKey']),
                int(jsonData['privateKey']),
                jsonData['item'], 
                int(jsonData['amount'])
            )
        ),
        status=200,
        mimetype='application/json'
    )

@app.route('/api/blockchain/removeInventory', methods=['POST'])
def removeInventory():
    """The remove inventory is the fourth smart contract. It first checks to 
    make sure that the required variables are there and then calls the remove inventory function 
    which creates a transaction and returns back the block and other data

    Returns:
        json: the response to the remove_inventory smart contract 
    """
    # parse the data  
    jsonData = request.get_json()

    return Response(
        response=json.dumps(
            # call the get_all_inventory function with the parameters sent by the user.
            blockchain.remove_inventory(
                int(jsonData['publicKey']),
                int(jsonData['privateKey']),
                jsonData['item'], 
                int(jsonData['amount'])
            )
        ),
        status=200,
        mimetype='application/json'
    )

@app.route('/api/blockchain/deleteInventory', methods=['POST'])
def delete_inventory():
    """The delete inventory is the fifth smart contract. It first checks to 
    make sure that the required variables are there and then calls the delete inventory function 
    which creates a transaction and returns back the block and other data

    Returns:
        json: the response to the delete_inventory smart contract 
    """
    # parse the data  
    jsonData = request.get_json()

    return Response(
        response=json.dumps(
            # call the get_all_inventory function with the parameters sent by the user.
            blockchain.delete_inventory(
                int(jsonData['publicKey']),
                int(jsonData['privateKey']),
                jsonData['item']
            )
        ),
        status=200,
        mimetype='application/json'
    )

if __name__ == '__main__':
    # create the blockchain object
    blockchain = Blockchain()
    # run the flask app
    app.run(host='127.0.0.1', port=8080, debug=1)
