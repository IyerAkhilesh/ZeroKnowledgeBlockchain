import hmac
from hashlib import sha512
from datetime import datetime

# The actual block class which will be used to manufacture blocks
class Block:
    t_string = ""
    # The default constructor function of this class
    def __init__(self, transactions, previous_hash, nonce = 0):
        # Inititalizing these values
        """
        IN THE ACTUAL NETWORK, THE BLOCK WILL CONTAIN ONLY A HASH OF ANY TRANSACTION, AND NOT THE
        TRANSACTION ITSELF.
        THIS IS FOR CLARITY OF DEMONSTRATION ONLY.

        :param transactions: the transactions to be stored in the block
        :param previous_hash: the hash of the previous block
        :param nonce: the nonce which is calculated by an algorithm in the real world,
        but will always be 0 in this demo code
        """
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.timestamp = datetime.now() # Returns the current date in YYYY-MM-DD and time in HH:MM:SS(6) format
        self.hash = self.generate_hash()
        # the string representation of all transactions in the array "transactions"
        for txn in transactions:
            self.t_string += str(txn)

    # creates a unique identifier for a block, that stems from its transactions
    def block_identifier(self, transactions):
        # the string representation of all transactions in the array "transactions"
        for txn in transactions:
            self.t_string += str(txn)
        return hmac.new(bytes("|\\|0|)e$|2o(|<".encode()), self.t_string.encode(), sha512).hexdigest()

    # Generates a hash of the information stored in the block in the given format
    def generate_hash(self):
        # the hash parameter will be a string concatenation of the timestamp,
        # the string concatenation of all transactions, the hash of the previous block and the nonce
        content = str(self.timestamp) + str(self.transactions) + str(self.previous_hash) + str(self.nonce)
        hash_of_content = hmac.new(bytes(str(self.previous_hash).encode()), content.encode(), sha512).hexdigest()
        print("This is the content:", content, "\nThis is the hash: ", hash_of_content)
        return hash_of_content

    # Prints the contents of a block
    def print_block_content(self):
        print("Block content:\n")
        # object = Block()
        print("Current transactions: ",self.transactions)
        print("Previous hash: ",self.previous_hash)
        print("Current hash: ",self.generate_hash())