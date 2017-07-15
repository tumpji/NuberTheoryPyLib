from __future__ import division
import copy

import number_factors

import unittest
import test_utils



class NumberTotient (object):
    def __init__ (self, copye=None, **kwargs):
        if copy is not None:
            if type(copye) is NumberTotient:
                self.__dict__ = copy.deepcopy( copye.__dict__ )
                assert 'factorization' in self.__dict__
            elif type(copye) is number_factors.NumberFact:
                self.factorization =  copye
                self.calculate_from_scratch()
            else:
                self.factorization = number_factors.NumberFact(**kwargs)
                self.calculate_from_scratch()

    def calculate_from_scratch ( self ):
        self.totient = 1
        for p,v in self.factorization.factorization.items():
            t = self.get_totient_form_prime_power(p, v)
            # t(a * b) =  t(a) * t(b) * gcd(a,b) / t(gcd(a,b))
            # 'a' and 'b' is relative prime => gcd=1 & t(gcd) = 1
            # => t(a*b) = t(a) * t(b)
            self.totient *= t

    def __mul__ (self, number):
        co = NumberTotient( self )
        co *= number
        return co
    def __imul__ (self, number):
        if isinstance(number, number_factors.NumberFact):
            self.factorization *= number
        elif isinstance(number, NumberTotient):
            self.factorization *= number.factorization
        elif isinstance(number, int):
            self.factorization *= number_factors.NumberFact( number=number )
        else :
            raise TypeError('Not compatible type')
        self.calculate_from_scratch()
        return self

    def __pow__ (self, number):
        assert isinstance(number, int)
        return NumberTotient( self.factorization ** number )
    def __ipow__ (self, number):
        assert isinstance(number, int)
        self.factorization **= number
        self.calculate_from_scratch()
        return self
        
    @staticmethod
    def get_totient_from_prime ( prime ):
        # t(p) = p - 1  if p is prime
        return prime - 1
    @staticmethod
    def get_totient_form_prime_power ( prime, power ):
        # t(n^m) = n ^ (m-1) * t(n)
        return (prime**(power - 1)) * NumberTotient.get_totient_from_prime( prime )




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
        self.assertEqual( c.totient, 200 )
        

    
if __name__ == '__main__':
    unittest.main(verbosity=2)
