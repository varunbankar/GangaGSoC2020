########################################
####### GANGA CHALLENGE PART 1-2 #######
########################################

# Imports
import os
from os import walk
import ganga
import ganga.ganga
from ganga import Job, jobs, Executable, File, LocalFile, ArgSplitter, CustomMerger, Local
from basicGangaJob import monitorGangaJob

# Enable monitoring in Python
ganga.enableMonitoring()

#--------------------------------------#

# Path to current working directory
currentDir = os.path.dirname(os.path.realpath(__file__))

def main():

    # Ganga job to split PDFs
    job = Job(name="Split PDF File")
    job.application.exe = File("pdfSplitter.sh")
    job.inputfiles = [ LocalFile("pdfSplitter.py"), LocalFile("CERN.pdf") ]
    job.outputfiles = [ LocalFile("CERN_*.pdf") ]
    job.backend = Local()

    # Submiting the job
    job.submit()

    # Monitoring the job status
    monitorGangaJob(job)

    # Arguments to be used in ArgSplitter
    args = []
    for outputfile in job.outputfiles:
        arg = []
        arg.append(str(outputfile.namePattern))
        args.append(arg)

    # Creating ArgSplitter    
    splitter = ArgSplitter(args=args)

    # Ganga Job to count the word file by file using subjobs
    job2 = Job(splitter=splitter, name="Count Word 'the'")
    job2.application.exe = File("count.sh")
    job2.inputfiles = job.outputfiles
    job2.outputfiles = [ LocalFile("count.txt") ]
    
    # Submiting the job2
    job2.submit()

    # Monitoring job2 status
    monitorGangaJob(job2)

    # Custom Merger to merger the output of the subjobs
    merger = CustomMerger()
    merger.files = ["count.txt"]
    merger.module = File("merger.py")
    merger.ignorefailed = True
    merger.overwrite = False
    merger.merge(job2.subjobs, os.path.join(currentDir, "wordCounterOutput"))

    # Removing jobs
    job.remove()
    job2.remove()

    return True


#--------------------------------------#

if __name__ == "__main__":
    main()

########################################




