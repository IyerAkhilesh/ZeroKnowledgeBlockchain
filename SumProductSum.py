import math

# Import the below libraries if you are using a version of Python less than 3.8
# import functools
# import operator

class FactorService:
    # Defined as a class constant so it isn't recreated on every function call
    CHAR_MAP = {
        "a":3, "B":4, "c":5, "D":6, "e":7, "F":8, "g":9, "H":10, "i":11, "J":12, 
        "k":13, "L":14, "m":15, "N":16, "o":17, "P":18, "q":19, "R":20, "s":21, 
        "T":22, "u":23, "V":24, "w":25, "X":26, "y":27, "Z":28, "A":29, "b":30, 
        "C":31, "d":32, "E":33, "f":34, "G":35, "h":36, "I":37, "j":38, "K":39, 
        "l":40, "M":41, "n":42, "O":43, "p":44, "Q":45, "r":46, "S":47, "t":48, 
        "U":49, "v":50, "W":51, "x":52, "Y":53, "z":54, "0":55, "1":56, "2":57, 
        "3":58, "4":59, "5":60, "6":61, "7":62, "8":63, "9":64, "@":65, "-":66, 
        "_":67, "&":68, "$":69, "|": 70, "<": 71, ">": 72, "~": 73
    }

    @staticmethod
    def get_all_factors(n):
        """
        Optimized factorization.
        Iterates only up to sqrt(n) instead of n.
        Complexity: O(sqrt(n))
        """
        if n < 2: return []
        
        factors = set()
        # Use the sqrt() function if you are using a version of Python less than 3.8 
        # for i in range(2, int(math.sqrt(n)) + 1):

        # Else, use isqrt() - We only need to check up to the square root of n
        for i in range(2, int(math.isqrt(n)) + 1):
            if n % i == 0:
                factors.add(i)
                factors.add(n // i) # Add the pair immediately
        
        return sorted(list(factors))

    @classmethod
    def process_string(cls, s):
        """
        Calculates Sum (S) and Product (P) based on the map,
        then finds unique factors for both.
        """
        if not s:
            return []

        # Use a list comprehension to get values, defaulting to 0 if char not found
        # to prevent crashing
        values = [cls.CHAR_MAP.get(char, 0) for char in s]
        
        # 1. Sum of all characters
        val_sum = sum(values)

        # 2. Product of characters at odd indices

        odd_index_values = values[1::2]

        # Use the reduce() function if you are using a version of Python less than 3.8 
        # if odd_index_values:
        #     val_prod = functools.reduce(operator.mul, odd_index_values, 1)
        # else:
        #     val_prod = 0

        # Else, use prod() - Slicing [1::2] grabs odd indices. math.prod is faster than reduce.
        val_prod = math.prod(odd_index_values) if odd_index_values else 0

        # Get factors for both
        factors_sum = cls.get_all_factors(val_sum)
        factors_prod = cls.get_all_factors(val_prod)

        # Combine unique factors
        return sorted(list(set(factors_sum + factors_prod)))

    @staticmethod
    def extract_indices(factors, percent_index):
        """Safely gets an item from the list based on a percentage index."""
        if not factors:
            return 0 # Or handle error appropriately
        
        idx = int(len(factors) * percent_index)
        # Ensure we don't go out of bounds (logic from original code adjusted)
        idx = max(0, min(idx, len(factors) - 1))
        return factors[idx]

    @classmethod
    def get_factors(cls, username, password):
        # 1. Process Username
        u_factors = cls.process_string(username)
        if len(u_factors) < 2:
            print("Username yields too few factors.")
            return []

        # Logic from original: Middle two elements
        mid_idx = len(u_factors) // 2
        u_factor_one = u_factors[mid_idx - 1]
        u_factor_two = u_factors[mid_idx]

        # 2. Process Password
        p_factors = cls.process_string(password)
        
        # Logic from original: 65th percentile element
        # math.floor(len * 0.65) - 1 is roughly index at 65%
        p_factor_final = cls.extract_indices(p_factors, 0.65)
        

        # # Use the print("".format({var})) function if you are using a version of Python less than 3.6
        # print("User Factors: {}, {}".format(u_factor_one, u_factor_two))
        # print("Pass Factor: {}".format(p_factor_final))

        # Else, use print(f"{var}") - Output results
        print(f"User Factors: {u_factor_one}, {u_factor_two}")
        print(f"Pass Factor: {p_factor_final}")
        
        return [u_factor_one, u_factor_two, p_factor_final]

# --- Usage ---
if __name__ == "__main__":
    # Example usage
    result = FactorService.get_factors("Admin", "Password123")
    print("Result:", result)
