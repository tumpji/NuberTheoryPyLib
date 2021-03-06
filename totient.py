from __future__ import division
import copy

import number_factors
import utils




class NumberTotient (object):
    def __init__ (self, copye=None, **kwargs):
        if copye is not None:
            if type(copye) is NumberTotient:
                self.factorization = copy.deepcopy(copye.factorization)
                self.totient = copye.totient
                return
            elif type(copye) is number_factors.NumberFact:
                assert len(kwargs) == 0 
                self.factorization = copy.deepcopy(copye)
        else:
            self.factorization = number_factors.NumberFact(**kwargs)

        self.calculate_from_scratch()
        assert 'factorization' in self.__dict__
        assert 'totient' in self.__dict__

    def calculate_from_scratch ( self ):
        self.totient = 1
        print(self)
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
        a = self.factorization ** number
        return NumberTotient( a )
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

