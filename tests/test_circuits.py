import unittest
from itertools import product
from demos.circuits import (
    attack_examples, binding_fixed, selector_fixed, iszero_fixed,
    foreign_fixed, fake_glv_fixed
)

class ConstraintTests(unittest.TestCase):
    def test_every_vulnerable_example_is_rejected_after_repair(self):
        for name, vulnerable, repaired, _ in attack_examples():
            with self.subTest(name=name):
                self.assertTrue(vulnerable)
                self.assertFalse(repaired)

    def test_binding_public_x_7_unprovable(self):
        for w0 in range(11):
            w1 = w0**2 % 11
            w2 = w1**2 % 11
            w3 = (w2+5) % 11
            self.assertFalse(binding_fixed(7,w0,w1,w2,w3))

    def test_selector_sound_all_field_assignments(self):
        # For x,y any, if repaired constraints accept then z is one of them.
        for x,y,s in product(range(11), repeat=3):
            for z in range(11):
                if selector_fixed(x,y,z,s):
                    self.assertIn(z,(x,y))

    def test_iszero_sound(self):
        for a,out,hint in product(range(11),repeat=3):
            if iszero_fixed(a,out,hint):
                self.assertEqual(out, int(a==0))

    def test_foreign_field_sound(self):
        for x,y,z,k in product(range(3), range(3), range(3), range(2)):
            if foreign_fixed(x,y,z,k):
                self.assertEqual((x*y-z)%3,0)

    def test_fake_glv_group_cancellation(self):
        for s,u,v,P,Q in product(range(5),repeat=5):
            if fake_glv_fixed(s,u,v,P,Q):
                self.assertEqual(Q,(s*P)%5)

    def test_free_quotient_always_available(self):
        inv_ell = pow(5,-1,11)
        for u,s,v in product(range(11),repeat=3):
            k = ((u-s*v)*inv_ell) % 11
            self.assertEqual((u-s*v-5*k)%11,0)

if __name__ == '__main__':
    unittest.main()
