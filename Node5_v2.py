from BlockchainCode import Blockchain

class Node5:

    worker_node_dict = {
        "node1": 50200,
        "node2": 20500,
        "node3": 21000,
        "node4": 21500,
        "node5": 22000,
        "node6": 22500,
        "node7": 23000
    }
    transactions = []
    bch = None
    gen = None
    block_table = "node5"
    zero_hash = ""

    def __init__(self):
        self.bch = Blockchain.Blockchain()

    def genesis(self):
        self.gen, self.zero_hash = self.bch.block_zero("node5")
        blockname = self.gen[0].hash
        block_data = [
            self.gen[0].hash,
            "0",
            self.gen[0].timestamp,
            self.gen[0].nonce,
            "0",
            self.gen[0].transactions,
            len(self.gen[0].transactions[0])
        ]

        # Access and insert the first block in the database "user_information" and table node5
        import pymysql.cursors
        conn = pymysql.connect(host="localhost",
                               user="root",
                               password="Akhilesh@1997",
                               db="user_information",
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)
        try:
            with conn.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `node5` (`blockname`, `blockdata`) VALUES (%s, %s)"
                cursor.execute(sql, (str(blockname), str(block_data)))
            conn.commit()
        finally:
            conn.close()
        self.gen_flag = True

    def mine_block(self, txn):
        # Adding the block to a virtual blockchain
        new_block = self.bch.add_block(txn, "node5")

        # Validating it with other nodes and the network logic and appending it to the actual, if validated successfully
        if self.bch.validate_block("node5"):
            new_block_data = [
                new_block.hash,
                "0",
                new_block.timestamp,
                new_block.nonce,
                "0",
                new_block.transactions,
                len(new_block.transactions[0])
            ]

            new_blockname = new_block.block_identifier(new_block.transactions)
            # Access and insert the newest block in the database "user_information" and table node5
            import pymysql.cursors
            conn = pymysql.connect(host="localhost",
                                   user="root",
                                   password="Akhilesh@1997",
                                   db="user_information",
                                   charset='utf8mb4',
                                   cursorclass=pymysql.cursors.DictCursor)
            try:
                with conn.cursor() as cursor:
                    # Create a new record
                    sql = "INSERT INTO `node5` (`blockname`, `blockdata`) VALUES (%s, %s)"
                    cursor.execute(sql, (str(new_blockname), str(new_block_data)))
                conn.commit()
            finally:
                conn.close()

        else:
            # Print an error message
            print("CANNOT MINE BLOCK!")
            return


    def print_blockchain(self):
        self.bch.print_block_chain()

    def register_node(self, worker_node_id):
        from BlockchainCode import SumProductSum as prng
        import socket
        import pickle

        username = input("Enter the username: ")
        password = input("Enter the password: ")
        exponents = prng.get_factors(username, password)
        exponents =str(exponents[0])+","+str(exponents[1])+","+str(exponents[2])
        dump_var = pickle.dumps(exponents)

        try:
            sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Port ", self.worker_node_dict[worker_node_id])
            sender_socket.connect(("127.0.0.1", self.worker_node_dict[worker_node_id]))
            self.transactions.append(self.block_table+"->"+worker_node_id+"->"+str(exponents))
            sender_socket.send(dump_var)
            dump_var = sender_socket.recv(1024)
            powers = pickle.loads(dump_var)
            self.transactions.append(worker_node_id+"->"+self.block_table+"->"+str(powers))
            print(self.transactions)
            sender_socket.close()
        except ConnectionRefusedError as cr:
            print(cr)


n1 = Node5()
# Access and insert the first block in the database "user_information" and table node5
import pymysql.cursors
conn = pymysql.connect(host="localhost",
                       user="root",
                       password="Akhilesh@1997",
                       db="user_information",
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)
try:
    with conn.cursor() as cursor:
        # Create a new record
        sql = "SELECT * FROM `node5`"
        cursor.execute(sql)
        if len(list(cursor.fetchall())) == 0:
            n1.genesis()
            print("Genesis done")

        else:
            # Registration
            registered_flag = n1.register_node("node1")
            print("Registration status: ",registered_flag)
            # n1.mine_block(["username: people", "password: areAlive"])
            # n1.mine_block(["Akhilesh: Iyer", "Vignesh: Iyer", "Shikha: Doshi"])
            # n1.mine_block(["Grocery: 50", "Travel: 104"])
            # n1.mine_block(["Grocery: 50", "Travel: 101"])
            # n1.mine_block(["Peeping: Tom", "Running: Jerry"])

    conn.commit()
finally:
    conn.close()

# n1.print_blockchain()
