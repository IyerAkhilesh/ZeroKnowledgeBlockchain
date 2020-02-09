# import csv
# import hmac
# from _sha512 import sha512
import random
import socket
import pickle

try:
    while True:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allows the resuse of socket address
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        client_socket.bind(("127.0.0.1", 36500))
        client_socket.listen(50)
        conn, addr = client_socket.accept()
        print("Connection established by Node 3")

        node_id = str(conn.recv(1024)).replace("b\'", "")
        conn.send(bytes("ack".encode()))

        node_id = node_id.replace("\'", "")

        chain_object = conn.recv(1024)
        chain = pickle.loads(chain_object)
        conn.send(bytes("ack".encode()))

        """
            To check if the block has already been mined
            The block name is produced by hashing the transactions in the current block with the Gen hash
            This will make it unique and non-replicable
        """
        zero_hash = conn.recv(1024)
        is_block_mined = True

        # Access and insert the first block in the database "user_information" and table node3
        import pymysql.cursors

        mysql_conn = pymysql.connect(host="localhost",
                               user="root",
                               password="Akhilesh@1997",
                               db="user_information",
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)

        rows = []
        try:
            with mysql_conn.cursor() as cursor:
                sql = "select * from `node3`"
                cursor.execute(sql)
                rows = cursor.fetchall()
            mysql_conn.commit()
        except pymysql.MySQLError as message:
            print(message)
            pass

        if len(rows) == 0:

            current_hash_validity = chain[0].hash == chain[0].generate_hash()
            previous_hash_validity = True
            new_block_data = [
                chain[0].hash,
                "0",
                chain[0].timestamp,
                chain[0].nonce,
                "0",
                chain[0].transactions,
                len(chain[0].transactions[0])
            ]
            new_blockname = chain[0].generate_hash()
            try:
                with mysql_conn.cursor() as cursor:
                    sql = "INSERT INTO `node3` (`blockname`, `blockdata`) VALUES (%s, %s)"
                    cursor.execute(sql, (str(new_blockname), str(new_block_data)))
                mysql_conn.commit()
            except pymysql.IntegrityError as message:
                print(message)
                is_block_mined = False
                pass


        else:
            new_blockname = chain[len(chain)-1].block_identifier(chain[len(chain)-1].transactions)
            current_hash_validity = chain[len(chain) - 1].hash == chain[len(chain) - 1].generate_hash()
            print("Length of chain", len(chain), "\nChain: ", chain)
            random_height = random.randint(0, len(chain) - 1)
            previous_hash_validity = chain[random_height].hash == chain[random_height].generate_hash()

            block_names=[]
            try:
                with mysql_conn.cursor() as cursor:
                    sql = "select blockname from `node3` "
                    cursor.execute(sql)
                    block_names = cursor.fetchall()
                mysql_conn.commit()
            except pymysql.MySQLError as message:
                print(message)
                pass

            # for i in range(0, len(reader)):
            if new_blockname in block_names:
                print("Block name exists")
                is_block_mined = False
                break
            else:
                new_block_data = [
                    chain[len(chain) - 1].hash,
                    "0",
                    chain[len(chain) - 1].timestamp,
                    chain[len(chain) - 1].nonce,
                    "0",
                    chain[len(chain) - 1].transactions,
                    len(chain[len(chain) - 1].transactions[0])
                ]

                try:
                    with mysql_conn.cursor() as cursor:
                        sql = "insert into `node3` (`blockname`, `blockdata`) VALUES (%s, %s)"
                        cursor.execute(sql, (str(new_blockname), str(new_block_data)))
                    mysql_conn.commit()
                except pymysql.IntegrityError as message:
                    print(message)
                    is_block_mined = False
                    pass

                finally:
                    mysql_conn.close()

        result = str(is_block_mined & current_hash_validity & previous_hash_validity)
        print("Final: ", result)
        conn.send(bytes(result.encode()))
        # conn.close()

except ConnectionRefusedError as ce:
    print("In Node 3: ", ce.__traceback__)

