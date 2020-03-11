import unittest
from Part1.basicGangaJob import createBasicGangaJob
from GangaCore.testlib.monitoring import run_until_completed

class TestSimpleGangaJob(unittest.TestCase):

    def test_create(self):
        j = createBasicGangaJob()
        self.assertEqual(j.name, "Basic Ganga Job")
        self.assertEqual(j.application.exe, "/bin/echo")
        self.assertEqual(j.application.args[0], "Hello World")

        j.submit()

        self.assertIn(j.status, ["submitted", "running", "completed"])

        run_until_completed(j)

        self.assertEqual(j.status, "completed")