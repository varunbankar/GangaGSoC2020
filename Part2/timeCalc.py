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

# Return time taken to execute readFromDatabase 1000 times
def readFromDatabase_time():

    setup = """
from createDatabase import readFromDatabase"""

    testCode = """
readFromDatabase()"""

    print(timeit.timeit(setup = setup, stmt = testCode, number = 1000))

#--------------------------------------#

# Return time taken to execute createJob 100 times
def createJob_time():

    setup = """
from createDatabase import createJob
from __main__ import jobinfo"""

    testCode = """
createJob(jobinfo)"""

    print(timeit.timeit(setup = setup, stmt = testCode, number = 100))

#--------------------------------------#

if __name__ == "__main__":
    readFromDatabase_time() 
    createJob_time()

########################################