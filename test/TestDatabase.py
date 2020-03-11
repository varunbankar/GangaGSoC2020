########################################
###### GANGA CHALLENGE UNIT TESTS ######
############ TEST DATABASE #############
########################################

# Imports
import unittest
from Part1.basicGangaJob import createBasicGangaJob
from Part2.createDatabase import recreateDatabase, addToDatabase, readFromDatabase, reCreateJob
from GangaCore.testlib.monitoring import run_until_completed

#--------------------------------------#

class TestDatabase(unittest.TestCase):

    def test_database(self):
        
        # Recreate Database for the test
        recreateDatabase()

        # "Hello World" Ganga job
        j = createBasicGangaJob()

        # Add job to database
        addToDatabase(j)

        # Recreate Job from database
        j_info = readFromDatabase()
        j2 = reCreateJob(j_info)

        # Compare Original & Recreated job
        self.assertEqual(j.name, j2.name)
        self.assertEqual(j.application, j2.application)
        self.assertEqual(j.application.exe, j2.application.exe)
        self.assertEqual(j.application.args, j2.application.args)
        self.assertEqual(j.backend, j2.backend)

        # Submit recreated job
        j2.submit()
        self.assertIn(j2.status, ["submitted", "running", "completed"])

        # Run Recreated job until completed
        run_until_completed(j2)
        self.assertEqual(j2.status, "completed")

#--------------------------------------#