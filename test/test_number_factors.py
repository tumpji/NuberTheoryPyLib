#!/usr/bin/env python3
from __future__ import division
import unittest

from number_factors import *


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
        m = NumberFact( number=100 )
        self.assertEqual( m.factorization, {2:2, 5:2} )

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
