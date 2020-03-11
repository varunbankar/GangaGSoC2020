########################################
####### GANGA CHALLENGE PART 2-1 #######
########################################

# Imports
import os
import sys
import time
from io import StringIO 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import ganga
from ganga import Job
from GangaCore.GPIDev.Persistency import stripProxy
from GangaCore.testlib.monitoring import run_until_completed
from Part1.basicGangaJob import createBasicGangaJob

#--------------------------------------#

# Database configurations
# SQLite database used here for prototyping purpose
# With simple change in URI it can be connected to production grade database like PostreSQL
# DATABASE_URI = "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
DATABASE_URI = "sqlite:///database.db"
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

#--------------------------------------#

# Base for Database Model
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

def recreateDatabase():
    """ Recreate Database by deleting and rebuilding it """

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

#--------------------------------------#

def main():

    # Recreating database for fresh benchmarks
    recreateDatabase()

    # Simple "Hello World" job - created in first exercise
    job = createBasicGangaJob("Hello World")

    # Add the job to database
    addToDatabase(job)

    # Retrieve job info from database
    jobinfo = readFromDatabase()

    # Recreate job from the retrieved information
    recreatedJob = reCreateJob(jobinfo)

    # Submit job to test if it works
    recreatedJob.submit()

    # Run until job is complete
    run_until_completed(recreatedJob)

    # Print stdout of the job
    recreatedJob.peek("stdout", "cat")

    # Removing jobs
    print("PYTHON OUTPUT: Removing jobs...")
    job.remove()
    recreatedJob.remove()

#--------------------------------------#

def addToDatabase(job):
    """ Add Ganga job to database """

    # Ganga Job check
    if not isinstance(job, Job):
        print("ERROR: Not an instance Ganga Job")
        return False

    # session to interact with database
    session = Session()

    # Extracting job information to a variable: Export() Function inner working
    strippedProxyJob = stripProxy(job)

    with Capturing() as output:
        strippedProxyJob.printTree(sys.stdout, "copyable")

    lineList = [
            "#Ganga# File created by Ganga - %s\n" % (time.strftime("%c")),
            "#Ganga#\n",
            "#Ganga# Object properties may be freely edited before reloading into Ganga\n",
            "#Ganga#\n",
            "#Ganga# Lines beginning #Ganga# are used to divide object definitions,\n",
            "#Ganga# and must not be deleted\n",
            "\n"]


    l1 = ''.join(lineList)
    name = strippedProxyJob._name
    category = strippedProxyJob._category
    l2 = "#Ganga# %s object (category: %s)\n" % (name, category)
    l3 = '\n'.join(output)
    
    # Storing the Export() function like output to a variable
    jobinfo = l1 + l2 + l3

    # Database row to add
    addJob = gangaJob(jobinfo=jobinfo)

    # Adding & commiting changes to databse
    session.add(addJob)
    session.commit()
    print(f"PYTHON OUTPUT: Stored Ganga Job to Database")

    # Closing database session
    session.close()

    return True

#--------------------------------------#

def readFromDatabase(jobID=1):
    """ Retrieve job info based on database ID (Default ID = 1) """

    # session to interact with database
    session = Session()

    # Get job information for database using ID (Database ID)
    jobinfo = session.query(gangaJob).get(jobID)
   
    # Closing database session
    session.close()

    return jobinfo

#--------------------------------------#

def reCreateJob(jobinfo):
    """  Create job from the information retrieved from the database """

    # Recreate job using stored job info. Load() fuction inner functionality
    lineList = []
    for line in jobinfo.jobinfo.splitlines():
        if (line.strip().startswith("#Ganga#")):
            lineList.append("#Ganga#")
        else:
            lineList.append(line)
    itemList = ("".join(lineList)).split("#Ganga#")

    jobList = []
    for item in itemList:
        item = item.strip()
        if item:
            try:
                from GangaCore.GPIDev.Base.Proxy import getProxyInterface
                this_object = eval(str(item), getProxyInterface().__dict__)
                jobList.append(this_object)
            except:
                print("Unable to Recreate Ganga Job from given Job Info")

    return jobList[0]

#--------------------------------------#

# Capture stdout for specific function
class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout
    
#--------------------------------------#

if __name__ == "__main__":
    main()

########################################