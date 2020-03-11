########################################
###### GANGA CHALLENGE UNIT TESTS ######
########### TEST WORD COUNT ############
########################################

# Imports
import unittest
import os
import Part1.wordCounter as wordCounter

#--------------------------------------#

# Path to "gangasoc" directory
gangasoc = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

#--------------------------------------#

class TestWordCounter(unittest.TestCase):

    def test_count(self):
        
        # Execute the count jobs
        wordCounter.main()

        # Open the output file and assert the count with correct value
        f = open(os.path.join(gangasoc, "Part1", "wordCounterOutput", "count.txt"), "r")
        count = f.read()
        self.assertEqual(int(count), 399)

#--------------------------------------#