def gen_primes():
    """
    ;return: This function yields a generator containing prime numbers
    """
    D = {}
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

