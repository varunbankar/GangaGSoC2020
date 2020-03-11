########################################
####### GANGA CHALLENGE PART 2-2 #######
########################################

# Imports
import timeit 
from createDatabase import readFromDatabase

#--------------------------------------#

# jobinfo so that createDatabase_time() doesn't need to recreate it.
jobinfo = readFromDatabase()

#--------------------------------------#

# Return time taken to execute readFromDatabase() 1000 times
def readFromDatabase_time():

    setup = """
from createDatabase import readFromDatabase"""

    testCode = """
readFromDatabase()"""

    print(timeit.timeit(setup = setup, stmt = testCode, number = 1000))

#--------------------------------------#

# Return time taken to execute reCreateJob() 100 times
def reCreateJob_time():

    setup = """
from createDatabase import reCreateJob
from __main__ import jobinfo"""

    testCode = """
reCreateJob(jobinfo)"""

    print(timeit.timeit(setup = setup, stmt = testCode, number = 100))

#--------------------------------------#

if __name__ == "__main__":
    readFromDatabase_time() 
    reCreateJob_time()

########################################