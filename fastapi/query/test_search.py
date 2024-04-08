import unittest
import search

class MyTestCase(unittest.TestCase):
    def test_something(self):
        q = "The quick brown fox jumps over the lazy dog."
        expected = ["quick", "brown", "fox", "jumps", "over", "lazy", "dog"]
        actual = search.parse_query(q)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
