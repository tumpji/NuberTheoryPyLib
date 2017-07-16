from __future__ import division
import collections
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
            if number == 0:
                raise ValueError('Result is zero')
            if number == 1:
                pass
            else:
                for p in prime_numbers.prime_set.addaptive_factorization(number):
                    self.factorization[p] += 1

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


