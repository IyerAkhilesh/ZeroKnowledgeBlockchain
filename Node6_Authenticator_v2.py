import math
import socket
import pickle
from BlockchainCode import SumProductSum as prng

def mine_block(txn):
    from BlockchainCode import Blockchain

    bch = Blockchain.Blockchain()
    # Adding the block to a virtual blockchain
    new_block = bch.add_block(txn, "node1")

    # Validating it with other nodes and the network logic and appending it to the actual, if validated successfully
    if bch.validate_block("node1"):
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
        # Access and insert the newest block in the database "user_information" and table node1
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
                sql = "INSERT INTO `node1` (`blockname`, `blockdata`) VALUES (%s, %s)"
                cursor.execute(sql, (str(new_blockname), str(new_block_data)))
            conn.commit()
        finally:
            conn.close()
        return True
    else:
        # Print an error message
        print("CANNOT MINE BLOCK!")
        return False


GENERATOR = 3
try:
    # while True:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Allows the reuse of socket address
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    client_socket.bind(("127.0.0.1", 52500))
    client_socket.listen(50)
    connection, address = client_socket.accept()
    print("Connection established by Node 6 - Authenticator")

    # the first power corresponding to the username: X
    dump_var = connection.recv(1024)
    X = pickle.loads(dump_var)

    import pymysql.cursors

    conn = pymysql.connect(host="localhost",
                           user="root",
                           password="Akhilesh@1997",
                           db="user_information",
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
    relevant_row = []
    try:
        with conn.cursor() as cursor:
            # Create a new record
            sql = "SELECT `blockdata` FROM `node6` `blockdata` WHERE `blockdata` like '{}'".format('%{0}%'.format(X[1:len(X)-1]))
            print(sql)
            cursor.execute(sql)
            relevant_row = cursor.fetchall()
        conn.commit()
    finally:
        conn.close()
    print(relevant_row)

    Nb = math.floor(pow(5, math.e * 9 / 2)) % 100000000
    Nb_factors = prng.factors(Nb)
    nb1 = Nb_factors[math.floor(len(Nb_factors)/2) - 1]

    # the first part of the challenge: nb1
    dump_var = pickle.dumps(nb1)
    connection.send(dump_var)

    # the first part of the repsonse r1
    dump_var = connection.recv(1024)
    r1 = pickle.loads(dump_var)

    connection.send(bytes("False".encode()))
    ack = connection.recv(1024)

    client_socket.close()
except ConnectionRefusedError as cr:
    print(cr)
except OverflowError as oe:
    print(oe)
