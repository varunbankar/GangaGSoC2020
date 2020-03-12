# Ganga Project GSoC 2020 Challenge

# Introduction

Hello, I am Varun Bankar, an undergraduate student at BITS Pilani, Goa studying Computer Science. Doing this challenge was a very fun experience. It helped me understand the codebase and functionality of Ganga in a much better way. I would like to sincerely thank Mr. Ulrik Egede for helping me throughout whenever I needed help. Below is my solution for this challenge and information on my approach for each section of the challenge.

# How to Set Up

As per the challenge instructions, this repository can be set up in the following way:

    virtualenv -p python3 GSoC
    cd GSoC/
    . bin/activate
    pip install -e git+https://github.com/varunbankar/GangaGSoC2020#egg=gangagsoc

# Challenge

## Part 1

### Task 1 - Creating Simple Ganga Job

The Python file associated with this task is `./Part1/basicGangaJob.py` and can be run by `python basicGangaJob.py`. I will briefly walk through the code below:

- First few lines are the imports.
- I noticed that we need to manually enable monitoring of Ganga job by using  `ganga.enableMonitoring()` or the script won't be able to track the status of the job.
- Function `createBasicGangaJob(args="Hello World")` - creates a Ganga Job with specific set attributes and returns it. Parameter of the function accepts the arguments to `/bin/echo` whose default value is "`Hello World"`.
- Function `run_until_completed` - waits until the jobs status turns to 'completed'.

**SCREENSHOT:**
![Alt text](https://snipboard.io/m0BWSp.jpg "Optional title")

**DEMO: #TOUPLOAD**

### Task 2 - Splitting PDF, Using Subjobs to Count Words, Merging the Output

The Python file associated with this task is `./Part1/wordCounter.py` with the helper modules `pdfSplitter.py`, `pdfSplitter.sh`, `count.sh`, `merger.py`. This script can be run by `python wordCounter.py`.

- The `main()` function can be divided into 3 parts:
    - First, A Ganga Job is created to split `CERN.pdf` into individual pages. `pdfSplitter.py` & `pdfSplitter.sh` are given as input files.
        - `pdfSplitter.py` - uses PyPDF2 package and splits the pdf into individual page pdf and saves them in the same directory.
        - `pdfSplitter.sh` - simple bash script to run `pdfSplitter.py`
        - After the job is completed, all the files are stored in the `outputdir` of the Ganga job and information about them in `job.outputfiles`
        - Using the information in `job.outputfiles` , an array `args` is created containing the names of all the split files to be used for `ArgSplitter`
    - Second, another Ganga Job is created with splitter as `ArgSplitter(args=args)` , the job uses `count.sh` to count the occurrence of word `the` in a given file. Input files for the job is directly taken from `job.outputfiles` and output file is set to `count.txt` which will contain the numeric count of occurrence of word 'the'
        - `count.sh` - takes a file name as argument and count the number of occurrence of the word 'the' and stores the value in `output.txt`
        - After the job is completed, the `output.txt` of all the subjobs is merged
    - Third, `CustomMerger()` is implemented to merge the `output.txt` from all the subjobs and save in it the directory `wordCounterOutput` . This merger uses `merger.py` as module.
        - `merger.py` - takes `output.txt` of all the subjobs, converts the value inside it into integer, add all the values and save it in the file in `wordCounterOutput`
- After all the jobs are finished, they are removed.

**SCREENSHOT:**
![Alt text](https://snipboard.io/SOjRGu.jpg "Optional title")

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
![Alt text](https://snipboard.io/KzNOFZ.jpg "Optional title")

**DEMO: #TOUPLOAD**

### Task 2 - Measure Time

The file associated with this task is `./Part2/timeCalc.py`

- First few lines are import for `timeit`
- Function `readFromDatabase_time` - using `timeit.timeit` benchmarks the time it take for `readFromDatabase` function to run 1000 times.
- Function `reCreateJob_time` - using `timeit.timeit` benchmarks the time it take for `reCreateJob` function to run 100 times.

**SCREENSHOTS:**
![Alt text](https://snipboard.io/FfWwPt.jpg "Optional title")

**DEMO: #TOUPLOAD**

## Pytest

**TestSimpleJob.py**
![Alt text](https://snipboard.io/RQ7FN2.jpg "Optional title")

**TestWordCounter.py**
![Alt text](https://snipboard.io/piV1gv.jpg "Optional title")

**TestDatabase.py**
![Alt text](https://snipboard.io/rAGROu.jpg "Optional title")

## Part 3

For this Part of the challenge, I have used Flask web framework for Python to create a web server. Before going into the working of it, I would like to explain the structure of the project. All the files related to this task reside in `./Part3/` folder. The web server can be started by `python app.py`.

- `app.py` - used to start Flask server at `localhost:5000`
- `config.py` - has configuration related to flask stored in a class.
- `app` - package which contains the core files.
    - `routes.py` - here resides the logic of what routes are available and what must be done when the specific route is requested.
    - `templates` - folder which has all the HTML file which are dynamically rendered using Jinja2.
    - `static` - folder which has static files such as `main.css` , `home.js` , `jobs.js`.

Now the basic structure is discussed, the core functionality lies in `routes.py` , `home.js`, `jobs.js`.

- **The GUI has 4 pages:**
    - **Home:** Has a quick statistics section which gets updated every 5 seconds (time can be modified according to requirement) by making an API call to the server, has another sections which lists out 10 Recent Jobs which are also updated every 5 seconds by making an API call to the server and lastly, there is a section called "Programming Fun" which makes an AJAX request to a external API and fetches a joke, it is updated every 8 seconds.
    - **Create:** I have created the layout to showcase how the create page can look, but here only the deploy section is working. Deploy section has 2 buttons, one is to submit a Ganga Job to execute `Sleep(60)` and another is to submit 15 Ganga Job to execute `Sleep(15)`, `Sleep(20)`...and so on.
    - **Jobs:** This page lists out all the jobs and their information in a tabular form, here also the status of the jobs are updated every 5 seconds by making an API call to the server. Here the "Job Info" button is just to showcase the layout of how the GUI might look.
    - Config: This page lists out Ganga config for each section in a nice tabular way with their docstrings and effective value.
- **Javascript:**
    - **home.js:** Utilised by Home page, makes 3 AJAX requests.
        - One request is make to an external API to fetch a joke every 8 seconds
        - One is made to update quick statistics section every 5 seconds
        - One is made to update Recent Job status every 5 seconds (NOTE: the request is only made when there is atleast one job who's status is not in ["new", "completed", "failed"]
    - **jobs.js:** Utilised by Jobs page, makes an AJAX API request to the server every 5 seconds if there is atleast one job who's status is not in ["new", "completed", "failed"].
- **API:**
    - `localhost:5000/api/info` - If "GET" request is made, returns information about every job in JSON format.
    - `localhost:5000/api/info` - If "POST" request is made and "job_ids" data is given, then returns information about the jobs with job id in job_ids in JSON format
    - `localhost:5000/api/info/<int:job_id>` - Returns information about job with job.id = job_id in JSON format

**SCREENSHOTS:**

**HOME**
![Alt text](https://snipboard.io/CdrWw5.jpg "Optional title")

**CREATE**
![Alt text](https://snipboard.io/1MpelJ.jpg "Optional title")

**JOBS**
![Alt text](https://snipboard.io/LHnfiX.jpg "Optional title")

**CONFIG**
![Alt text](https://snipboard.io/zEqutd.jpg "Optional title")

---
