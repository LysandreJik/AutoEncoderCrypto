# This function yields a generator to get prime numbers
def gen_primes():

    # D is the list of previous prime numbers
    D = {}

    # q is the number we test currently
    q = 2

    while True:
        if q not in D:

            yield q
            D[q * q] = [q]
        else:
            for p in D[q]:
                D.setdefault(p + q, []).append(p)
            del D[q]

        q += 1

