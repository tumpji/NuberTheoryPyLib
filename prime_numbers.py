import unittest

'''
This is temporary file

it creates prime numbers and store them in 
set "prmes_set" and list "primes"
'''


maximum_prime = 1000000
maximum_hledane = 2**500500

sieve = [0] * maximum_prime
for i in range(2,maximum_prime):
    if sieve[i] == 0: # prime
        for y in range(i+i, maximum_prime, i):
            sieve[y] = 1

primes = [ i for (i,d) in enumerate(sieve) if d == 0 ][2:] # remove 0,1 
primes_set  = set(primes)

sieve = None

class TestPrime(unittest.TestCase):
    @staticmethod
    def get_random_index ( count, f, to ):
        from random import randrange
        for i in range(count):
            yield randrange(f, to)

    def test_random (self):
        self.assertTrue( 2 in primes )
        self.assertTrue( 3 in primes )
        self.assertTrue( 17 in primes )
        self.assertTrue( 11 in primes )
        self.assertTrue( 97 in primes )
        self.assertTrue( 1 not in primes )
    def test_first_few (self):
        for i, p in enumerate([2,3,5,7,11,13,17]):
            self.assertEqual( p, primes[i] )

    def test_order (self):
        for i in self.get_random_index( 1000 ,1,len(primes)):
            self.assertTrue( primes[i-1] < primes[i] )

    def test_primes_set (self):
        self.assertEqual( len(primes), len(primes_set) )

        for i in self.get_random_index( 1000, 0, len(primes) ):
            p = primes[i]
            self.assertTrue( p in primes_set  )

if __name__ == '__main__':
    unittest.main(verbosity=2)
