from Prime_Generator import gen_primes
from random import randint

def dh_exchange():
    """

    :return: alice_key
    """
    primes = gen_primes()
    rand1 = randint(1000, 100000)
    rand2 = randint(1000, 10000)
    p = [next(primes) for i in range(rand1)][rand1-1]
    g = [next(primes) for i in range(rand1)][rand1-1]
    a = randint(1000, 100000)
    b = randint(1000, 100000)

    alice_to_bob = pow(g, a) % p
    bob_to_alice = pow(g, b) % p

    alice_key = pow(bob_to_alice, a) % p
    bob_key = pow(alice_to_bob, b) % p

    return alice_key, bob_key


key = dh_exchange()