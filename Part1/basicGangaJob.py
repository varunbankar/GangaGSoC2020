########################################
####### GANGA CHALLENGE PART 1-1 #######
########################################

# Imports
import sys
if sys.version_info >= (3, 0):
    import ganga
else:
    import ganga.ganga
from ganga import Job, jobs, Executable, Local
from GangaCore.testlib.monitoring import run_until_completed

# Enable monitoring in Python
ganga.enableMonitoring()

#--------------------------------------#

def main():

    # Create job
    job = createBasicGangaJob("Hello World")

    job.submit()
    print(f"PYTHON OUTPUT: Job Submited with ID: {job.id}")

    run_until_completed(job)
    print(f"PYTHON OUTPUT: Job with ID: {job.id}, Completed")

    job.peek("stdout", "cat")

    # Delete job
    job.remove()
    print(f"PYTHON OUTPUT: Deleted Job with ID {job.id}")

    return True

#--------------------------------------#

# Create & specify simple Ganga job
def createBasicGangaJob(args="Hello World"):
    """ Creates a simple Ganga Job to execute /bin/echo with arguments given as parameters """
    
    job = Job(name="Basic Ganga Job")
    job.application = Executable()
    job.application.exe = "/bin/echo"
    job.application.args = args
    job.backend = Local()

    return job

#--------------------------------------#

if __name__ == "__main__":
    main()

########################################
