from __future__ import division

import unittest
import test_utils

from totient import *



class TestTotient(unittest.TestCase):
    def setUp (self):
        import test_utils
        cache = test_utils.global_CacheFile
        url = 'http://oeis.org/A000010/b000010.txt'
        strpair = ( line.split() for line in cache.load_url(url).split('\n') ) 
        self.data_pairs = [ int(pair[1]) for pair in strpair if len(pair) ]

    def test_prime (self):
        a = NumberTotient( prime=11 )
        self.assertEqual( a.totient, 10 )

    def test_prime_power (self):
        a = NumberTotient( prime=13 )
        b = a ** 3
        a **= 3
        self.assertEqual( b.totient, a.totient )
        self.assertEqual( 2028 , a.totient )

    def test_number_power (self):
        a = NumberTotient( prime_list=[5,3,3] )
        b = a ** 3
        a **= 3
        self.assertEqual( b.totient, a.totient )
        self.assertEqual( b.totient, 48600 )

    def test_multiply_numbertotient (self):
        a = NumberTotient( prime_list=[5,3] ) # aka 15
        b = NumberTotient( prime_list=[5,5,2] ) # aka 50
        c = a * b
        a *= b
        self.assertEqual( c.totient, a.totient )
        self.assertEqual( c.totient, 200 )

    def test_multiply_number (self):
        c = NumberTotient( prime_list=[5,5,2] ) # aka 50
        a = c * 2
        c *= 2
        self.assertEqual( c.totient, a.totient )
        self.assertEqual( c.totient, 40 )
        

    
if __name__ == '__main__':
    unittest.main()

