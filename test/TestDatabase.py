import unittest
from Part1.basicGangaJob import createBasicGangaJob
from Part2.createDatabase import recreateDatabase, addToDatabase, readFromDatabase, reCreateJob
from GangaCore.testlib.monitoring import run_until_completed

class TestDatabase(unittest.TestCase):

    def test_database(self):
        
        recreateDatabase()

        j = createBasicGangaJob()

        addToDatabase(j)

        j_info = readFromDatabase()

        j2 = reCreateJob(j_info)

        self.assertEqual(j.name, j2.name)
        self.assertEqual(j.application, j2.application)
        self.assertEqual(j.application.exe, j2.application.exe)
        self.assertEqual(j.application.args, j2.application.args)
        self.assertEqual(j.backend, j2.backend)

        j2.submit()

        self.assertIn(j2.status, ["submitted", "running", "completed"])

        run_until_completed(j2)

        self.assertEqual(j2.status, "completed")