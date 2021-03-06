import socket
import pickle


def mine_block(txn):
    from BlockchainCode import Blockchain

    bch = Blockchain.Blockchain()
    # Adding the block to a virtual blockchain
    new_block = bch.add_block(txn, "node3")

    # Validating it with other nodes and the network logic and appending it to the actual, if validated successfully
    if bch.validate_block("node3"):
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
        # Access and insert the newest block in the database "user_information" and table node3
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
                sql = "INSERT INTO `node3` (`blockname`, `blockdata`) VALUES (%s, %s)"
                cursor.execute(sql, (str(new_blockname), str(new_block_data)))
            conn.commit()
        finally:
            conn.close()

    else:
        # Print an error message
        print("CANNOT MINE BLOCK!")
        return


GENERATOR = 3
try:
    # while True:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Allows the reuse of socket address
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    client_socket.bind(("127.0.0.1", 51000))
    client_socket.listen(50)
    conn, addr = client_socket.accept()
    print("Connection established by Node 3 - Power Raiser")

    dump_var = conn.recv(1024)
    exponent_string = pickle.loads(dump_var)
    powers, exponents = [], []
    transactions = []
    if "," in exponent_string:
        exponents = exponent_string.split(",")
        transactions.append(exponents)
        powers.append(pow(GENERATOR, int(exponents[0])))
        powers.append(pow(GENERATOR, int(exponents[1])))
        powers.append(pow(GENERATOR, int(exponents[2])))
        transactions.append(powers)
        dump_var_send = pickle.dumps(powers)
        conn.send(dump_var_send)
        conn.recv(512)

        print("Transactions: ", transactions)
        conn.send(bytes(str(mine_block(transactions)).encode()))
        conn.recv(512)

    else:
        powers.append(pow(GENERATOR, int(exponent_string)))
        transactions.append(exponents)
        transactions.append(powers)
        dump_var_send = pickle.dumps(powers)
        conn.send(dump_var_send)
        conn.recv(512)

        print("Transactions: ", transactions)
        conn.send(bytes("Its a login!".encode()))
        conn.recv(512)

    client_socket.close()
except ConnectionRefusedError as cr:
    print(cr)
except OverflowError as oe:
    print(oe)
