########################################
####### GANGA CHALLENGE PART 1-1 #######
########################################

# Imports
import ganga
import ganga.ganga
from ganga import Job, jobs, Executable, Local

# Enable monitoring in Python
ganga.enableMonitoring()

#--------------------------------------#

def main():

    # Create job
    job = createBasicGangaJob("Hello World")

    # Submit job
    job.submit()
    print(f"PYTHON OUTPUT: Job Submited with ID: {job.id}")

    # Monitor job
    monitorGangaJob(job)

    # Delete file after job is complete
    job.remove()
    print(f"PYTHON OUTPUT: Deleted Job with ID {job.id}")

    return True

#--------------------------------------#

# Create & specify basic Ganga job
def createBasicGangaJob(args="Hello World"):
    
    job = Job(name="Basic Ganga Job")
    job.application = Executable()
    job.application.exe = "/bin/echo"
    job.application.args = args
    job.backend = Local()

    return job

#--------------------------------------#

# Monitor Ganga job
def monitorGangaJob(job):

    # Ganga Job check
    if not isinstance(job, Job):
        print("ERROR: Not an instance Ganga Job")
        return False

    status = job.status

    while True:
        if job.status != status:
            status = job.status
            print(f"PYTHON OUTPUT: Job Status changed to: {status}")

        if job.status == "completed":
            status = job.status
            job.peek("stdout", "cat")
            print(f"PYTHON OUTPUT: Job with ID {job.id} Complete!")
            break
    
    return "completed"

#--------------------------------------#

# Execute main()
if __name__ == "__main__":
    main()

########################################