import unittest
import helpy.misc as misc
import helpy.functional as fnc
import helpy.curried as curried
import helpy.logging as logging
from helpy.curried import curry


class TestCurried(unittest.TestCase):

    def test_common_curries(self):
        o = object()

        self.assertTrue( curried.eq(3)(3) )
        self.assertTrue( curried.eq(o)(o) )
        self.assertFalse( curried.eq(o)( object() ) )

        self.assertTrue( curried.not_eq(4)(7) )
        self.assertTrue( curried.not_eq(o)( object() ) )
        self.assertFalse( curried.not_eq(o)(o) )

        self.assertTrue( curried.startswith('ab')('abc') )
        self.assertFalse( curried.startswith('c')('abc') )

        self.assertTrue( curried.endswith('bc')('abc') )
        self.assertFalse( curried.endswith('cab')('abc') )

    def test_map(self):
        cmap = curried.map(lambda x: x*x)
        self.assertEqual( list(cmap([1,2,3])), [1,4,9] )
        self.assertEqual( list(cmap([2,3,4])), [4,9,16] )

    def test_filter(self):
        cfilter = curried.filter(lambda x: x%2==0)
        self.assertEqual( list(cfilter([1,2,3,4])), [2,4] )
        self.assertEqual( list(cfilter(range(10))), [0,2,4,6,8] )

    def test_reduce(self):
        creduce = curried.reduce(lambda acc, y: acc+y)
        creduce123 = creduce([1,2,3])
        self.assertEqual( creduce123(), 6 )
        self.assertEqual( creduce123(0), 6 )
        self.assertEqual( creduce([1,2,3])(), 6 )
        self.assertEqual( creduce([1,2,3])(0), 6 )
        self.assertEqual( creduce123(1), 7 )

    def test_sorting(self):
        stuff = [ (5,6), (1,2), (3,4) ]
        sortfn = lambda x: x[1]
        csortby1 = curried.sort_by( sortfn )
        self.assertEqual( csortby1( stuff ), sorted(stuff, key=sortfn) )
        self.assertEqual( csortby1( stuff ), [ (1,2), (3,4), (5,6) ] )

        cargsortby1 = curried.argsort_by( sortfn )
        self.assertEqual( cargsortby1( stuff ), [ 1, 2, 0 ] )

    def test_currying(self):
        curried_max = curry(lambda x, y: max(x, y))
        max9 = curried_max(9)

        self.assertEqual( max9(8), 9 )
        self.assertEqual( max9(13), 13 )

        # try to break it
        foo = lambda x, y, z: x+y+z
        f = curry( foo )
        f(9); f(8); f(7); f(6); f(5); f(4); f(3); f(2); f(1); f(0)

        f = curry( foo )
        g = f(9)
        h = g(8)
        self.assertEqual( h(7), 9+8+7 )
        self.assertEqual( h(6), 9+8+6 )
        self.assertEqual( g(5)(2), 9+5+2 )
        self.assertEqual( f(1)(2)(3), 1+2+3 )

    def test_pipe(self):
        a = lambda x: x**13
        b = lambda x: x*7
        c = lambda x: x+23
        self.assertEqual( curried.pipe(a,b,c)(17), c(b(a(17))) )
        self.assertEqual( curried.pipe(c,a,b)(17), b(a(c(17))) )
        self.assertEqual( curried.pipe(b,c,a)(17), a(c(b(17))) )
        self.assertEqual( curried.pipe(a,c,b)(17), b(c(a(17))) )
        self.assertEqual( curried.pipe(b,a,c)(17), c(a(b(17))) )
        self.assertEqual( curried.pipe(c,b,a)(17), a(b(c(17))) )


class TestFunctional(unittest.TestCase):

    def test_flip(self):
        powflip = fnc.flip( lambda x,y: x**y )
        self.assertEqual( powflip(2,5), 25 )

    def test_foldr(self):
        fn = lambda acc,y: fnc.appended( acc, y )
        self.assertEqual( fnc.foldr(fn, [1,2,3], []), [3,2,1] )

    def test_appended(self):
        self.assertEqual( fnc.appended([1,2,3], 4), [1,2,3,4] )

    def test_argsorted(self):
        self.assertEqual( fnc.argsorted([49,52,31]), [2,0,1] )
        self.assertEqual( fnc.argsorted([49,52,31], key=lambda x: -x), [1,0,2] )


class TestMisc(unittest.TestCase):

    def test_assertion(self):
        # try to break
        misc.assertion(value_of=3, is_one_of=[1,3,5])
        misc.assertion(type_of=3, is_one_of=[int, str])
        # ensure assertion errors
        with self.assertRaises(Exception):
            misc.assertion(value_of=3, is_one_of=[1,5,9])
        with self.assertRaises(Exception):
            misc.assertion(type_of=3, is_one_of=[str])


class TestLogging(unittest.TestCase):

    def test_fmt(self):
        log = logging.Log(indent_str='#', prefix='[', suffix=']', join=' ')
        self.assertEqual( log.fmt('hi {foo}', 2, foo='bar'), "[ hi bar ]")
        log.indent()
        self.assertEqual( log.fmt('bye {foo}', foo='bar', a=3), "[ # bye bar ]")
        log.dedent()
        log.dedent()
        log.dedent()
        log.dedent()
        self.assertEqual( log.fmt('blah {1} {0}', 4, 5, a=3), "[ blah 5 4 ]")


if __name__ == '__main__':
    unittest.main()
