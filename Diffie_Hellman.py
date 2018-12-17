from Prime_Generator import gen_primes
from random import randint


# This function processes the DIffie-Hellman key exchange
# Return: alice_key and bob_key (should be the same)
def dh_exchange():
    
	# Prime number generator declaration
    primes = gen_primes()
	
	# Using random numbers to chose a random prime number with the generator
    rand1 = randint(1000, 100000)
    rand2 = randint(1000, 10000)
	
	# p and g are created using generated prime numbers
    p = [next(primes) for i in range(rand1)][rand1-1]
    g = [next(primes) for i in range(rand1)][rand1-1]
	
	# Bob and Alice chose random numbers
    a = randint(1000, 100000)
    b = randint(1000, 100000)

	# Calculates the information to exchange
    alice_to_bob = pow(g, a) % p
    bob_to_alice = pow(g, b) % p

	# Calculates the key from previous exchange
    alice_key = pow(bob_to_alice, a) % p
    bob_key = pow(alice_to_bob, b) % p
	
	# Returns the keys, that are supposed to be equal
    return alice_key, bob_key


key = dh_exchange()
