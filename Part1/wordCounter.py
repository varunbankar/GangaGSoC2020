########################################
####### GANGA CHALLENGE PART 1-2 #######
########################################

# Imports
import os
import ganga
import ganga.ganga
from ganga import Job, jobs, Executable, File, LocalFile, ArgSplitter, CustomMerger, Local
from GangaCore.testlib.monitoring import run_until_completed

# Enable monitoring in Python
ganga.enableMonitoring()

#--------------------------------------#

# Path to current working directory
currentDir = os.path.dirname(os.path.realpath(__file__))

def main():

    # Ganga job to split PDFs
    job = Job(name="Split PDF File")
    job.application.exe = File(os.path.join(currentDir, "pdfSplitter.sh"))
    job.inputfiles = [ LocalFile(os.path.join(currentDir, "pdfSplitter.py")), LocalFile(os.path.join(currentDir, "CERN.pdf")) ]
    job.outputfiles = [ LocalFile("CERN_*.pdf") ]
    job.backend = Local()

    # Submiting the job
    job.submit()

    # Run until the job status is completed
    run_until_completed(job)

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
    job2.application.exe = File(os.path.join(currentDir, "count.sh"))
    job2.inputfiles = job.outputfiles
    job2.outputfiles = [ LocalFile("count.txt") ]
    
    # Submiting the job2
    job2.submit()

    # Run until the job2 status is completed
    run_until_completed(job2)

    # Custom Merger to merger the output of the subjobs
    merger = CustomMerger()
    merger.files = ["count.txt"]
    merger.module = File(os.path.join(currentDir, "merger.py"))
    merger.ignorefailed = True
    merger.overwrite = True
    merger.merge(job2.subjobs, os.path.join(currentDir, "wordCounterOutput"))

    # Removing jobs
    print("PYTHON OUTPUT: Removing jobs...")
    job.remove()
    job2.remove()

    return True

#--------------------------------------#

if __name__ == "__main__":
    main()

########################################




