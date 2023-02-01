# Blockchain
#### Blockchain - Final Project 
#### November 24, 2021

**Title:**
Blockchain inventory management system 

**Goal:**
The goal was to create a custom blockchain inventory management software using smart contracts, a web interface, and security. 

**Technologies Used:**
Python, [Flask](https://flask.palletsprojects.com/en/2.2.x/), Hashlib, RSA, HTML, JavaScript, Jquery, CSS, Bootstrap 

**Result:**
With a simple Bootstrap web interface, the application worked to connect to the Flask API and perform the actions that you expect an inventory management system to do. These actions were created as smart contracts and ran on custom made blockchain. 

There are 9 files in this directory. 8 of these are html files which allows the users to interact with the app. The main.py file contains the source code of the blockchain network and Flask routes. 

**Run through:**

1) The user first creates a wallet which housed information relating to the business, such as the name, addresses, and also the initial inventory that the user wants to start off with. This was taken as a list. 
2) Once that is confirmed, the program uses RSA to generate a public and private key for that user. It instructs the user to keep the private key safe and will be needed when performing actions on the blockchain. 
3) The user then is greeted with various functions that they can perform, such as add inventory, remove inventory, and delete inventory. They also have functions for "get all inventory" which returned the values for all of the products stored, and "get inventory" which returned the value of a single piece of inventory. 
4) When using the add, remove, or delete inventory, once the data was been validated, the blockchain will create a new block containing the updated inventory of specific products. All of these functions will return back the new block that was created and the new inventory number for the product that the user requested to change. These are all POST calls done using Flask routes. 
5) When adding blocks to the chain, there is work being done to ensure that the block has been validated before adding. This is done using SHA256. Each block contains a nonce value is being updated which changes the hash value of that block. The difficulty variable indicates how many 0s the hash value should start with to "validate" the block. 
6) Each block is also being signed with the user's private and public keys to ensure that the data is accurate. 
7) The user also has the option to check the validity of the blockchain which makes sure that the each block is linked correctly and previous hash values relate to the previous block to ensure tha the chain has not been tampered with. 
8) The user can also get information for a single block on the blockchain. Of course, the contents that were added to the block are hashed, but the user can ensure that the new information has been added successfully. 