#!/usr/bin/env python3
import unittest
import operator
from random import randrange
import bisect

from prime_numbers import *

class TestPrime(unittest.TestCase):
    @classmethod
    def setUpClass (cls):
        cls.object_of_interrest = PrimeModuleClass()
        url = 'https://oeis.org/A000040/b000040.txt'
        t = test_utils.global_CacheFile.load_url(url)
        t = list( int(line.split()[1]) for line in t.split('\n') if len(line) )
        cls.loaded_primes = t
    
    @staticmethod
    def get_random_index ( count, f, to ):
        for i in range(count):
            yield randrange(f, to)

    def test_first_few (self):
        for i, p in enumerate([2,3,5,7,11,13,17]):
            self.assertEqual( p, self.object_of_interrest.prime_array[i] )

    def test_order (self):
        pa = self.object_of_interrest.prime_array
        for i in self.get_random_index( 1000 ,1,len(pa)):
            self.assertTrue( pa[i-1] < pa[i] )

    def test_prime_search(self):
        pa = self.object_of_interrest.prime_array

        for i in self.get_random_index( 1000, 0, len(pa) ):
            p = pa[i]
            t = self.object_of_interrest.prime_search(p)
            self.assertTrue( t == i  )
            # not prime 
            if p != 2:
                p += 1 
                t = self.object_of_interrest.prime_search(p)
                self.assertIsNone(t)

    def generator_random_primes (self, maximum=None):
        pa = self.object_of_interrest.prime_array
        if maximum is None:
            maximum = len(pa)
        assert maximum <= len(pa)
        for i in self.get_random_index( 1000, 0, maximum ):
            yield pa[i]

    def test_factorization_prime_lut ( self ):
        # find smallest posible 
        maxi = bisect.bisect_left( 
                self.object_of_interrest.prime_array, 
                self.object_of_interrest._maximum_lut )
        
        for p in self.generator_random_primes( maximum=maxi ):
            f = self.object_of_interrest.lut_factorization(p)
            mp = reduce( operator.mul, f )
            self.assertEqual(p, mp)
    def test_factorization_lut ( self ):
        i = 0
        while i < 1000:
            number = randrange(4, self.object_of_interrest._maximum_prime)
            if number in self.object_of_interrest.prime_array: 
                continue
            fakt = self.object_of_interrest.lut_factorization(number)
            n = reduce( operator.mul, fakt )
            self.assertEquals( number, n )
            i += 1


    def test_from_internet (self):
        maximum_prime_index = min( \
                len(self.loaded_primes), \
                len(self.object_of_interrest.prime_array) \
                ) 
        for i in self.get_random_index( 1000, 0, maximum_prime_index ):
            p1 = self.loaded_primes[i]
            p2 = self.object_of_interrest.prime_array[i]
            self.assertEqual( p1, p2 )


if __name__ == '__main__':
    unittest.main()
