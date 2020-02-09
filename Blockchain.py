from _sha512 import sha512
from BlockchainCode import Block


# The class that will make use of the Block class and create the actual chain
class Blockchain:

    seed_hash = sha512("Genesis669666999".encode()).hexdigest()
    node_list = {}

    # The default constructor function for this class
    def __init__(self, chain=None, all_transactions=None):
        if all_transactions is None:
            all_transactions = []
        if chain is None:
            chain = []
        self.chain = chain
        self.all_transactions = all_transactions
        self.node_list = {
            "node1": 35500,
            "node2": 31000,
            "node3": 36500,
            "node4": 38000,
            "node5": 38500,
            "node6": 40000,
            "node7": 41000
        }

    # The genesis block which will be the starting of the chain; a parent block in some way
    def block_zero(self, node_id):
        # The genesis or zero block is initialized with a special key that is to be kept confidential
        # The previous hash for the Gen block is 0
        block = Block.Block([self.seed_hash], 0)
        self.chain.append(block)
        if self.validate_block(node_id):
            print("\nGENESIS BLOCK MINED!\n")
        else:
            print("\nGENESIS BLOCK CANNOT BE MINED!\n")

        return [self.chain, self.seed_hash]

    # The function that adds new blocks to the existing chain
    def add_block(self, transactions, node_id):

        import pymysql.cursors
        mysql_conn = pymysql.connect(host="localhost",
                                     user="root",
                                     password="Akhilesh@1997",
                                     db="user_information",
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        previous_block_hash = ""
        print(self.chain, len(self.chain))
        try:
            with mysql_conn.cursor() as cursor:
                sql = "select blockname from %s"%(node_id)
                print(sql)
                cursor.execute(sql)
                block_height = len(cursor.fetchall())
            mysql_conn.commit()
            with mysql_conn.cursor() as cursor:
                sql = "select blockname from %s"%node_id+" limit %s, %s"
                print(type(block_height))
                cursor.execute(sql, (block_height-1, block_height))
        finally:
            mysql_conn.close()

        new_block = Block.Block(transactions, previous_block_hash)
        self.chain.append(new_block)
        return new_block

    # The function that validates the new blocks by comparing hashes
    def validate_block(self, node_id):
        import socket
        import pickle

        # Multicast the data to all blocks except the sender, for validation
        nodes = ["node1", "node2", "node3", "node4", "node5", "node6", "node7"]
        # you can send objects using pickle files
        dumping_variable = pickle.dumps(self.chain)
        chain_object = dumping_variable
        result = True
        print(nodes)
        for node in nodes:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if node != node_id:
                port = self.node_list[node]
                # print(port)
                try:
                    server_socket.connect(("127.0.0.1", port))
                    server_socket.send(bytes(node_id.encode()))
                    m1 = server_socket.recv(1024)

                    server_socket.send(chain_object)
                    m1 = server_socket.recv(1024)

                    server_socket.send(bytes(str(self.seed_hash).encode()))

                    result_string = str(server_socket.recv(1024))
                    result_from_one_node = False
                    if str(result_string) == "b\'True\'":
                        result_from_one_node = True
                    print("Message received: ", result_from_one_node)
                    result &= result_from_one_node

                    server_socket.close()
                except ConnectionRefusedError as ce:
                    print("In Blockchain: ", ce.strerror, ce.__traceback__)
        print("Out of the loop")
        return result

    # The function that will print the whole blockchain
    def print_block_chain(self):
        for block_index in range(len(self.chain)):
            current_block = self.chain[block_index]
            print("Block {} {} ".format(block_index, current_block))
            current_block.print_block_content()


if __name__ == '__main__':
    print("Yo")
    # bch = Blockchain()
    # bch.validate_block("Node1")
