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

primes = map( lambda (i,d): i, filter(lambda (i,d) : d == 0, enumerate(sieve)))



primes      = primes[2:]
primes_set  = set(primes)



class TestPrime(unittest.TestCase):
    def test_obsahuje (self):
        self.assertTrue( 2 in primes )
        self.assertTrue( 3 in primes )
        self.assertTrue( 17 in primes )
        self.assertTrue( 11 in primes )
        self.assertTrue( 97 in primes )
        self.assertTrue( 1 not in primes )
    def test_poradi (self):
        for i in range(1,len(primes)):
            self.assertTrue( primes[i-1] < primes[i] )
    def test_primes_set (self):
        for p in primes:
            self.assertTrue( p in primes_set  )
    def test_primes (self):
        for p in primes_set:
            self.assertTrue( p in primes )

if __name__ == '__main__':
    unittest.main()
