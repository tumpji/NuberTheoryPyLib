import unittest
import test_utils

'''
This is temporary file

it creates prime numbers and store them in 
set "prmes_set" and list "primes"
'''



class PrimeModuleClass (object):
    def __init__ (self, maximum_prime=100000, maximum_factorization_lut=100000, factorization_enable=True, **kwargs):
        assert len(kwargs) == 0
        assert isinstance(maximum_prime, int) 
        assert isinstance(maximum_factorization_lut, int)

        self._maximum_prime     = maximum_prime
        self._maximum_lut       = maximum_factorization_lut
        assert self._maximum_lut <= self._maximum_prime

        self.prime_array        = self._generate_prime_list()

        if factorization_enable:
            self._factorization_lut = self._generate_factorization_lut()

    def _generate_prime_list ( self ):
        ''' 
        create list of primes to (without) maximum value
        '''
        sieve = [0] * self._maximum_prime
        for i in range(2,self._maximum_prime):
            if sieve[i] == 0: # prime
                for y in range(i+i, self._maximum_prime, i):
                    sieve[y] = 1
        return [ i for (i,d) in enumerate(sieve[2:], start=2) if d == 0 ]

    def _generate_factorization_lut ( self ):
        ''' 
        generates look up table factorizations of numbers
        '''
        result = [None]
        for act_number in range(1, self._maximum_lut):
            number = act_number     # remaining product
            fact_list = []          # current factorization

            for p in self.prime_array:   # for all prime numbers 
                while number % p == 0:  # its a divisor
                    fact_list.append(p)
                    number //= p
                if number == 1:     # done 
                    break
                elif number < act_number: # alredy computed
                    fact_list += result[number]
                    number = 1
                    break
                assert p < number
            result.append( fact_list )
        return result

    def get_max_prime_value (self):
        ''' returns maximum value generated prime numbers '''
        return self._maximum_prime

    def prime_search (self, search ):
        '''
        gets number (posibly prime number) 
        returns 
            a) None -- it is not prime
            b) Int  -- it is prime
            c) assertion error -- search for number bigger than maximum_prime const.
        '''
        mini, maxi   = 0, len(self.prime_array) - 0
        assert search < self._maximum_prime

        while True:
            pivi = (mini+maxi)//2 # pivot index
            pivv = self.prime_array[pivi] # pivot value

            if pivv == search:
                return pivi
            elif pivv > search:
                maxi = pivi - 1
            else: # pivv < search
                mini = pivi + 1

            if not (mini <= maxi) :
                return None

    def lut_factorization ( self, number ):
        '''
        factorization of number with look up table
        '''
        assert number < self._maximum_lut
        return self._factorization_lut[number]

    def addaptive_factorization ( self, number ):
        assert isinstance( number, int )

        if number < self._maximum_lut:
            return self.lut_factorization(number)
        elif self.number < 10**50:
            raise NotImplementedError





class TestPrime(unittest.TestCase):
    @classmethod
    def setUpClass (cls):
        cls.object_of_interrest = PrimeModuleClass()
        url = 'https://oeis.org/A000040/b000040.txt'
        t = test_utils.global_CacheFile.load_url(url)
        t = list( int(line.split()[1]) for line in t.split('\n') if len(line) )
        cls.loaded_primes = t
        print( t )
    
    @staticmethod
    def get_random_index ( count, f, to ):
        from random import randrange
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

    def test_from_internet (self):
        raise NotImplementedError


if __name__ == '__main__':
    unittest.main(verbosity=2)
