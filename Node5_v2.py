from BlockchainCode import Blockchain

class Node5:

    worker_node_dict = {
        "node1": 50200,
        "node2": 50500,
        "node3": 51000,
        "node4": 51500,
        "node5": 52000,
        "node6": 52500,
        "node7": 53000
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

            sender_socket.send(bytes("ack".encode()))
            registration_result = sender_socket.recv(512)
            sender_socket.send(bytes("ack".encode()))
            powers = pickle.loads(dump_var)
            self.transactions.append(worker_node_id+"->"+self.block_table+"->"+str(powers))
            print(self.transactions)
            sender_socket.close()

            if "True" in str(registration_result.decode()):
                return "Successful!"
            else:
                return "Unsuccessful!"

        except ConnectionRefusedError as cr:
            print(cr)

    # the login function with parameters as the IDs of nodes that will serve the functions
    # of containers and authenticator FaaS servers
    def login(self, container1,  container2, container3, container4, authenticator1, authenticator2):
        from BlockchainCode import SumProductSum as prng

        username = input("Enter the username: ")
        password = input("Enter the password: ")
        exponents = prng.get_factors(username, password)
        print("Exponents array: ", exponents)
        # exponents = str(exponents[0]) + "," + str(exponents[1]) + "," + str(exponents[2])

        # send first value to container one and get back the exponent
        X = self.send_to_container(container1, str(exponents[0]))

        # send second value to container two and get back the exponent
        Y = self.send_to_container(container2, str(exponents[1]))
        print("Powers returned by container servers: ", X, Y)

        # send first power, response one process from
        # pass_number and first user number to authenticator one and get back result one
        R_ONE = self.send_to_authenticator(authenticator1, X, exponents[2], exponents[0])

        # send second power, response one process from
        # pass_number and second user number to authenticator two and get back result two
        R_TWO = self.send_to_authenticator(authenticator2, Y, exponents[2], exponents[1])
        print("Results returned by authentication servers: ", R_ONE, R_TWO)

        return R_ONE & R_TWO

    def send_to_authenticator(self,container_id, power, exponent1, exponent2):
        import socket
        import pickle

        dump_var = pickle.dumps(power)
        try:
            sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sender_socket.connect(("127.0.0.1", self.worker_node_dict[container_id]))

            self.transactions.append(self.block_table + "->" + container_id + "->" + str(power))
            sender_socket.send(dump_var)

            # what is received is challenge nb
            dump_var = sender_socket.recv(1024)
            nb = pickle.loads(dump_var)
            print("Challenge: ", nb)

            # what is calculated is response r
            r = int(nb) * exponent1 + exponent2
            print("Response: ", r)
            dump_var = pickle.dumps(r)
            sender_socket.send(dump_var)

            transaction_result = sender_socket.recv(1024)
            sender_socket.send(bytes("ack".encode()))

            self.transactions.append(container_id + "->" + self.block_table + "->" + str(power))
            sender_socket.close()
            print(self.transactions)

            if "True" in str(transaction_result.decode()):
                print("Hello there! Your chances of logging in successfully are 50% more now!")
                return True
            else:
                print("I am sorry! You can't login now!")
                return False
        except ConnectionRefusedError as cr:
            print(cr)

    def send_to_container(self, container_id, exponent):
        import socket
        import pickle

        print("Exponent sent to "+container_id, exponent)
        dump_var = pickle.dumps(exponent)

        try:
            sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Port ", self.worker_node_dict[container_id])
            sender_socket.connect(("127.0.0.1", self.worker_node_dict[container_id]))
            self.transactions.append(self.block_table + "->" + container_id + "->" + str(exponent))
            sender_socket.send(dump_var)
            dump_var = sender_socket.recv(1024)

            sender_socket.send(bytes("ack".encode()))
            transaction_result = sender_socket.recv(512)
            sender_socket.send(bytes("ack".encode()))
            power = pickle.loads(dump_var)
            self.transactions.append(container_id + "->" + self.block_table + "->" + str(power))
            sender_socket.close()
            print(self.transactions)

            if "True" in str(transaction_result.decode()):
                print("Hello there! This is your first transaction!")
                return str(power)
            else:
                print("Congratulations: You have logged in more than once!")
                return str(power)
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
            # registered_flag = n1.register_node("node1")
            # print("Registration status: ",registered_flag)

            # Login
            login_result = n1.login("node1", "node3", "", "", "node6", "node7")
            if login_result:
                print("Whoa! You made it! Welcome to Zero Knowledge Blockchain!")
            else:
                print("I am sorry! Nobody wants you in! Try registering the next time! ;-)")
    conn.commit()
finally:
    conn.close()

# n1.print_blockchain()
