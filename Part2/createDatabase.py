########################################
####### GANGA CHALLENGE PART 2-1 #######
########################################

# Imports
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import ganga
import ganga.ganga
from ganga import Job, load, export
from Part1.basicGangaJob import createBasicGangaJob, monitorGangaJob

#--------------------------------------#

# Database configurations
# SQLite data for prototyping purpose
# With simple change in URI it can be connected to production level database like PostreSQL
# DATABASE_URI = "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
DATABASE_URI = "sqlite:///database.db"
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

#--------------------------------------#

# Database Model
Base = declarative_base()
Base.metadata.create_all(engine)

# Class for ORM
class gangaJob(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    name = Column(String, default="Ganga Job")
    jobinfo = Column(String)

    def __repr__(self):
        return "<Job (id='{}', name='{}')>".format(self.id, self.name)

#--------------------------------------#

# Functionn to recreate database
def recreateDatabase():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

#--------------------------------------#

def main():

    # Recreating database for fresh benchmarks
    recreateDatabase()

    # Simple "Hello World" job created in first exercise
    job = createBasicGangaJob("Hello World")

    # Add the job to database
    addToDatabase(job)

    # Retrieve job info from database
    jobinfo = readFromDatabase()

    # Create job from the retrieved information
    recreatedJob = createJob(jobinfo)

    # Submit job to test if it works
    recreatedJob.submit()

    # Monitor ganga job status
    monitorGangaJob(recreatedJob)

    # Removing jobs
    print("PYTHON OUTPUT: Removing jobs...")
    job.remove()
    recreatedJob.remove()

#--------------------------------------#

# Function to add Ganga job to database
def addToDatabase(job):

    # Ganga Job check
    if not isinstance(job, Job):
        print("ERROR: Not an instance Ganga Job")
        return False

    # session to interact with database
    session = Session()

    # Exporting job to a text file
    export(job, "job.txt")

    # Reading exported file and storing content in a variable
    jobfile = open("job.txt", "r") 
    jobinfo = jobfile.read()
    os.remove("job.txt")

    # Database row to add
    addJob = gangaJob(jobinfo=jobinfo)

    # Adding & commiting changes to databse
    session.add(addJob)
    session.commit()

    # Closing database session
    session.close()

    return True

#--------------------------------------#

# Function to retrieve job info based on database ID (Default ID = 1)
def readFromDatabase(jobID=1):

    # session to interact with database
    session = Session()

    # Get job information for database using ID (Database ID)
    jobinfo = session.query(gangaJob).get(jobID)
   
    # Closing database session
    session.close()

    return jobinfo

#--------------------------------------#

# Function to create job from the information retrieved from the database
def createJob(jobinfo):

    # Creating job file for load function to read from
    jobfile = open("job.txt", "w")
    jobfile.write(jobinfo.jobinfo)
    jobfile.close()

    # Create Ganga job from job.txt
    job = load("job.txt")
    os.remove("job.txt")

    return job[0]

#--------------------------------------#

if __name__ == "__main__":
    main()

########################################