# Ganga Project GSoC 2020 Challenge

# Introduction

Challenge for Google Summer of Code 2020 by Ganga Project. 

---

# How to Set Up

#TODO

---

# Challenge

## Part 1

### Task 1 - Creating Simple Ganga Job

For this task, basic Ganga Job was supposed to be created which would run `Hello Run` after submitting. The file associated with this task is `./Part1/basicGangaJob.py` . I will briefly walk through the code.

- First few lines are the imports and I noticed that we need to manually enable monitoring of Ganga job else after running the script it would not update the status of the job, hence `ganga.enableMonitoring()` enables monitoring of Ganga jobs to monitor the status of the job after executing the script.
- Function `createBasicGangaJob(args="Hello World")` - function which creates a Ganga Job Object with specific attributes and returns it. Parameter of the function accepts the arguments to `echo` whose default value is `Hello World`
    - This function will then be further used in Part 2 of the challenge.
- Function `monitorGangaJob(job)` - function accepts only an instance of Ganga Job and monitors it's status. Print anytime the status of the jobs changes and returns `completed` after successful completion of the job.
    - This function will be used in all further tasks.
- Function `Main()` - created a basic Ganga Job using `createBasicGangaJob(args)` function and the submits it. `monitorGangaJob(job)` monitors the job status and when the job is completed, `job.peek()` prints the `stdout` of the job in the terminal. After the task is finished, the job is then removed.

**DEMO:** [https://youtu.be/8y0_s4Vr4VE](https://youtu.be/8y0_s4Vr4VE)

### Task 2 - Splitting PDF, Using Subjobs to Count Words, Merging the Output

For this task, the given file `CERN.pdf` was supposed to be split into individual pages and the using `ArgSpliiter` count the occurrence of the word `the` in every individual file and save it in the output. After the output of the all subjobs was to be added and stored in a file. The main file associated with this task is `./Part1/wordCounter.py` with the helper modules `./Part1/pdfSplitter.py`, `./Part1/pdfSplitter.sh`, `./Part1/count.sh`, `./Part1/merger.py` . With all these files in place, I will briefly walk through the code.

- First few lines are the imports and `ganga.enableMonitoring()` enables monitoring of Ganga jobs in the python script.
- In the `main()` function can be divided into 3 parts:
    - First, A Ganga Job is created to split `CERN.pdf` into individual pages. To the Ganga job, `[pdfSplitter.py](http://pdfsplitter.py)` & `[pdfSplitter.sh](http://pdfsplitter.sh)` are given as input files.
        - `[pdfSplitter.py](http://pdfsplitter.py)` - uses PyPDF2 package and splits the pdf into individual page pdf and saves them in the same directory.
        - `[pdfSplitter.sh](http://pdfsplitter.sh)` - simple bash script to run `pdfSplitter.py`
        - The job is then submitted and monitored using `monitorGangaJob(job)` from Task 1
        - After the job is completed, all the jobs are stored into the `outputdir` of the Ganga job and information about them in `job.outputfiles`
        - Using the information in `job.outputfiles` , an array `args` is created containing the names of all the split files to be used for `ArgSplitter`
    - Second, another Ganga Job is created with `splitter` as `ArgSplitter(args=args)` , the job uses `[count.sh](http://count.sh)` to count the occurrence of word `the` in a given file. Input files for the job is directly taken from `job.outputfiles` and output file is set to `count.txt` which will contain the numeric count of occurrence of word `the`
        - `[count.sh](http://count.sh)` - takes a file name as argument and count the number of occurrence of the word `the` and stores the value in `output.txt`
        - The job is then submitted and monitored using `monitorGangaJob(job)` from Task 1
        - After the job is completed, the `output.txt` of all the subjobs is merged
    - Third, `CustomMerger()` is implemented to merge the `output.txt` from all the subjobs and save in it the directory `wordCounterOutput` . This merger uses `[merger.py](http://merger.py)` as module.
        - `[merger.py](http://merger.py)` - takes `output.txt` of all the subjobs, converts the value inside it into integer, add all the values and save it in the file in `wordCounterOutput`
- After all the jobs are finished, they are removed

**DEMO:** [https://youtu.be/8y0_s4Vr4VE](https://youtu.be/8y0_s4Vr4VE)

## Part 2

### Task 1 - Creating & Interacting with Database

For the task, a simple database was to be created, and Ganga job info was to be stored in it, Afterwards, the info was to be retrieved converting it back to a Ganga job. The file associated with this task is `./Part2/createDatabase.py`

- First few lines are imports for `SQLAlchemy` which is a ORM to create and manage databases in Python.
- Next section contains the configuration for `SQLAlchemy` - for this demonstration I have used `SQLite` (which is a local file based database solution, mostly used for prototyping) as it doesn't need us to start any server. But this solution can easily be migrated to a database server with just one change of line, that is `DATABASE_URI`
- In the next section, I have described a class which will be used by `SQLAlchemy` to create table and do operations on it.
- Function `recreateDatabase` - is a function to drop all information in the database and recreate it fresh - this is helpful for the task (not applicable besides prototyping)
- Function `addToDatabase` - takes a Ganga Job Object as an argument and stores it's text format in the database
- Function `readFromDatabase` - takes Database Job ID as an argument and return the text related to that Job
- Function `createJob` -  creates a job using the text provided by `readFromDatabase` function
- Function `main()` - using `createBasicGangaJob` from Task 1 create a basic Ganga Job, adds it to database, and using `readFromDatabase` the job text is stored in `jobinfo` variable, and using `createJob` function the basic job is recreated and submitted to run. The recreatedJob is monitored using `monitorGangaJob` from Task 1. After the job is finished, it is removed.

**DEMO:** [https://youtu.be/8y0_s4Vr4VE](https://youtu.be/8y0_s4Vr4VE)

### Task 2 - Measure Time

For this task, we had to measure time taken to run `readFromDatabase` function and `createJob` function 1000 times. The file associated with this task is `./Part2/timeCalc.py`

- First few lines are import for `timeit`
- Function `readFromDatabase_time` - using `timeit.timeit` benchmarks the time it take for `readFromDatabase` function to run 1000 times.
- Function `createJob_time` - using `timeit.timeit` benchmarks the time it take for `createJob` function to run 100 times.

**DEMO:** [https://youtu.be/8y0_s4Vr4VE](https://youtu.be/8y0_s4Vr4VE)

## Part 3

### Task 1 - Starting Up Simple Web Server

#TODO

---