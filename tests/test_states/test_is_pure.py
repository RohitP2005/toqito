"""Tests for is_pure function."""
import unittest
import numpy as np

from toqito.states import basis, bell
from toqito.state_props import is_pure


class TestIsPure(unittest.TestCase):
    """Unit test for is_pure."""

    def test_is_pure_state(self):
        """Ensure that pure Bell state returns True."""
        rho = bell(0) * bell(0).conj().T
        self.assertEqual(is_pure(rho), True)

    def test_is_pure_list(self):
        """Check that list of pure states returns True."""
        e_0, e_1, e_2 = basis(3, 0), basis(3, 1), basis(3, 2)

        e0_dm = e_0 * e_0.conj().T
        e1_dm = e_1 * e_1.conj().T
        e2_dm = e_2 * e_2.conj().T

        self.assertEqual(is_pure([e0_dm, e1_dm, e2_dm]), True)

    def test_is_not_pure_state(self):
        """Check that non-pure state returns False."""
        rho = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        self.assertEqual(is_pure(rho), False)

    def test_is_not_pure_list(self):
        """Check that list of non-pure states return False."""
        rho = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        sigma = np.array([[1, 2, 3], [10, 11, 12], [7, 8, 9]])
        self.assertEqual(is_pure([rho, sigma]), False)


if __name__ == "__main__":
    unittest.main()
