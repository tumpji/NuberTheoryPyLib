from __future__ import division
import collections
import unittest
import copy

import prime_numbers



class NumberFact (object):
    '''
    this class transforms every number to pair its prime factorization
    with this representation is posible to acomplish more optimal algorithms
    '''
    #def __init__ (self, copya=None, *, prime=None, prime_list=None, prime_dict=None, number=None):
    def __init__ (self, copya=None, prime=None, prime_list=None, prime_dict=None, number=None, **kwargs):
        ''' 
        NumberFact(prime=11, prime_list=[2,3], prime_dict={5:4, 2:6}, number=120)
        creates number 11 * 2*3 * 5^4 * 2^6 * [ 120 ]
        '''
        self.factorization = collections.defaultdict(int)

        assert any(map(lambda x: x != None, 
            [copya, prime, prime_list, prime_dict, number] ))
        assert len(kwargs) == 0

        if copya is not None:
            assert isinstance(copya, NumberFact)
            self.factorization = copy.deepcopy(copya.factorization)

        if prime is not None:
            assert isinstance(prime, int)
            self.factorization[prime] += 1
        if prime_list is not None:
            assert isinstance(prime_list, list)
            for p in prime_list:
                assert isinstance(p, int)
                self.factorization[p] += 1
        if prime_dict is not None:
            assert isinstance(prime_dict, dict)
            for p,n in prime_dict.items():
                assert isinstance(p, int)
                assert isinstance(n, int)
                self.factorization[p] += n

        if number is not None:
            if number == 1:
                pass
            else:
                raise NotImplementedError

        for p in self.factorization:
            self.check_prime(p)

        self.factorization = self._clear_dict(self.factorization)

    @staticmethod
    def check_prime ( prime ):
        if prime not in prime_numbers.prime_set.prime_array:
            raise ValueError( "'{}' is not prime".format(prime) )
        # or
        #assert k in prime_set
    @staticmethod
    def _clear_dict ( dictionary ):
        a = collections.defaultdict(int)
        a.update( {k : v for k, v in dictionary.items() if v > 0 } )
        return a

    def __eq__ (self, other):
        assert isinstance(other, NumberFact)
        return self.factorization == other.factorization

    def to_int (self):
        n = 1
        for k,v in self.factorization.items():
            n *= k ** v
        return n
    
    def __pow__ ( self, number ):
        '''
        basic power, argument can be only non negative integer
        '''
        result = NumberFact( self )
        result **= number
        return result 
    def __ipow__ ( self, number ):
        assert isinstance(number, int)
        if   number == 0: self.factorization = collections.defaultdict(int)
        elif number == 1: pass
        elif number <  0: raise ValueError
        else:
            for i in self.factorization:
                self.factorization[i] *= number
        return self 


    def __mul__ ( self, number ):
        '''
        multiplication, argument can be integer or this class instance 
        '''
        result = NumberFact( self )
        result *= number
        return result 
    def __imul__ ( self, number ):
        if isinstance(number, int):
            self.check_prime( number )
            self.factorization[number] += 1
        elif isinstance(number, NumberFact):
            for p,v in number.factorization.items():
                if v != 0:
                    self.factorization[p] += v
        else: 
            raise TypeError
        return self

    def __truediv__ ( self, number ):
        '''
        division, argument can be integer or this class instance 
        '''
        return self.__floordiv__( number )
    def __itruediv__ (self, number):
        return self.__iregulardiv__( number )

    def __floordiv__ ( self, number ):
        '''
        division, argument can be integer or this class instance 
        '''
        result = NumberFact( self )
        result //= number
        return result 

    def __ifloordiv__ ( self, number ):
        if isinstance(number, int):
            check_prime( number )
            if self.factorization[number] == 0:
                raise ValueError('division cannot be reduced')
            self.factorization[number] -= 1
        elif isinstance(number, NumberFact):
            for p,v in number.factorization.items():
                if v == 0: continue
                if self.factorization[p] < v:
                    raise ValueError('division cannot be reduced')
                self.factorization[p] -= v
        else: 
            raise TypeError('division cannot handle type \'' + number.__name__ + '\'')
        self.factorization = self._clear_dict( self.factorization )
        return self


# ++++++++++++++++++++++++++++++++++++++++++++++++++
#                   tests
# ++++++++++++++++++++++++++++++++++++++++++++++++++


class TestNumber(unittest.TestCase):
    def setUp (self):
        #self.numbers = [ ({13:2, 3:1}, 312), (, 7320) ]
        self.number1 = NumberFact( prime_dict={13:2, 3:1} ) # totient 312
        self.number2 = NumberFact( prime_dict={5:1, 3:3, 11:2} ) # totient 7320
        self.number1_value = 312
        self.number2_value = 7320

    def test_init_prime (self):
        a = NumberFact( prime=11 )
        #self.assertEqual( a.totient, 11 - 1 )
        self.assertEqual( a.factorization , {11:1} )
    def test_init_prime_list (self):
        a = NumberFact( prime_list=[5,2,3,2] )
        #self.assertEqual( a.totient, 16 )
        self.assertEqual( a.factorization , {2:2, 3:1, 5:1} )
    def test_init_prime_dict (self):
        a = NumberFact( prime_dict=dict(self.number1.factorization) )
        m =self.number1.factorization 
        self.assertEqual( a.factorization, m )

    def test_init_error_kwargs (self):
        with self.assertRaises( AssertionError ):
            NumberFact( somethingbad=12 )
    def test_init_error_no_args (self):
        with self.assertRaises( AssertionError ):
            NumberFact()
    def test_init_number_1 (self):
        m = NumberFact( number=1 )
        self.assertTrue( len(m.factorization) == 0 )
    def test_init_number_10 (self):
        # this test is temporary
        with self.assertRaises( NotImplementedError ):
            m = NumberFact( number=2 )

    def test_copy (self):
        a = NumberFact( self.number2 )
        self.assertEqual( a.factorization, self.number2.factorization )
    
    def test_equal (self):
        a = NumberFact( self.number1 )
        self.assertEqual( a , self.number1 )
        self.assertNotEqual( a , self.number2 )
        a *= 3
        self.assertNotEqual( a , self.number1 )
        

    def test_exponentiation (self):
        a = NumberFact( prime_dict={2:2, 11:1} )
        a = a ** 2
        #self.assertEqual( a.totient, 880 )
        self.assertEqual( a.factorization , {2:4, 11:2} )

    def test_multiplication_class (self):
        a = NumberFact( prime_dict={2:2, 5:1} ) # 20
        b = NumberFact( prime_dict={2:1, 11:2} ) # 242
        c = a * b
        #self.assertEqual( c.totient, 1760 )
        self.assertEqual( c.factorization , {2:3, 5:1, 11:2} )
    def test_multiplication_int (self):
        a = NumberFact( prime_dict={2:2, 5:1} ) # 20
        c = a * 11
        c = c * 2
        c = c * 11
        #self.assertEqual( c.totient, 1760 )
        self.assertEqual( c.factorization , {2:3, 5:1, 11:2} )

    def test_division_ok (self):
        a = NumberFact( prime_dict={2:3, 5:1, 11:1, 13:1} )
        b = NumberFact( prime_dict={2:1, 5:1} )
        c = a / b
        #self.assertEqual( c.totient, 240 )
        self.assertEqual( c.factorization , {2:2, 11:1, 13:1} )

    def test_division_error (self):
        a = NumberFact( prime_dict={2:3, 5:1, 11:1, 13:1} )
        b = NumberFact( prime_dict={2:1, 5:2 } )
        self.assertRaises( ValueError, lambda : a / b ) 

    def test_to_int (self):
        self.assertEqual( self.number1.to_int(), 13*13*3 )
        self.assertEqual( self.number2.to_int(), 11**2 * 3**3 * 5 )

if __name__ == '__main__':
    unittest.main(verbosity=2)
