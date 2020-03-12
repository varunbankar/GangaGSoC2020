# Ganga Project GSoC 2020 Challenge

# Introduction

Hello, I am Varun Bankar, an undergraduate student at BITS Pilani, Goa studying Computer Science. Doing this challenge was a fun experience. It helped me understand the codebase and functionality of Ganga in a much better way. I would like to sincerely thank Mr. Ulrik Egede for helping me throughout whenever I needed help. Below is my solution for this challenge and information on my approach for each section of the challenge.

# How to Set Up

As per the challenge instructions, this repository can be set up in the following way:

    virtualenv -p python3 GSoC
    cd GSoC/
    . bin/activate
    pip install -e git+https://github.com/varunbankar/GangaGSoC2020#egg=gangagsoc

# Challenge

## Part 1

### Task 1 - Creating Simple Ganga Job

The Python file associated with this task is `./Part1/basicGangaJob.py` . I will briefly walk through the code below:

- First few lines are the imports.
- I noticed that we need to manually enable monitoring of Ganga job by using  `ganga.enableMonitoring()` or the script won't be able to track the status of the job.
- Function `createBasicGangaJob(args="Hello World")` - creates a Ganga Job with specific set attributes and returns it. Parameter of the function accepts the arguments to `/bin/echo` whose default value is "`Hello World"`.
- Function `run_until_completed` - waits until the jobs status turns to 'completed'.

**SCREENSHOT:**

**DEMO: #TOUPLOAD**

### Task 2 - Splitting PDF, Using Subjobs to Count Words, Merging the Output

The Python file associated with this task is `./Part1/wordCounter.py` with the helper modules `pdfSplitter.py`, `pdfSplitter.sh`, `count.sh`, `merger.py` . 

- The `main()` function can be divided into 3 parts:
    - First, A Ganga Job is created to split `CERN.pdf` into individual pages. `[pdfSplitter.py](http://pdfsplitter.py)` & `[pdfSplitter.sh](http://pdfsplitter.sh)` are given as input files.
        - `[pdfSplitter.py](http://pdfsplitter.py)` - uses PyPDF2 package and splits the pdf into individual page pdf and saves them in the same directory.
        - `[pdfSplitter.sh](http://pdfsplitter.sh)` - simple bash script to run `pdfSplitter.py`
        - After the job is completed, all the files are stored in the `outputdir` of the Ganga job and information about them in `job.outputfiles`
        - Using the information in `job.outputfiles` , an array `args` is created containing the names of all the split files to be used for `ArgSplitter`
    - Second, another Ganga Job is created with splitter as `ArgSplitter(args=args)` , the job uses `[count.sh](http://count.sh)` to count the occurrence of word `the` in a given file. Input files for the job is directly taken from `job.outputfiles` and output file is set to `count.txt` which will contain the numeric count of occurrence of word 'the'
        - `[count.sh](http://count.sh)` - takes a file name as argument and count the number of occurrence of the word 'the' and stores the value in `output.txt`
        - After the job is completed, the `output.txt` of all the subjobs is merged
    - Third, `CustomMerger()` is implemented to merge the `output.txt` from all the subjobs and save in it the directory `wordCounterOutput` . This merger uses `[merger.py](http://merger.py)` as module.
        - `[merger.py](http://merger.py)` - takes `output.txt` of all the subjobs, converts the value inside it into integer, add all the values and save it in the file in `wordCounterOutput`
- After all the jobs are finished, they are removed.

**SCREENSHOT:**

**DEMO: #TOUPLOAD**

## Part 2

### Task 1 - Creating & Interacting with Database

The file associated with this task is `./Part2/createDatabase.py`

- First few lines are imports for `SQLAlchemy` .
- Next section contains the configuration for `SQLAlchemy` - for this demonstration I have used `SQLite` . But this solution can easily be migrated to a database server with just one change of line, that is `DATABASE_URI`
- In the next section, I have described a class which will be used by `SQLAlchemy` to create table and do operations on it.
- Function `recreateDatabase` - drops all information in the database and recreate it fresh - this is helpful for the task (not applicable besides prototyping)
- Function `addToDatabase` - takes a Ganga Job Object as an argument and stores it's text format in the database
- Function `readFromDatabase` - takes Database Job ID as an argument and return the text related to that Job
- Function `reCreateJob` -  creates a job using the text provided by `readFromDatabase` function
- Function `main()` - using `createBasicGangaJob` from Task 1 create a basic Ganga Job, adds it to database, and using `readFromDatabase` the job text is stored in `jobinfo` variable, and using `createJob` function the basic job is recreated and submitted to run. After the job is finished, it is removed.

**SCREENSHOT:**

**DEMO: #TOUPLOAD**

### Task 2 - Measure Time

The file associated with this task is `./Part2/timeCalc.py`

- First few lines are import for `timeit`
- Function `readFromDatabase_time` - using `timeit.timeit` benchmarks the time it take for `readFromDatabase` function to run 1000 times.
- Function `reCreateJob_time` - using `timeit.timeit` benchmarks the time it take for `reCreateJob` function to run 100 times.

**SCREENSHOTS:**

**DEMO: #TOUPLOAD**

## Part 3

### Task 1 - Starting Up Simple Web Server

#TODO

---
