import unittest
import os
import Part1.wordCounter as wordCounter

gangasoc = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

class TestWordCounter(unittest.TestCase):

    def test_count(self):
        
        wordCounter.main()

        f = open(os.path.join(gangasoc, "Part1", "wordCounterOutput", "count.txt"), "r")

        count = f.read()

        self.assertEqual(int(count), 399)