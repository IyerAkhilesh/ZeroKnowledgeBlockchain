import csv
from BlockchainCode import Blockchain
import hmac
from hashlib import sha512


class Node2:

    bch = None
    gen = None
    block_table = "node2"
    zero_hash = ""

    def __init__(self):
        self.bch = Blockchain.Blockchain()

    def genesis(self):
        self.gen, self.zero_hash = self.bch.block_zero("Node2")
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

        # Access and insert the first block in the database "user_information" and table node2
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
                sql = "INSERT INTO `node2` (`blockname`, `blockdata`) VALUES (%s, %s)"
                cursor.execute(sql, (str(blockname), str(block_data)))
            conn.commit()
        finally:
            conn.close()
        self.gen_flag = True

    def mine_block(self, txn):
        # Adding the block to a virtual blockchain
        new_block = self.bch.add_block(txn, "Node2")

        # Validating it with other nodes and the network logic and appending it to the actual, if validated successfully
        if self.bch.validate_block("Node2"):
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
            # Access and insert the newest block in the database "user_information" and table node2
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
                    sql = "INSERT INTO `node2` (`blockname`, `blockdata`) VALUES (%s, %s)"
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


n1 = Node2()
# Access and insert the first block in the database "user_information" and table node2
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
        sql = "SELECT * FROM `node2`"
        cursor.execute(sql)
        if len(list(cursor.fetchall())) == 0:
            n1.genesis()
            print("Genesis done")

        else:
            n1.mine_block(["Akhilesh: Iyer", "Vignesh: Iyer", "Shikha: Doshi"])
            n1.mine_block(["Grocery: 50", "Travel: 104"])
            n1.mine_block(["Grocery: 50", "Travel: 101"])
            n1.mine_block(["Peeping: Tom", "Running: Jerry"])

    conn.commit()
finally:
    conn.close()

# n1.print_blockchain()
